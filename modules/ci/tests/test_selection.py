from pathlib import Path
import unittest

from cad_model_ci.items import CadModel, PythonModule
from cad_model_ci.selection import changed_selection


MODULES = (
    PythonModule("ci", Path("modules/ci"), impact="full", watch=("modules/ci/**",)),
    PythonModule("build", Path("modules/build"), impact="models", watch=("modules/build/**",)),
    PythonModule("merge-policy", Path("modules/merge-policy"), watch=("modules/merge-policy/**",)),
)
MODELS = (
    CadModel(
        "box",
        Path("models/box"),
        "forge",
        Path("scpf/model.py"),
        watch=("models/box/**", "models/components/ci.yml"),
    ),
    CadModel(
        "plate",
        Path("models/plate"),
        "forge",
        Path("scpf/model.py"),
        watch=("models/plate/**",),
    ),
)


class SelectionTests(unittest.TestCase):
    def test_changed_model_selects_only_that_model(self):
        result = changed_selection(
            branch="dev",
            paths=("models/box/model.yml",),
            modules=MODULES,
            models=MODELS,
        )
        self.assertEqual(result.modules, ())
        self.assertEqual(result.models, ("box",))


    def test_changed_group_config_selects_models_in_that_group(self):
        result = changed_selection(
            branch="dev",
            paths=("models/components/ci.yml",),
            modules=MODULES,
            models=MODELS,
        )
        self.assertEqual(result.modules, ())
        self.assertEqual(result.models, ("box",))

    def test_changed_merge_policy_selects_only_itself(self):
        result = changed_selection(
            branch="dev",
            paths=("modules/merge-policy/src/policy.py",),
            modules=MODULES,
            models=MODELS,
        )
        self.assertEqual(result.modules, ("merge-policy",))
        self.assertEqual(result.models, ())

    def test_changed_build_module_adds_all_models(self):
        result = changed_selection(
            branch="dev",
            paths=("modules/build/src/build.py",),
            modules=MODULES,
            models=MODELS,
        )
        self.assertEqual(result.modules, ("build",))
        self.assertEqual(result.models, ("box", "plate"))

    def test_changed_ci_module_is_full(self):
        result = changed_selection(
            branch="dev",
            paths=("modules/ci/src/selection.py",),
            modules=MODULES,
            models=MODELS,
        )
        self.assertIsNone(result.modules)
        self.assertIsNone(result.models)

    def test_root_ci_change_is_full(self):
        result = changed_selection(
            branch="dev",
            paths=("ci.yml",),
            modules=MODULES,
            models=MODELS,
        )
        self.assertIsNone(result.modules)
        self.assertIsNone(result.models)

    def test_docs_and_build_yml_have_no_dev_build_impact(self):
        result = changed_selection(
            branch="dev",
            paths=("docs/manual.md", "build.yml"),
            modules=MODULES,
            models=MODELS,
        )
        self.assertEqual(result.modules, ())
        self.assertEqual(result.models, ())


if __name__ == "__main__":
    unittest.main()
