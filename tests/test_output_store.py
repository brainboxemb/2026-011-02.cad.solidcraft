"""Candidate and build-branch output contracts."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import MODELS, model_build_path  # noqa: E402
from output_store import (  # noqa: E402
    input_fingerprint,
    migrate_legacy_pages,
    migrate_legacy_store_layout,
    normalize_native_snapshots,
    prepare_candidate,
    promote_candidate,
    prune_removed_models,
    safe_preview_key,
)


class OutputStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.native = self.root / "native"
        self.generated = self.root / "generated"
        self.candidate = self.root / "candidate"
        self.store = self.root / "store"

    def tearDown(self):
        self.temp.cleanup()

    def make_model_output(self, slug, marker):
        native = self.native / slug
        native.mkdir(parents=True)
        (native / "model.sc").write_text(marker, encoding="utf-8")
        (native / "measurements.json").write_text(
            json.dumps({"marker": marker}),
            encoding="utf-8",
        )
        generated = self.generated / slug / "scpf"
        generated.mkdir(parents=True)
        (generated / "solidcraft.json").write_text(
            json.dumps({"commands": [], "marker": marker}),
            encoding="utf-8",
        )

    def prepare(self, models):
        prepare_candidate(
            models=models,
            native_root=self.native,
            generated_root=self.generated,
            out=self.candidate,
            metadata={
                "schema": 1,
                "source_commit": "cad123",
                "scpf_commit": "forge123",
                "scpf_release": "0.10.0",
                "scpc_commit": "cmd123",
                "solidcraft_version": "0.42.0",
                "workflow_run": "99",
                "toolchain_image": "ghcr.io/brainboxemb/cad-ci:toolchain-test",
                "verified": True,
            },
        )

    def test_input_fingerprint_changes_only_with_declared_inputs(self):
        first = input_fingerprint("bolted-flange")
        unrelated = ROOT / "tests" / "_fingerprint_unrelated.tmp"
        try:
            unrelated.write_text("not a model input", encoding="utf-8")
            self.assertEqual(input_fingerprint("bolted-flange"), first)
        finally:
            unrelated.unlink(missing_ok=True)

        source = ROOT / "models/basic/bolted_flange/scpf/model.py"
        original = source.read_bytes()
        try:
            source.write_bytes(original + b"\n# fingerprint probe\n")
            self.assertNotEqual(input_fingerprint("bolted-flange"), first)
        finally:
            source.write_bytes(original)

    def test_prepare_candidate_writes_verification_per_model(self):
        self.make_model_output("bolted-flange", "new")
        self.prepare(("bolted-flange",))

        verification = json.loads(
            (
                self.candidate
                / model_build_path("bolted-flange")
                / "verification.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(verification["model"], "bolted-flange")
        self.assertEqual(verification["source_commit"], "cad123")
        self.assertEqual(verification["scpf_commit"], "forge123")
        self.assertEqual(verification["solidcraft_version"], "0.42.0")
        self.assertEqual(
            verification["toolchain_image"],
            "ghcr.io/brainboxemb/cad-ci:toolchain-test",
        )
        self.assertEqual(
            verification["input_fingerprint"],
            input_fingerprint("bolted-flange"),
        )
        self.assertTrue(verification["verified"])

    def test_stable_promotion_replaces_only_selected_model(self):
        old_a = self.store / "main" / model_build_path("bolted-flange")
        old_b = self.store / "main" / model_build_path("bracket")
        old_a.mkdir(parents=True)
        old_b.mkdir(parents=True)
        (old_a / "old.txt").write_text("old flange", encoding="utf-8")
        (old_b / "old.txt").write_text("keep bracket", encoding="utf-8")

        self.make_model_output("bolted-flange", "new flange")
        self.prepare(("bolted-flange",))
        promote_candidate(
            candidate=self.candidate,
            store=self.store,
            models=("bolted-flange",),
            channel="stable",
        )

        self.assertFalse(
            (self.store / "main" / model_build_path("bolted-flange") / "old.txt").exists()
        )
        self.assertEqual(
            (
                self.store
                / "main"
                / model_build_path("bolted-flange")
                / "native/model.sc"
            ).read_text(encoding="utf-8"),
            "new flange",
        )
        self.assertEqual(
            (
                self.store
                / "main"
                / model_build_path("bracket")
                / "old.txt"
            ).read_text(encoding="utf-8"),
            "keep bracket",
        )

    def test_preview_promotion_never_changes_stable(self):
        stable = self.store / "main" / model_build_path("bolted-flange")
        stable.mkdir(parents=True)
        (stable / "marker.txt").write_text("stable", encoding="utf-8")

        self.make_model_output("bolted-flange", "preview")
        self.prepare(("bolted-flange",))
        promote_candidate(
            candidate=self.candidate,
            store=self.store,
            models=("bolted-flange",),
            channel="preview",
            preview_key="PR 129",
        )

        self.assertEqual(
            (stable / "marker.txt").read_text(encoding="utf-8"),
            "stable",
        )
        self.assertEqual(
            (
                self.store
                / "pr/129"
                / model_build_path("bolted-flange")
                / "native/model.sc"
            ).read_text(encoding="utf-8"),
            "preview",
        )

    def test_incomplete_candidate_changes_nothing(self):
        stable_a = self.store / "main" / model_build_path("bolted-flange")
        stable_b = self.store / "main" / model_build_path("bracket")
        stable_a.mkdir(parents=True)
        stable_b.mkdir(parents=True)
        (stable_a / "marker.txt").write_text("a", encoding="utf-8")
        (stable_b / "marker.txt").write_text("b", encoding="utf-8")

        self.make_model_output("bolted-flange", "candidate a")
        self.prepare(("bolted-flange",))

        with self.assertRaisesRegex(FileNotFoundError, "bracket"):
            promote_candidate(
                candidate=self.candidate,
                store=self.store,
                models=("bolted-flange", "bracket"),
                channel="stable",
            )

        self.assertEqual(
            (stable_a / "marker.txt").read_text(encoding="utf-8"),
            "a",
        )
        self.assertEqual(
            (stable_b / "marker.txt").read_text(encoding="utf-8"),
            "b",
        )

    def test_prune_removes_only_models_missing_from_catalog(self):
        known = self.store / "main" / model_build_path("bolted-flange")
        removed = self.store / "main/models/basic/retired_model"
        known.mkdir(parents=True)
        removed.mkdir(parents=True)
        (known / "verification.json").write_text(
            json.dumps({"model": "bolted-flange", "verified": True}),
            encoding="utf-8",
        )
        (removed / "verification.json").write_text(
            json.dumps({"model": "retired-model", "verified": True}),
            encoding="utf-8",
        )

        self.assertEqual(
            prune_removed_models(self.store),
            ("retired-model",),
        )
        self.assertTrue(known.is_dir())
        self.assertFalse(removed.exists())

    def test_legacy_native_snapshot_is_normalized_to_model_png(self):
        model = (
            self.store
            / "main"
            / model_build_path("bolted-flange")
        )
        native = model / "native"
        native.mkdir(parents=True)
        (model / "verification.json").write_text(
            json.dumps({
                "model": "bolted-flange",
                "verified": True,
                "source_commit": "legacy",
            }),
            encoding="utf-8",
        )
        (native / "native.png").write_bytes(b"legacy-png")

        normalized = normalize_native_snapshots(self.store)

        self.assertEqual(normalized, ("bolted-flange",))
        self.assertFalse((native / "native.png").exists())
        self.assertEqual((native / "model.png").read_bytes(), b"legacy-png")
        verification = json.loads(
            (model / "verification.json").read_text(encoding="utf-8")
        )
        self.assertEqual(verification["source_commit"], "legacy")

    def test_snapshot_normalization_is_idempotent_and_removes_duplicate_legacy_name(self):
        model = (
            self.store
            / "main"
            / model_build_path("plate")
        )
        native = model / "native"
        native.mkdir(parents=True)
        (model / "verification.json").write_text(
            json.dumps({"model": "plate", "verified": True}),
            encoding="utf-8",
        )
        (native / "model.png").write_bytes(b"canonical")
        (native / "native.png").write_bytes(b"legacy")

        normalized = normalize_native_snapshots(self.store)

        self.assertEqual(normalized, ("plate",))
        self.assertEqual((native / "model.png").read_bytes(), b"canonical")
        self.assertFalse((native / "native.png").exists())
        self.assertEqual(normalize_native_snapshots(self.store), ())

    def test_complete_legacy_store_migrates_without_rewriting_verification(self):
        expected = tuple(
            slug for slug, model in MODELS.items()
            if model.get("native")
        )
        for slug in expected:
            source = self.store / "stable/models" / slug
            source.mkdir(parents=True)
            payload = {
                "schema": 1,
                "model": slug,
                "source_commit": f"legacy-{slug}",
                "verified": True,
            }
            (source / "verification.json").write_text(
                json.dumps(payload),
                encoding="utf-8",
            )
            (source / "marker.txt").write_text(slug, encoding="utf-8")

        migrated = migrate_legacy_store_layout(store=self.store)
        self.assertEqual(set(migrated), set(expected))

        for slug in expected:
            target = self.store / "main" / model_build_path(slug)
            self.assertEqual(
                (target / "marker.txt").read_text(encoding="utf-8"),
                slug,
            )
            verification = json.loads(
                (target / "verification.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                verification["source_commit"],
                f"legacy-{slug}",
            )

    def test_complete_legacy_pages_can_bootstrap_stable_store(self):
        pages = self.root / "pages"
        native_models = tuple(
            slug for slug, model in MODELS.items()
            if model.get("native")
        )
        provenance = {
            "source_commit": "1" * 40,
            "scpf_commit": "2" * 40,
            "scpf_release": "0.9.0",
            "scpc_commit": "3" * 40,
            "solidcraft_version": "0.42.0",
            "workflow_run": "123",
            "native_file_format": "solidcraft/57",
            "native_verified_models": list(native_models),
        }
        pages.mkdir()
        (pages / "provenance.json").write_text(
            json.dumps(provenance),
            encoding="utf-8",
        )

        for slug in native_models:
            model = pages / "models" / slug
            model.mkdir(parents=True)
            with zipfile.ZipFile(model / "model.sc", "w") as archive:
                archive.writestr(
                    "document.json",
                    json.dumps({"format": "solidcraft/57"}),
                )
                archive.writestr(
                    "container.json",
                    json.dumps({"format": "solidcraft-container/1"}),
                )
            (model / "solidcraft.json").write_text(
                json.dumps({"commands": []}),
                encoding="utf-8",
            )
            if slug != "csg-cube":
                (model / "native.png").write_bytes(b"png")

        migrated = migrate_legacy_pages(
            pages=pages,
            store=self.store,
        )
        self.assertEqual(set(migrated), set(native_models))

        for slug in native_models:
            verification = json.loads(
                (
                    self.store
                    / "main"
                    / model_build_path(slug)
                    / "verification.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(verification["model"], slug)
            self.assertEqual(
                verification["input_fingerprint"],
                input_fingerprint(slug),
            )
            self.assertTrue(verification["legacy_migrated"])

    def test_partial_legacy_pages_is_rejected_before_bootstrap(self):
        pages = self.root / "pages"
        pages.mkdir()
        (pages / "provenance.json").write_text(
            json.dumps({
                "source_commit": "1" * 40,
                "scpf_commit": "2" * 40,
                "scpf_release": "0.9.0",
                "scpc_commit": "3" * 40,
                "solidcraft_version": "0.42.0",
                "workflow_run": "123",
                "native_file_format": "solidcraft/57",
                "native_verified_models": ["bolted-flange"],
            }),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "not a complete native catalog"):
            migrate_legacy_pages(pages=pages, store=self.store)
        self.assertFalse((self.store / "main").exists())

    def test_preview_key_is_safe_and_stable(self):
        self.assertEqual(safe_preview_key("PR 129 / test"), "pr-129-test")
        with self.assertRaises(ValueError):
            safe_preview_key("///")


if __name__ == "__main__":
    unittest.main()
