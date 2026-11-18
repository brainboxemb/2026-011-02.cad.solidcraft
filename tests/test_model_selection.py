"""Targeted CAD model selection contracts."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import MODELS, model_input_paths, model_slugs  # noqa: E402
from select_models import (  # noqa: E402
    _matches,
    affected_models,
    needs_site_refresh,
    select_models,
)


class TargetedModelSelectionTests(unittest.TestCase):
    def test_one_model_source_change_selects_only_that_model(self):
        self.assertEqual(
            affected_models(
                ["models/basic/bolted_flange/scpf/model.py"],
                kind="native",
            ),
            ("bolted-flange",),
        )

    def test_scpc_change_selects_only_matching_scpc_model(self):
        self.assertEqual(
            affected_models(
                ["models/basic/bolted_flange/scpc/model.py"],
                kind="scpc",
            ),
            ("bolted-flange",),
        )

    def test_directory_inputs_are_prefix_matches(self):
        watched = "models/components/guide_rail/scpf/"
        changed = "models/components/guide_rail/scpf/profiles.py"
        self.assertIn(watched, model_input_paths("guide-rail"))
        self.assertIn(watched, model_input_paths("simple-mft-assembly"))
        self.assertTrue(_matches(changed, watched))

    def test_model_root_readme_selects_models_sharing_that_root(self):
        changed = ["models/components/guide_rail/README.md"]
        selected = affected_models(changed, kind="native")
        self.assertEqual(
            selected,
            ("guide-rail", "guide-rail-makita"),
        )
        self.assertNotIn("simple-mft-assembly", selected)

    def test_model_root_check_selects_only_owning_model(self):
        changed = ["models/advanced/hub75_wood_frame/check.py"]
        selected = affected_models(changed, kind="native")
        self.assertEqual(selected, ("hub75-wood-frame",))

    def test_unrelated_readme_does_not_select_models(self):
        changed = ["docs/README.md"]
        self.assertEqual(affected_models(changed, kind="native"), ())

    def test_shared_guide_rail_code_selects_real_dependants(self):
        selected = affected_models(
            ["models/components/guide_rail/scpf/profiles.py"],
            kind="native",
        )
        self.assertEqual(
            set(selected),
            {
                "guide-rail",
                "guide-rail-makita",
                "simple-mft-assembly",
            },
        )

    def test_corner_bracket_change_selects_all_real_dependants(self):
        selected = affected_models(
            ["models/components/corner_bracket/scpf/model.py"],
            kind="native",
        )
        self.assertEqual(
            set(selected),
            {"corner-bracket", "hub75-wood-frame", "hub75-display2"},
        )

    def test_non_catalog_basic_hub75_component_selects_both_displays(self):
        selected = affected_models(
            ["models/components/hub75_panel/basic/scpf/model.py"],
            kind="native",
        )
        self.assertEqual(
            selected,
            ("hub75-wood-frame", "hub75-display2"),
        )

    def test_forge_dependency_pin_does_not_implicitly_select_all(self):
        self.assertEqual(
            affected_models(["dependencies.repos"], kind="native"),
            (),
        )

    def test_solidcraft_workflow_version_change_does_not_select_all(self):
        self.assertEqual(
            affected_models(
                [".github/workflows/native-cad.yml"],
                kind="native",
            ),
            (),
        )

    def test_explicit_models_mode_builds_only_requested_models(self):
        self.assertEqual(
            select_models(
                mode="models",
                kind="native",
                models=("bolted-flange", "bracket"),
            ),
            ("bolted-flange", "bracket"),
        )

    def test_explicit_models_mode_filters_by_build_capability(self):
        requested = ("bolted-flange", "bracket")
        selected = select_models(
            mode="models",
            kind="scpc",
            models=requested,
        )
        self.assertEqual(
            selected,
            tuple(slug for slug in requested if slug in model_slugs("scpc")),
        )

    def test_explicit_all_mode_is_the_only_full_catalog_selection(self):
        self.assertEqual(
            select_models(mode="all", kind="native"),
            model_slugs("native"),
        )

    def test_explicit_model_mode_rejects_unknown_slug(self):
        with self.assertRaisesRegex(ValueError, "unknown model"):
            select_models(
                mode="models",
                kind="native",
                models=("does-not-exist",),
            )

    def test_catalog_change_refreshes_site_without_geometry_build(self):
        paths = ["scripts/ci/model_catalog.py"]
        selected = affected_models(paths, kind="native")
        self.assertEqual(selected, ())
        self.assertTrue(needs_site_refresh(paths, selected))

    def test_publisher_change_refreshes_site_without_geometry(self):
        paths = [".github/workflows/publish-cad.yml"]
        self.assertEqual(affected_models(paths, kind="native"), ())
        self.assertTrue(needs_site_refresh(paths, ()))

    def test_output_store_change_refreshes_site_without_geometry(self):
        paths = ["scripts/ci/output_store.py"]
        self.assertEqual(affected_models(paths, kind="native"), ())
        self.assertTrue(needs_site_refresh(paths, ()))

    def test_model_change_refreshes_site(self):
        paths = ["models/basic/bolted_flange/scpf/model.py"]
        selected = affected_models(paths, kind="native")
        self.assertEqual(selected, ("bolted-flange",))
        self.assertTrue(needs_site_refresh(paths, selected))

    def test_unrelated_change_does_not_request_geometry_or_site(self):
        paths = ["notes/idea.md"]
        self.assertEqual(affected_models(paths, kind="native"), ())
        self.assertFalse(needs_site_refresh(paths, ()))


if __name__ == "__main__":
    unittest.main()
