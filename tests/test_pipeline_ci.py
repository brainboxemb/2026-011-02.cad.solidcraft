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
    def test_execute_extends_plan_and_runs_tool_proof_before_native(self):
        """The stable plan and Plate proof feed the same native pipeline run."""

        initial = {
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
        extended = dict(initial)
        extended["scpf_models"] = ["plate", "new-model"]
        extended["native_models"] = ["plate", "new-model"]

        with TemporaryDirectory() as temp:
            root = Path(temp)
            build = root / "generated-build"
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
                return_value=initial,
            ) as make_plan, patch.object(
                pipeline_ci,
                "resolve_build_baseline",
                return_value=root / "resolved/main",
            ) as resolve, patch.object(
                pipeline_ci,
                "extend_plan_for_missing_stable",
                return_value=extended,
            ) as extend, patch.object(
                pipeline_ci.cad_ci,
                "execute",
            ) as cheap, patch.object(
                pipeline_ci,
                "run_tool_cad_ci_proof",
                return_value=("plate",),
            ) as tool_proof, patch.object(
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
                persisted = json.loads(
                    (out / "plan.json").read_text(encoding="utf-8")
                )

        self.assertEqual(result, extended)
        configure.assert_called_once_with()
        changed.assert_called_once_with("base", "head")
        make_plan.assert_called_once()
        resolve.assert_called_once()
        extend.assert_called_once_with(initial, root / "resolved/main")
        cheap.assert_called_once()
        tool_proof.assert_called_once_with(
            mode="changed",
            models="",
            base_sha="base",
            head_sha="head",
            paths=("models/basic/plate/scpf/model.py",),
            output_root=out,
        )
        native.assert_called_once()
        self.assertEqual(
            native.call_args.kwargs["stable_store"],
            root / "resolved/main",
        )
        self.assertEqual(persisted["scpf_models"], ["plate", "new-model"])

    def test_missing_stable_models_uses_verification_files(self):
        """A catalog directory without verification still counts as missing."""

        with TemporaryDirectory() as temp:
            stable = Path(temp)
            native = tuple(pipeline_ci.model_slugs("native"))
            self.assertTrue(native)

            for slug in native[:-1]:
                verification = (
                    stable
                    / pipeline_ci.model_build_path(slug)
                    / "verification.json"
                )
                verification.parent.mkdir(parents=True, exist_ok=True)
                verification.write_text("{}", encoding="utf-8")

            partial = stable / pipeline_ci.model_build_path(native[-1])
            partial.mkdir(parents=True, exist_ok=True)

            self.assertEqual(
                pipeline_ci.missing_stable_models(stable),
                (native[-1],),
            )

    def test_extend_plan_adds_missing_model_by_supported_kinds(self):
        """The plan uses catalog eligibility instead of hardcoded model names."""

        plan = {
            "scpf_models": ["plate"],
            "scpc_models": ["plate"],
            "native_models": ["plate"],
            "snapshot_models": [],
            "site_refresh": False,
            "publishable": False,
        }

        def kinds(kind):
            values = {
                "native": ("plate", "new-model"),
                "scpf": ("plate", "new-model"),
                "scpc": ("plate",),
                "native-snapshot-required": ("new-model",),
            }
            return values[kind]

        with patch.object(
            pipeline_ci,
            "missing_stable_models",
            return_value=("new-model",),
        ), patch.object(
            pipeline_ci,
            "model_slugs",
            side_effect=kinds,
        ), patch.object(
            pipeline_ci,
            "MODELS",
            {"plate": {}, "new-model": {}},
        ):
            result = pipeline_ci.extend_plan_for_missing_stable(
                plan,
                Path("/unused"),
            )

        self.assertEqual(result["scpf_models"], ["plate", "new-model"])
        self.assertEqual(result["scpc_models"], ["plate"])
        self.assertEqual(result["native_models"], ["plate", "new-model"])
        self.assertEqual(result["snapshot_models"], ["new-model"])
        self.assertTrue(result["site_refresh"])
        self.assertTrue(result["publishable"])

    def test_named_models_map_shared_variants_to_unique_item_roots(self):
        """Named catalog variants are grouped by their owning model-root item."""

        mapping = {
            "guide-rail": "guide-rail",
            "guide-rail-makita": "guide-rail",
            "bracket": "bracket",
        }
        with patch.object(
            pipeline_ci,
            "item_id_for_slug",
            side_effect=mapping.get,
        ):
            groups = pipeline_ci._tool_selection_groups(
                mode="models",
                models="guide-rail guide-rail-makita bracket",
                base_sha="",
                head_sha="head",
                paths=(),
            )

        self.assertEqual(
            groups,
            (
                ("--item", "guide-rail"),
                ("--item", "bracket"),
            ),
        )

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
