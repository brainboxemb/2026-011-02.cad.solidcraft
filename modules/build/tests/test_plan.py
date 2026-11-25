from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_model_build.config import (
    ForgePin,
    ModelConfig,
    ModelVariant,
    ProjectConfig,
    SnapshotSpec,
    SolidCraftPin,
)
from cad_model_build.plan import resolve_plan


class BuildPlanTests(unittest.TestCase):
    def project(self):
        return ProjectConfig(
            stable_branch="main",
            development_branch="dev",
            build_branch="build",
            forge=ForgePin("brainboxemb/lib.py.solidcraft.forge", "v0.14.0"),
            solidcraft=SolidCraftPin(
                "ghcr.io/brainboxemb/cad-solidcraft:v0.3.5",
                "0.48.1",
            ),
            models_root=Path("models"),
            output_root=Path("build"),
        )

    @patch("cad_model_build.plan.source_sha", return_value="b" * 40)
    def test_single_source_owner_keeps_existing_output_shape(self, _source_sha):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            root = repo / "models" / "box"
            model = ModelConfig(
                id="box",
                root=root,
                variants=(ModelVariant("box", Path("scpf/model.py")),),
                artifacts=("stl",),
                snapshots=(SnapshotSpec("top.png", {"pitch": -1.55}),),
                snapshot_camera={"yaw": -0.4},
            )
            plan = resolve_plan(
                repo=repo,
                project=self.project(),
                models=(model,),
                selected_ids=("box",),
                namespace="dev",
            )
            row = plan["models"][0]
            self.assertEqual(row["id"], "box")
            self.assertEqual(row["owner"], "box")
            self.assertEqual(row["commands"], "models/box/solidcraft.json")
            self.assertEqual(row["snapshot"]["camera"], {"yaw": -0.4})
            self.assertEqual(row["native"]["stl"], "models/box/model.stl")
            self.assertEqual(row["drawings"], [])
            self.assertEqual(row["snapshots"][0]["path"], "models/box/top.png")

    @patch("cad_model_build.plan.source_sha", return_value="b" * 40)
    def test_selected_owner_expands_all_variants_deterministically(self, _source_sha):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            root = repo / "models" / "guide-rail"
            model = ModelConfig(
                id="guide-rail",
                root=root,
                variants=(
                    ModelVariant("guide-rail-makita", Path("scpf/makita.py")),
                    ModelVariant("guide-rail", Path("scpf/model.py")),
                ),
                artifacts=(),
                snapshots=(),
            )
            plan = resolve_plan(
                repo=repo,
                project=self.project(),
                models=(model,),
                selected_ids=("guide-rail",),
                namespace="dev",
            )
            self.assertEqual(
                [row["id"] for row in plan["models"]],
                ["guide-rail", "guide-rail-makita"],
            )
            self.assertTrue(all(row["owner"] == "guide-rail" for row in plan["models"]))
            self.assertEqual(
                plan["models"][1]["source"],
                "models/guide-rail/scpf/makita.py",
            )


    @patch("cad_model_build.plan.source_sha", return_value="b" * 40)
    def test_selected_owners_are_ordered_by_priority_then_id(self, _source_sha):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            models_root = repo / "models"
            first = ModelConfig(
                id="advanced",
                root=models_root / "advanced",
                variants=(ModelVariant("advanced", Path("scpf/model.py")),),
                artifacts=(),
                snapshots=(),
                priority=30,
            )
            second = ModelConfig(
                id="component-b",
                root=models_root / "component-b",
                variants=(ModelVariant("component-b", Path("scpf/model.py")),),
                artifacts=(),
                snapshots=(),
                priority=20,
            )
            third = ModelConfig(
                id="component-a",
                root=models_root / "component-a",
                variants=(ModelVariant("component-a", Path("scpf/model.py")),),
                artifacts=(),
                snapshots=(),
                priority=20,
            )
            plan = resolve_plan(
                repo=repo,
                project=self.project(),
                models=(first, second, third),
                selected_ids=("advanced", "component-b", "component-a"),
                namespace="dev",
            )

            self.assertEqual(
                [row["id"] for row in plan["models"]],
                ["component-a", "component-b", "advanced"],
            )
            self.assertEqual(
                [row["priority"] for row in plan["models"]],
                [20, 20, 30],
            )

    @patch("cad_model_build.plan.source_sha", return_value="b" * 40)
    def test_dependency_precedes_consumer_even_when_priority_would_not(self, _source_sha):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            root = repo / "models"
            dependency = ModelConfig(
                id="component",
                root=root / "component",
                variants=(ModelVariant("component", Path("scpf/model.py")),),
                artifacts=(),
                snapshots=(),
                priority=50,
            )
            consumer = ModelConfig(
                id="assembly",
                root=root / "assembly",
                variants=(ModelVariant("assembly", Path("scpf/model.py")),),
                artifacts=(),
                snapshots=(),
                priority=10,
                dependencies=("component",),
            )
            plan = resolve_plan(
                repo=repo,
                project=self.project(),
                models=(consumer, dependency),
                selected_ids=("assembly", "component"),
                namespace="dev",
            )
            self.assertEqual(
                [row["id"] for row in plan["models"]],
                ["component", "assembly"],
            )
            self.assertEqual(
                plan["models"][1]["dependencies"],
                ["component"],
            )

    @patch("cad_model_build.plan.source_sha", return_value="b" * 40)
    def test_main_is_a_valid_output_namespace(self, _source_sha):
        with tempfile.TemporaryDirectory() as tmp:
            plan = resolve_plan(
                repo=Path(tmp),
                project=self.project(),
                models=(),
                selected_ids=(),
                namespace="main",
            )
            self.assertEqual(plan["namespace"], "main")
            self.assertEqual(plan["models"], [])


if __name__ == "__main__":
    unittest.main()
