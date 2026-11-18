"""Tests for the single CAD pipeline entry point."""

from pathlib import Path
import json
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

import pipeline_ci  # noqa: E402


class PipelineCiTests(unittest.TestCase):
    def test_execute_runs_one_plan_then_cheap_and_native_phases(self):
        plan = {
            "schema": 1,
            "scpf_models": ["plate"],
            "scpc_models": [],
            "native_models": ["plate"],
            "snapshot_models": ["plate"],
            "site_refresh": True,
            "publishable": True,
            "channel": "preview",
            "preview_key": "pr-12",
            "public_base": "https://example.test/preview/pr-12",
        }
        with TemporaryDirectory() as temp:
            root = Path(temp)
            build = root / "build"
            pages = root / "pages"
            out = root / "output"
            build.mkdir()
            pages.mkdir()

            with patch.object(
                pipeline_ci,
                "configure_git_workspace",
            ) as configure, patch.object(
                pipeline_ci.build_plan,
                "changed_paths",
                return_value=("models/basic/plate/scpf/model.py",),
            ) as changed, patch.object(
                pipeline_ci.build_plan,
                "make_plan",
                return_value=plan,
            ) as make_plan, patch.object(
                pipeline_ci,
                "resolve_build_baseline",
                return_value=root / "resolved/main",
            ) as resolve, patch.object(
                pipeline_ci.cad_ci,
                "execute",
            ) as cheap, patch.object(
                pipeline_ci.native_ci,
                "execute",
            ) as native:
                result = pipeline_ci.execute(
                    mode="changed",
                    models="",
                    base_sha="base",
                    head_sha="head",
                    event_name="pull_request",
                    ref_name="feature/test",
                    pull_request=12,
                    output_root=out,
                    build_root=build,
                    previous_site=pages,
                    workflow_run="77",
                    image_reference="ghcr.io/example/cad-ci:toolchain-abc",
                )

        self.assertEqual(result, plan)
        configure.assert_called_once_with()
        changed.assert_called_once_with("base", "head")
        make_plan.assert_called_once()
        resolve.assert_called_once()
        cheap.assert_called_once()
        self.assertFalse(cheap.call_args.kwargs["build_site_output"])
        native.assert_called_once()
        self.assertEqual(
            native.call_args.kwargs["stable_store"],
            root / "resolved/main",
        )
        persisted = json.loads((out / "plan.json").read_text(encoding="utf-8"))
        self.assertEqual(persisted["preview_key"], "pr-12")

    def test_existing_build_main_needs_no_legacy_migration(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "build"
            destination = root / "resolved"
            (source / "main").mkdir(parents=True)
            (source / "main/marker.txt").write_text("ok", encoding="utf-8")

            with patch.object(
                pipeline_ci,
                "migrate_legacy_store_layout",
            ) as migrate:
                stable = pipeline_ci.resolve_build_baseline(source, destination)

        self.assertEqual(stable, destination / "main")
        migrate.assert_not_called()

    def test_legacy_build_is_migrated_only_in_resolved_copy(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "build"
            destination = root / "resolved"
            (source / "stable").mkdir(parents=True)

            def migrate(*, store):
                (store / "main").mkdir(parents=True)
                return ("plate",)

            with patch.object(
                pipeline_ci,
                "migrate_legacy_store_layout",
                side_effect=migrate,
            ):
                stable = pipeline_ci.resolve_build_baseline(source, destination)

            self.assertTrue(stable.is_dir())
            self.assertFalse((source / "main").exists())


if __name__ == "__main__":
    unittest.main()
