"""Tests for CAD-native fingerprints and temporary candidate output."""

from pathlib import Path
import json
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import model_build_path, verification_input_paths  # noqa: E402
from output_store import input_fingerprint, prepare_candidate  # noqa: E402


class OutputStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.native = self.root / "native"
        self.generated = self.root / "generated"
        self.candidate = self.root / "candidate"

    def tearDown(self):
        self.temp.cleanup()

    def make_model_output(self, slug: str, marker: str) -> None:
        """Create one small native/generated result for candidate tests."""

        native = self.native / slug
        native.mkdir(parents=True)
        with zipfile.ZipFile(native / "model.sc", "w") as archive:
            archive.writestr(
                "document.json",
                json.dumps({"format": "solidcraft/57"}),
            )
            archive.writestr(
                "container.json",
                json.dumps({"format": "solidcraft-container/1"}),
            )
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

    def prepare(self, models) -> None:
        """Run candidate preparation with stable test metadata."""

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

    def test_verification_fingerprint_ignores_model_root_metadata(self):
        slug = "hub75-wood-frame"
        first = input_fingerprint(slug)
        readme = ROOT / "models/advanced/hub75_wood_frame/README.md"
        check = ROOT / "models/advanced/hub75_wood_frame/check.py"
        originals = {path: path.read_bytes() for path in (readme, check)}
        try:
            readme.write_bytes(originals[readme] + b"\n<!-- probe -->\n")
            check.write_bytes(originals[check] + b"\n# probe\n")
            self.assertEqual(input_fingerprint(slug), first)
        finally:
            for path, content in originals.items():
                path.write_bytes(content)

    def test_verification_paths_exclude_page_metadata(self):
        paths = verification_input_paths("hub75-wood-frame")
        self.assertNotIn(
            "models/advanced/hub75_wood_frame/README.md",
            paths,
        )
        self.assertNotIn(
            "models/advanced/hub75_wood_frame/check.py",
            paths,
        )
        self.assertIn(
            "models/advanced/hub75_wood_frame/scpf/model.py",
            paths,
        )

    def test_prepare_candidate_writes_verified_native_handoff(self):
        self.make_model_output("bolted-flange", "new")
        self.prepare(("bolted-flange",))

        root = self.candidate / model_build_path("bolted-flange")
        verification = json.loads(
            (root / "verification.json").read_text(encoding="utf-8")
        )
        self.assertEqual(verification["model"], "bolted-flange")
        self.assertEqual(verification["source_commit"], "cad123")
        self.assertEqual(verification["scpf_commit"], "forge123")
        self.assertEqual(verification["solidcraft_version"], "0.42.0")
        self.assertEqual(
            verification["toolchain_image"],
            "ghcr.io/brainboxemb/cad-ci:toolchain-test",
        )
        self.assertEqual(verification["native_file_format"], "solidcraft/57")
        self.assertEqual(
            verification["input_fingerprint"],
            input_fingerprint("bolted-flange"),
        )
        self.assertTrue((root / "native/model.sc").is_file())
        self.assertTrue((root / "generated/scpf/solidcraft.json").is_file())


if __name__ == "__main__":
    unittest.main()
