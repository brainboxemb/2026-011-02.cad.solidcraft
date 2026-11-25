from pathlib import Path
import tempfile
import unittest

from cad_model_build.config import (
    active_variant_ids,
    BuildConfigError,
    discover_models,
    load_project,
)


PROJECT = """schema: 1
branches:
  stable: main
  development: dev
generated:
  build_branch: build
dependencies:
  forge:
    repository: brainboxemb/lib.py.solidcraft.forge
    version: v0.14.0
  solidcraft:
    image: ghcr.io/brainboxemb/cad-solidcraft:v0.3.5
    version: 0.48.1
roots:
  modules: modules
  models: models
  output: build
"""


def write_project(repo: Path) -> None:
    (repo / "ci.yml").write_text(PROJECT, encoding="utf-8")


def write_source(model: Path, relative: str) -> None:
    source = model / relative
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("object()\n", encoding="utf-8")


class BuildConfigTests(unittest.TestCase):
    def test_single_source_is_one_variant_with_owner_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            model = repo / "models" / "components" / "box"
            write_source(model, "scpf/model.py")
            (model / "ci.yml").write_text(
                """schema: 1
id: box
builder: forge
source: scpf/model.py
artifacts: [stl]
snapshot:
  camera:
    yaw: -0.4
snapshots:
  - name: top.png
    camera:
      pitch: -1.55
""",
                encoding="utf-8",
            )

            project = load_project(repo)
            models = discover_models(repo, project)
            self.assertEqual(project.build_branch, "build")
            self.assertEqual(project.forge.version, "v0.14.0")
            self.assertEqual(len(models), 1)
            self.assertEqual(models[0].id, "box")
            self.assertEqual(models[0].variants[0].id, "box")
            self.assertEqual(models[0].variants[0].source, Path("scpf/model.py"))
            self.assertEqual(models[0].artifacts, ("stl",))
            self.assertEqual(models[0].snapshot_camera, {"yaw": -0.4})
            self.assertEqual(models[0].snapshots[0].name, "top.png")

    def test_multi_variant_owner_expands_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            model = repo / "models" / "components" / "rail"
            write_source(model, "scpf/model.py")
            write_source(model, "scpf/makita.py")
            (model / "ci.yml").write_text(
                """schema: 1
id: guide-rail
builder: forge
variants:
  - id: guide-rail
    source: scpf/model.py
  - id: guide-rail-makita
    source: scpf/makita.py
""",
                encoding="utf-8",
            )

            models = discover_models(repo, load_project(repo))
            self.assertEqual(
                [(item.id, item.source) for item in models[0].variants],
                [
                    ("guide-rail", Path("scpf/model.py")),
                    ("guide-rail-makita", Path("scpf/makita.py")),
                ],
            )
            self.assertEqual(
                active_variant_ids(models),
                {"guide-rail", "guide-rail-makita"},
            )

    def test_source_and_variants_are_mutually_exclusive(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            model = repo / "models" / "box"
            write_source(model, "scpf/model.py")
            (model / "ci.yml").write_text(
                """schema: 1
id: box
builder: forge
source: scpf/model.py
variants:
  - id: box-alt
    source: scpf/model.py
""",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                BuildConfigError,
                "exactly one of source or variants",
            ):
                discover_models(repo, load_project(repo))

    def test_variant_ids_are_globally_unique(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            first = repo / "models" / "first"
            second = repo / "models" / "second"
            write_source(first, "scpf/a.py")
            write_source(second, "scpf/b.py")
            (first / "ci.yml").write_text(
                """schema: 1
id: first
builder: forge
variants:
  - id: shared
    source: scpf/a.py
""",
                encoding="utf-8",
            )
            (second / "ci.yml").write_text(
                """schema: 1
id: second
builder: forge
variants:
  - id: shared
    source: scpf/b.py
""",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(BuildConfigError, "duplicate build variant id"):
                discover_models(repo, load_project(repo))


    def test_nearest_group_priority_is_inherited(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            (repo / "models").mkdir()
            (repo / "models/ci.yml").write_text(
                "schema: 1\nkind: group\npriority: 100\n",
                encoding="utf-8",
            )
            components = repo / "models/components"
            components.mkdir()
            (components / "ci.yml").write_text(
                "schema: 1\nkind: group\npriority: 20\n",
                encoding="utf-8",
            )
            model = components / "box"
            write_source(model, "scpf/model.py")
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\nsource: scpf/model.py\n",
                encoding="utf-8",
            )

            models = discover_models(repo, load_project(repo))

            self.assertEqual(len(models), 1)
            self.assertEqual(models[0].priority, 20)

    def test_group_config_is_not_a_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            group = repo / "models/components"
            group.mkdir(parents=True)
            (group / "ci.yml").write_text(
                "schema: 1\nkind: group\npriority: 20\n",
                encoding="utf-8",
            )
            model = group / "box"
            write_source(model, "scpf/model.py")
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\nsource: scpf/model.py\n",
                encoding="utf-8",
            )

            models = discover_models(repo, load_project(repo))

            self.assertEqual([model.id for model in models], ["box"])

    def test_invalid_group_priority_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            group = repo / "models/components"
            group.mkdir(parents=True)
            (group / "ci.yml").write_text(
                "schema: 1\nkind: group\npriority: -1\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                BuildConfigError,
                "group priority must be a non-negative integer",
            ):
                discover_models(repo, load_project(repo))

    def test_dependencies_are_discovered_and_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            component = repo / "models" / "panel"
            assembly = repo / "models" / "screen"
            write_source(component, "scpf/model.py")
            write_source(assembly, "scpf/model.py")
            (component / "ci.yml").write_text(
                "schema: 1\nid: panel\nbuilder: forge\nsource: scpf/model.py\n",
                encoding="utf-8",
            )
            (assembly / "ci.yml").write_text(
                "schema: 1\nid: screen\nbuilder: forge\nsource: scpf/model.py\n"
                "dependencies: [panel]\n",
                encoding="utf-8",
            )

            models = discover_models(repo, load_project(repo))
            by_id = {model.id: model for model in models}
            self.assertEqual(by_id["screen"].dependencies, ("panel",))

    def test_unknown_dependency_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            model = repo / "models" / "screen"
            write_source(model, "scpf/model.py")
            (model / "ci.yml").write_text(
                "schema: 1\nid: screen\nbuilder: forge\nsource: scpf/model.py\n"
                "dependencies: [missing]\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(BuildConfigError, "unknown model dependency"):
                discover_models(repo, load_project(repo))

    def test_dependency_cycle_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            for model_id, dependency in (("a", "b"), ("b", "a")):
                model = repo / "models" / model_id
                write_source(model, "scpf/model.py")
                (model / "ci.yml").write_text(
                    f"schema: 1\nid: {model_id}\nbuilder: forge\n"
                    "source: scpf/model.py\n"
                    f"dependencies: [{dependency}]\n",
                    encoding="utf-8",
                )
            with self.assertRaisesRegex(BuildConfigError, "cyclic model dependency"):
                discover_models(repo, load_project(repo))

    def test_snapshots_are_optional(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            model = repo / "models" / "box"
            write_source(model, "scpf/model.py")
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\nsource: scpf/model.py\n",
                encoding="utf-8",
            )
            models = discover_models(repo, load_project(repo))
            self.assertEqual(models[0].snapshots, ())

    def test_process_false_model_is_not_discovered(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_project(repo)
            model = repo / "models" / "box"
            write_source(model, "scpf/model.py")
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\n"
                "source: scpf/model.py\nprocess: false\n",
                encoding="utf-8",
            )
            self.assertEqual(discover_models(repo, load_project(repo)), ())


if __name__ == "__main__":
    unittest.main()
