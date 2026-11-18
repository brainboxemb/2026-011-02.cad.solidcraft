"""Tests for the immutable CAD CI toolchain image contract."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts" / "ci" / "cad_image.py"
    spec = importlib.util.spec_from_file_location("cad_image", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CadImageTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_metadata_uses_exact_repository_pins(self):
        data = self.module.metadata("BrainboxEmb/2026-011-02.cad.solidcraft")
        self.assertTrue(data["reference"].startswith(
            "ghcr.io/brainboxemb/2026-011-02.cad.solidcraft/cad-ci:toolchain-"
        ))
        self.assertRegex(data["scpf_sha"], r"^[0-9a-f]{40}$")
        self.assertRegex(data["scpc_sha"], r"^[0-9a-f]{40}$")
        self.assertEqual(data["solidcraft"], "0.42.0")
        self.assertNotIn("latest", data["reference"])

    def test_image_id_changes_for_toolchain_inputs(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            dockerfile = root / "docker" / "cad" / "Dockerfile"
            toolchain = root / "ci" / "toolchain.json"
            dependencies = root / "dependencies.repos"
            resolver = root / "scripts" / "ci" / "cad_image.py"
            for path, content in (
                (dockerfile, "FROM test\n"),
                (toolchain, '{"schema":1,"python_image":"python:3.12","solidcraft":"0.42.0"}\n'),
                (dependencies, "pins\n"),
                (resolver, "resolver\n"),
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")

            with patch.object(self.module, "ROOT", root), \
                 patch.object(self.module, "DOCKERFILE", dockerfile), \
                 patch.object(self.module, "TOOLCHAIN", toolchain), \
                 patch.object(self.module, "DEPENDENCIES", dependencies), \
                 patch.object(self.module, "SELF", resolver):
                first = self.module.image_id()
                dependencies.write_text("new pins\n", encoding="utf-8")
                second = self.module.image_id()

            self.assertNotEqual(first, second)

    def test_model_source_is_not_an_image_identity_input(self):
        workflow = (ROOT / ".github" / "workflows" / "image.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn('"dependencies.repos"', workflow)
        self.assertIn('"ci/toolchain.json"', workflow)
        self.assertIn('"docker/cad/**"', workflow)
        self.assertNotIn('"models/**"', workflow)

    def test_image_workflow_smokes_real_native_plate(self):
        workflow = (ROOT / ".github" / "workflows" / "image.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("models/basic/plate/scpf/model.py", workflow)
        self.assertIn("python -m scpf.headless", workflow)
        self.assertIn("solidcraft-cli eval", workflow)
        self.assertIn("docker/build-push-action@v6", workflow)


if __name__ == "__main__":
    unittest.main()
