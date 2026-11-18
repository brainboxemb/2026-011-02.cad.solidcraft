"""Tests for one CAD CI build plan."""

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from build_plan import make_plan  # noqa: E402


class BuildPlanTests(unittest.TestCase):
    def test_one_model_change_selects_only_that_model(self):
        plan = make_plan(
            mode="changed",
            paths=("models/basic/bolted_flange/scpf/model.py",),
        )
        self.assertEqual(plan["scpf_models"], ["bolted-flange"])
        self.assertEqual(plan["native_models"], ["bolted-flange"])
        self.assertTrue(plan["site_refresh"])

    def test_pipeline_change_adds_one_plate_end_to_end_smoke(self):
        plan = make_plan(
            mode="changed",
            paths=("scripts/ci/native_ci.py",),
            event_name="pull_request",
            ref_name="feature/ci",
            pull_request=12,
        )
        self.assertEqual(plan["scpf_models"], ["plate"])
        self.assertEqual(plan["native_models"], ["plate"])
        self.assertTrue(plan["site_refresh"])
        self.assertTrue(plan["publishable"])

    def test_toolchain_pin_change_does_not_select_catalog(self):
        plan = make_plan(
            mode="changed",
            paths=("dependencies.repos",),
        )
        self.assertEqual(plan["scpf_models"], [])
        self.assertEqual(plan["scpc_models"], [])
        self.assertEqual(plan["native_models"], [])
        self.assertFalse(plan["site_refresh"])

    def test_explicit_models_mode_stays_targeted(self):
        plan = make_plan(
            mode="models",
            models=("bolted-flange",),
        )
        self.assertEqual(plan["scpf_models"], ["bolted-flange"])
        self.assertEqual(plan["native_models"], ["bolted-flange"])
        self.assertTrue(plan["site_refresh"])

    def test_all_mode_is_explicit(self):
        plan = make_plan(mode="all")
        self.assertGreater(len(plan["scpf_models"]), 1)
        self.assertGreater(len(plan["native_models"]), 1)

    def test_pull_request_publication_is_scoped_to_pr(self):
        plan = make_plan(
            mode="changed",
            paths=("models/basic/bolted_flange/scpf/model.py",),
            event_name="pull_request",
            ref_name="feature/test",
            pull_request=42,
        )
        self.assertEqual(plan["channel"], "preview")
        self.assertEqual(plan["preview_key"], "pr-42")
        self.assertTrue(plan["publishable"])
        self.assertTrue(plan["public_base"].endswith("/preview/pr-42"))

    def test_push_to_main_targets_stable_publication(self):
        plan = make_plan(
            mode="changed",
            paths=("site/results.css",),
            event_name="push",
            ref_name="main",
        )
        self.assertEqual(plan["channel"], "stable")
        self.assertEqual(plan["preview_key"], "")
        self.assertTrue(plan["publishable"])

    def test_manual_main_run_is_stable_without_operator_publish_choice(self):
        from build_plan import publication_target

        target = publication_target(
            event_name="workflow_dispatch",
            ref_name="main",
        )
        self.assertEqual(target["channel"], "stable")
        self.assertEqual(target["preview_key"], "")

    def test_manual_branch_run_is_preview_without_operator_publish_choice(self):
        from build_plan import publication_target

        target = publication_target(
            event_name="workflow_dispatch",
            ref_name="feature/test",
        )
        self.assertEqual(target["channel"], "preview")
        self.assertEqual(target["preview_key"], "branch-feature-test")


if __name__ == "__main__":
    unittest.main()
