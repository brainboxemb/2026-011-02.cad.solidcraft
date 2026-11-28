from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_model_build.config import BuildConfigError, ForgePin, ProjectConfig, SolidCraftPin
from cad_model_build.pipeline import execute


class PipelineTests(unittest.TestCase):
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

    def test_invalid_forge_qualification_ref_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(
                BuildConfigError,
                "exact 40-character lowercase commit SHA",
            ):
                execute(
                    repo=Path(tmp),
                    namespace="dev",
                    selected_ids=(),
                    forge_ref="exp",
                )

    @patch("cad_model_build.pipeline.run_native_batch")
    @patch("cad_model_build.pipeline.compile_plan")
    @patch("cad_model_build.pipeline.tested_solidcraft_version")
    @patch("cad_model_build.pipeline.build_wheel")
    @patch("cad_model_build.pipeline.write_plan")
    @patch("cad_model_build.pipeline.resolve_plan")
    @patch("cad_model_build.pipeline.discover_models", return_value=())
    @patch("cad_model_build.pipeline.load_project")
    def test_empty_selection_writes_plan_without_forge_or_docker(
        self,
        load_project,
        _discover,
        resolve_plan,
        write_plan,
        build_wheel,
        tested_version,
        compile_plan,
        run_native,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            load_project.return_value = self.project()
            resolve_plan.return_value = {"models": []}
            expected = repo / "build/dev/build-plan.json"
            write_plan.return_value = expected

            actual = execute(repo=repo, namespace="dev", selected_ids=())

            self.assertEqual(actual, expected)
            build_wheel.assert_not_called()
            tested_version.assert_not_called()
            compile_plan.assert_not_called()
            run_native.assert_not_called()

    @patch("cad_model_build.pipeline.run_native_batch")
    @patch("cad_model_build.pipeline.compile_plan")
    @patch("cad_model_build.pipeline.tested_solidcraft_version", return_value="0.48.1")
    @patch("cad_model_build.pipeline.build_wheel")
    @patch("cad_model_build.pipeline.write_plan")
    @patch("cad_model_build.pipeline.resolve_plan")
    @patch("cad_model_build.pipeline.discover_models", return_value=())
    @patch("cad_model_build.pipeline.load_project")
    def test_non_empty_selection_compiles_then_runs_one_native_batch(
        self,
        load_project,
        _discover,
        resolve_plan,
        write_plan,
        build_wheel,
        _tested_version,
        compile_plan,
        run_native,
    ):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            project = self.project()
            load_project.return_value = project
            resolve_plan.return_value = {"models": [{"id": "box"}]}
            expected = repo / "build/dev/build-plan.json"
            write_plan.return_value = expected
            wheel = repo / "scpf.whl"
            build_wheel.return_value = wheel

            ref = "a" * 40
            actual = execute(
                repo=repo,
                namespace="dev",
                source_ref="issue/review",
                selected_ids=("box",),
                forge_ref=ref,
            )

            self.assertEqual(actual, expected)
            self.assertEqual(
                resolve_plan.call_args.kwargs["source_ref"],
                "issue/review",
            )
            self.assertEqual(
                resolve_plan.call_args.kwargs["forge_ref"],
                ref,
            )
            self.assertEqual(
                build_wheel.call_args.kwargs["qualification_ref"],
                ref,
            )
            compile_plan.assert_called_once()
            run_native.assert_called_once()


if __name__ == "__main__":
    unittest.main()
