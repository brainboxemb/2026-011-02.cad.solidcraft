"""Incremental site generation contracts."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import COMMAND_SOURCES, MODELS, model_build_path  # noqa: E402
from output_store import input_fingerprint  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "build_results",
    CI / "build-results.py",
)
build_results = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_results)


class IncrementalSiteGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.generated = self.root / "generated"
        self.store = self.root / "stable"
        self.site = self.root / "site"

        for slug in MODELS:
            target = self.generated / slug / "scpf"
            target.mkdir(parents=True)
            (target / "solidcraft.json").write_text(
                json.dumps({"commands": []}),
                encoding="utf-8",
            )
        for slug in COMMAND_SOURCES:
            target = self.generated / slug / "scpc"
            target.mkdir(parents=True, exist_ok=True)
            (target / "solidcraft.json").write_text(
                json.dumps({"commands": []}),
                encoding="utf-8",
            )

    def tearDown(self):
        self.temp.cleanup()

    def make_verified_store_model(self, slug="bolted-flange"):
        root = self.store / model_build_path(slug)
        native = root / "native"
        generated = root / "generated" / "scpf"
        native.mkdir(parents=True)
        generated.mkdir(parents=True)

        (native / "model.png").write_bytes(b"png")
        with zipfile.ZipFile(native / "model.sc", "w") as archive:
            archive.writestr(
                "document.json",
                json.dumps({"format": "solidcraft/1"}),
            )
            archive.writestr(
                "container.json",
                json.dumps({"format": "solidcraft-container/1"}),
            )

        (generated / "solidcraft.json").write_text(
            json.dumps({"commands": []}),
            encoding="utf-8",
        )
        verification = {
            "schema": 1,
            "model": slug,
            "source_commit": "1" * 40,
            "scpf_commit": "2" * 40,
            "scpf_release": "0.10.0",
            "scpc_commit": "3" * 40,
            "solidcraft_version": "0.42.0",
            "workflow_run": "123",
            "verified": True,
            "native_file_format": "solidcraft/1",
            "input_fingerprint": input_fingerprint(slug),
        }
        (root / "verification.json").write_text(
            json.dumps(verification),
            encoding="utf-8",
        )
        return verification

    def build(self):
        build_results.build(
            self.site,
            "a" * 40,
            generated_root=self.generated,
            stable_store=self.store,
        )

    def test_matching_stable_model_keeps_its_own_verification(self):
        expected = self.make_verified_store_model()
        self.build()

        page_verification = json.loads(
            (
                self.site
                / "models/bolted-flange/verification.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(page_verification, expected)

        catalog = json.loads(
            (self.site / "provenance.json").read_text(encoding="utf-8")
        )
        self.assertEqual(catalog["schema"], 2)
        self.assertEqual(
            catalog["models"]["bolted-flange"],
            expected,
        )
        self.assertIn(
            "Native verified · stored build",
            (
                self.site / "models/bolted-flange/index.html"
            ).read_text(encoding="utf-8"),
        )

    def test_stale_input_fingerprint_disables_stored_native_output(self):
        self.make_verified_store_model()
        manifest = self.store / model_build_path("bolted-flange") / "verification.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["input_fingerprint"] = "0" * 64
        manifest.write_text(json.dumps(data), encoding="utf-8")

        self.build()
        catalog = json.loads(
            (self.site / "provenance.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("bolted-flange", catalog["models"])
        self.assertFalse(
            (
                self.site
                / "models/bolted-flange/verification.json"
            ).exists()
        )

    def test_category_pages_list_all_models_and_home_honours_featured(self):
        original = MODELS["bolted-flange"].get("featured")
        had_key = "featured" in MODELS["bolted-flange"]
        try:
            MODELS["bolted-flange"]["featured"] = False
            self.build()
        finally:
            if had_key:
                MODELS["bolted-flange"]["featured"] = original
            else:
                MODELS["bolted-flange"].pop("featured", None)

        home = (self.site / "index.html").read_text(encoding="utf-8")
        basic = (
            self.site / "models/basic/index.html"
        ).read_text(encoding="utf-8")
        self.assertNotIn('href="models/bolted-flange/"', home)
        self.assertIn('href="../bolted-flange/"', basic)

        for section in ("basic", "components", "advanced"):
            self.assertTrue(
                (self.site / "models" / section / "index.html").is_file()
            )


if __name__ == "__main__":
    unittest.main()
