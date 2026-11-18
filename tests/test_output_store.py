"""Staging and stable model-output contracts."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import MODELS  # noqa: E402
from output_store import (  # noqa: E402
    input_fingerprint,
    migrate_legacy_pages,
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
                / "models/bolted-flange/verification.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(verification["model"], "bolted-flange")
        self.assertEqual(verification["source_commit"], "cad123")
        self.assertEqual(verification["scpf_commit"], "forge123")
        self.assertEqual(verification["solidcraft_version"], "0.42.0")
        self.assertEqual(
            verification["input_fingerprint"],
            input_fingerprint("bolted-flange"),
        )
        self.assertTrue(verification["verified"])

    def test_stable_promotion_replaces_only_selected_model(self):
        old_a = self.store / "stable/models/bolted-flange"
        old_b = self.store / "stable/models/bracket"
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
            (self.store / "stable/models/bolted-flange/old.txt").exists()
        )
        self.assertEqual(
            (
                self.store
                / "stable/models/bolted-flange/native/model.sc"
            ).read_text(encoding="utf-8"),
            "new flange",
        )
        self.assertEqual(
            (
                self.store
                / "stable/models/bracket/old.txt"
            ).read_text(encoding="utf-8"),
            "keep bracket",
        )

    def test_preview_promotion_never_changes_stable(self):
        stable = self.store / "stable/models/bolted-flange"
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
                / "previews/pr-129/models/bolted-flange/native/model.sc"
            ).read_text(encoding="utf-8"),
            "preview",
        )

    def test_incomplete_candidate_changes_nothing(self):
        stable_a = self.store / "stable/models/bolted-flange"
        stable_b = self.store / "stable/models/bracket"
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
        known = self.store / "stable/models/bolted-flange"
        removed = self.store / "stable/models/retired-model"
        known.mkdir(parents=True)
        removed.mkdir(parents=True)

        self.assertEqual(
            prune_removed_models(self.store),
            ("retired-model",),
        )
        self.assertTrue(known.is_dir())
        self.assertFalse(removed.exists())

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
                    / "stable/models"
                    / slug
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
        self.assertFalse((self.store / "stable").exists())

    def test_preview_key_is_safe_and_stable(self):
        self.assertEqual(safe_preview_key("PR 129 / test"), "pr-129-test")
        with self.assertRaises(ValueError):
            safe_preview_key("///")


if __name__ == "__main__":
    unittest.main()
