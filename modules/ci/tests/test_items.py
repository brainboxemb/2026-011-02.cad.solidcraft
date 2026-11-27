from pathlib import Path
import tempfile
import unittest

from cad_model_ci.config import ForgeDependency, ProjectConfig
from cad_model_ci.items import discover_models, discover_modules, select


class ItemTests(unittest.TestCase):
    def project(self):
        return ProjectConfig(
            stable_branch="main",
            development_branch="dev",
            forge=ForgeDependency(
                "brainboxemb/lib.py.solidcraft.forge",
                "v0.14.0",
            ),
            modules_root=Path("modules"),
            models_root=Path("models"),
            output_root=Path("build"),
        )

    def test_discovers_item_local_impact_and_nested_model_watch(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            module = repo / "modules" / "ci"
            module.mkdir(parents=True)
            (module / "ci.yml").write_text(
                "schema: 1\nid: ci\nkind: python\nimpact: full\n"
                "watch: [.github/workflows/ci.yml]\n",
                encoding="utf-8",
            )
            model = repo / "models" / "components" / "box"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf" / "model.py").write_text(
                "object()\n",
                encoding="utf-8",
            )
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\n"
                "source: scpf/model.py\nprocess: true\n",
                encoding="utf-8",
            )
            modules = discover_modules(repo, self.project())
            models = discover_models(repo, self.project())
            self.assertEqual(modules[0].impact, "full")
            self.assertIn("modules/ci/**", modules[0].watch)
            self.assertIn(".github/workflows/ci.yml", modules[0].watch)
            self.assertIn("models/components/box/**", models[0].watch)



    def test_model_inherits_nearest_group_priority_and_watch(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            models_root = repo / "models"
            models_root.mkdir()
            (models_root / "ci.yml").write_text(
                "schema: 1\nkind: group\npriority: 100\n",
                encoding="utf-8",
            )
            components = models_root / "components"
            components.mkdir()
            (components / "ci.yml").write_text(
                "schema: 1\nkind: group\npriority: 20\n",
                encoding="utf-8",
            )
            model = components / "box"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf/model.py").write_text("object()\n", encoding="utf-8")
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\nsource: scpf/model.py\n",
                encoding="utf-8",
            )

            models = discover_models(repo, self.project())

            self.assertEqual(len(models), 1)
            self.assertEqual(models[0].priority, 20)
            self.assertIn("models/components/ci.yml", models[0].watch)
            self.assertNotIn("models/ci.yml", models[0].watch)

    def test_models_are_discovered_in_priority_then_id_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for group_name, priority, model_id in (
                ("assemblies", 40, "z-assembly"),
                ("subassemblies", 30, "m-subassembly"),
                ("components", 20, "b-component"),
                ("basic", 10, "a-basic"),
            ):
                group = repo / "models" / group_name
                group.mkdir(parents=True)
                (group / "ci.yml").write_text(
                    f"schema: 1\nkind: group\npriority: {priority}\n",
                    encoding="utf-8",
                )
                model = group / model_id
                (model / "scpf").mkdir(parents=True)
                (model / "scpf/model.py").write_text(
                    "object()\n",
                    encoding="utf-8",
                )
                (model / "ci.yml").write_text(
                    f"schema: 1\nid: {model_id}\nbuilder: forge\n"
                    "source: scpf/model.py\n",
                    encoding="utf-8",
                )

            models = discover_models(repo, self.project())

            self.assertEqual(
                [model.id for model in models],
                ["a-basic", "b-component", "m-subassembly", "z-assembly"],
            )
            self.assertEqual(
                [model.priority for model in models],
                [10, 20, 30, 40],
            )

    def test_multi_variant_root_is_one_ci_item(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            model = repo / "models" / "components" / "rail"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf/model.py").write_text("object()\n", encoding="utf-8")
            (model / "scpf/makita.py").write_text("object()\n", encoding="utf-8")
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

            models = discover_models(repo, self.project())
            self.assertEqual(len(models), 1)
            self.assertEqual(models[0].id, "guide-rail")
            self.assertIsNone(models[0].source)
            self.assertIn("models/components/rail/**", models[0].watch)

    def test_model_dependencies_are_discovered_and_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            component = repo / "models" / "components" / "panel"
            assembly = repo / "models" / "assemblies" / "screen"
            for root in (component, assembly):
                (root / "scpf").mkdir(parents=True)
                (root / "scpf/model.py").write_text("object()\n", encoding="utf-8")
            (component / "ci.yml").write_text(
                "schema: 1\nid: panel\nbuilder: forge\nsource: scpf/model.py\n",
                encoding="utf-8",
            )
            (assembly / "ci.yml").write_text(
                "schema: 1\nid: screen\nbuilder: forge\nsource: scpf/model.py\n"
                "dependencies: [panel]\n",
                encoding="utf-8",
            )

            models = discover_models(repo, self.project())
            by_id = {model.id: model for model in models}
            self.assertEqual(by_id["screen"].dependencies, ("panel",))

    def test_unknown_model_dependency_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            model = repo / "models" / "screen"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf/model.py").write_text("object()\n", encoding="utf-8")
            (model / "ci.yml").write_text(
                "schema: 1\nid: screen\nbuilder: forge\nsource: scpf/model.py\n"
                "dependencies: [missing]\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(Exception, "unknown model dependency"):
                discover_models(repo, self.project())

    def test_cyclic_model_dependency_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for model_id, dependency in (("a", "b"), ("b", "a")):
                model = repo / "models" / model_id
                (model / "scpf").mkdir(parents=True)
                (model / "scpf/model.py").write_text("object()\n", encoding="utf-8")
                (model / "ci.yml").write_text(
                    f"schema: 1\nid: {model_id}\nbuilder: forge\n"
                    "source: scpf/model.py\n"
                    f"dependencies: [{dependency}]\n",
                    encoding="utf-8",
                )
            with self.assertRaisesRegex(Exception, "cyclic model dependency"):
                discover_models(repo, self.project())

    def test_process_false_model_is_discovered_but_not_selected_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            model = repo / "models" / "box"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf/model.py").write_text("object()\n", encoding="utf-8")
            (model / "ci.yml").write_text(
                "schema: 1\nid: box\nbuilder: forge\n"
                "source: scpf/model.py\nprocess: false\n",
                encoding="utf-8",
            )

            models = discover_models(repo, self.project())

            self.assertEqual(len(models), 1)
            self.assertFalse(models[0].process)
            self.assertEqual(select(models, None), ())
            self.assertEqual(
                [model.id for model in select(models, ("box",))],
                ["box"],
            )

    def test_process_false_model_remains_in_dependency_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            model = repo / "models" / "parked"
            (model / "scpf").mkdir(parents=True)
            (model / "scpf/model.py").write_text("object()\n", encoding="utf-8")
            (model / "ci.yml").write_text(
                "schema: 1\nid: parked\nbuilder: forge\n"
                "source: scpf/model.py\nprocess: false\n"
                "dependencies: [missing]\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(Exception, "unknown model dependency"):
                discover_models(repo, self.project())

    def test_selection_returns_only_requested_item(self):
        items = (
            type("Item", (), {"id": "one"})(),
            type("Item", (), {"id": "two"})(),
        )
        self.assertEqual([x.id for x in select(items, ("two",))], ["two"])


if __name__ == "__main__":
    unittest.main()
