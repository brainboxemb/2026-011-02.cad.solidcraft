"""Tests for the cheap CAD CI runner."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

import cad_ci  # noqa: E402


class CadCiTests(unittest.TestCase):
    def test_compile_runs_only_selected_models(self):
        plan = {
            "scpf_models": ["bolted-flange"],
            "scpc_models": [],
            "site_refresh": False,
        }
        with TemporaryDirectory() as temp, \
             patch.object(cad_ci, "run") as run, \
             patch.object(cad_ci, "command_check") as check:
            out = Path(temp)
            cad_ci.compile_models(plan, out)

        self.assertEqual(run.call_count, 1)
        command = run.call_args.args[0]
        self.assertEqual(command[0:3], [sys.executable, "-m", "scpf"])
        self.assertTrue(
            str(command[3]).replace("\\", "/").endswith(
                "models/basic/bolted_flange/scpf/model.py"
            )
        )
        check.assert_called_once()

    def test_site_build_is_skipped_when_plan_does_not_request_it(self):
        plan = {"site_refresh": False}
        with TemporaryDirectory() as temp, patch.object(cad_ci, "run") as run:
            root = Path(temp)
            cad_ci.build_site(
                plan=plan,
                output_root=root / "output",
                previous_site=root / "previous",
                source_sha="abc",
            )
        run.assert_not_called()

    def test_site_build_uses_generated_selected_output_and_previous_site(self):
        plan = {"site_refresh": True}
        with TemporaryDirectory() as temp, patch.object(cad_ci, "run") as run:
            root = Path(temp)
            cad_ci.build_site(
                plan=plan,
                output_root=root / "output",
                previous_site=root / "previous",
                source_sha="abc",
            )

        self.assertEqual(run.call_count, 2)
        build = run.call_args_list[0].args[0]
        smoke = run.call_args_list[1].args[0]
        self.assertIn("scripts/ci/build-results.py", build)
        self.assertIn(str(root / "previous"), build)
        self.assertIn("scripts/ci/test-results.py", smoke)


if __name__ == "__main__":
    unittest.main()
