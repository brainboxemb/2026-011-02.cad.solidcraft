from pathlib import Path
import unittest

from cad_model_ci.items import CadModel, PythonModule
from cad_model_ci.config import BuildSelection, SolidCraftCandidate
from cad_model_ci.selection import changed_selection, expand_model_dependents


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
    CadModel(
        "screen",
        Path("models/screen"),
        "forge",
        Path("scpf/model.py"),
        watch=("models/screen/**",),
        dependencies=("box",),
    ),
    CadModel(
        "case",
        Path("models/case"),
        "forge",
        Path("scpf/model.py"),
        watch=("models/case/**",),
        dependencies=("screen",),
    ),
    CadModel(
        "parked",
        Path("models/parked"),
        "forge",
        Path("scpf/model.py"),
        watch=("models/parked/**",),
        process=False,
    ),
    CadModel(
        "parked-dependent",
        Path("models/parked-dependent"),
        "forge",
        Path("scpf/model.py"),
        watch=("models/parked-dependent/**",),
        dependencies=("box",),
        process=False,
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


    def test_selected_component_expands_to_transitive_dependents(self):
        selection = BuildSelection(
            branch="dev",
            modules=(),
            models=("box",),
            tasks=("test", "build"),
        )
        result = expand_model_dependents(selection, MODELS)
        self.assertEqual(result.models, ("box", "screen", "case"))

    def test_dependent_expansion_preserves_runtime_candidate(self):
        candidate = SolidCraftCandidate(
            "ghcr.io/brainboxemb/cad-solidcraft@sha256:" + "a" * 64,
            "0.50.0",
        )
        selection = BuildSelection(
            branch="issue/122-runtime",
            modules=(),
            models=("box",),
            tasks=("test", "build"),
            solidcraft_candidate=candidate,
        )

        result = expand_model_dependents(selection, MODELS)

        self.assertIs(result.solidcraft_candidate, candidate)
        self.assertEqual(result.models, ("box", "screen", "case"))

    def test_changed_process_false_model_is_not_selected_automatically(self):
        result = changed_selection(
            branch="dev",
            paths=("models/parked/model.yml",),
            modules=MODULES,
            models=MODELS,
        )
        self.assertEqual(result.modules, ())
        self.assertEqual(result.models, ())

    def test_model_impact_module_excludes_process_false_models(self):
        result = changed_selection(
            branch="dev",
            paths=("modules/build/src/build.py",),
            modules=MODULES,
            models=MODELS,
        )
        self.assertEqual(result.modules, ("build",))
        self.assertEqual(result.models, ("box", "case", "plate", "screen"))

    def test_dependent_expansion_does_not_auto_add_process_false_models(self):
        selection = BuildSelection(
            branch="dev",
            modules=(),
            models=("box",),
            tasks=("test", "build"),
        )
        result = expand_model_dependents(selection, MODELS)
        self.assertEqual(result.models, ("box", "screen", "case"))

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
        self.assertEqual(result.models, ("box", "case", "plate", "screen"))

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
