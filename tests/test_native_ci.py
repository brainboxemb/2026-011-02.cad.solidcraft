"""Tests for the generic native CAD CI runner."""

from pathlib import Path
import json
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

import native_ci  # noqa: E402


class NativeCiTests(unittest.TestCase):
    def test_execute_uses_only_models_from_plan(self):
        plan = {
            "schema": 1,
            "native_models": ["plate", "bolted-flange"],
            "scpc_models": ["plate", "vent-plate"],
            "snapshot_models": ["plate"],
            "publishable": True,
            "channel": "preview",
            "preview_key": "pr-1",
            "public_base": "https://example.test/preview/pr-1",
        }
        with TemporaryDirectory() as temp:
            root = Path(temp)
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")

            with patch.object(
                native_ci,
                "toolchain_metadata",
                return_value={
                    "schema": 1,
                    "scpf_commit": "a" * 40,
                    "scpf_release": "0.1.0",
                    "scpc_commit": "b" * 40,
                    "solidcraft_version": "0.42.0",
                    "workflow_run": "7",
                    "toolchain_image": "ghcr.io/example/cad-ci:toolchain-abc",
                    "verified": True,
                },
            ), patch.object(native_ci, "compile_native") as compile_native, \
                 patch.object(native_ci, "snapshot") as snapshot, \
                 patch.object(native_ci, "run_native_checks") as native_checks, \
                 patch.object(native_ci, "compare_scpc") as compare_scpc, \
                 patch.object(native_ci, "copy_generated_commands") as copy_commands, \
                 patch.object(native_ci, "prepare_candidate") as prepare, \
                 patch.object(native_ci, "build_site") as build_site:
                compile_native.side_effect = lambda slug, native_root: native_root / slug

                native_ci.execute(
                    plan_path=plan_path,
                    output_root=root / "output",
                    stable_store=root / "store",
                    previous_site=root / "site",
                    source_sha="source",
                    workflow_run="7",
                    image_reference="ghcr.io/example/cad-ci:toolchain-abc",
                )

        self.assertEqual(
            [call.args[0] for call in compile_native.call_args_list],
            ["plate", "bolted-flange"],
        )
        self.assertEqual(
            [call.args[0] for call in snapshot.call_args_list],
            ["plate", "bolted-flange"],
        )
        native_checks.assert_called_once()
        compare_scpc.assert_called_once()
        self.assertEqual(compare_scpc.call_args.args[0], "plate")
        copy_commands.assert_called_once()
        prepare.assert_called_once()
        build_site.assert_called_once()

    def test_candidate_metadata_contains_immutable_image_reference(self):
        plan = {
            "schema": 1,
            "native_models": ["plate"],
            "scpc_models": [],
            "snapshot_models": [],
            "publishable": False,
            "channel": "preview",
            "preview_key": "branch-test",
            "public_base": "https://example.test/preview/branch-test",
        }
        metadata = {
            "schema": 1,
            "scpf_commit": "a" * 40,
            "scpf_release": "0.1.0",
            "scpc_commit": "b" * 40,
            "solidcraft_version": "0.42.0",
            "workflow_run": "8",
            "toolchain_image": "ghcr.io/example/cad-ci:toolchain-deadbeef",
            "verified": True,
        }
        with TemporaryDirectory() as temp:
            root = Path(temp)
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")

            with patch.object(native_ci, "toolchain_metadata", return_value=metadata), \
                 patch.object(native_ci, "compile_native", return_value=root / "output/native/plate"), \
                 patch.object(native_ci, "snapshot"), \
                 patch.object(native_ci, "run_native_checks"), \
                 patch.object(native_ci, "compare_scpc"), \
                 patch.object(native_ci, "copy_generated_commands"), \
                 patch.object(native_ci, "prepare_candidate") as prepare, \
                 patch.object(native_ci, "build_site"):
                native_ci.execute(
                    plan_path=plan_path,
                    output_root=root / "output",
                    stable_store=root / "store",
                    previous_site=root / "site",
                    source_sha="source",
                    workflow_run="8",
                    image_reference=metadata["toolchain_image"],
                )

        candidate_metadata = prepare.call_args.kwargs["metadata"]
        self.assertEqual(
            candidate_metadata["toolchain_image"],
            "ghcr.io/example/cad-ci:toolchain-deadbeef",
        )
        self.assertEqual(candidate_metadata["source_commit"], "source")


if __name__ == "__main__":
    unittest.main()
