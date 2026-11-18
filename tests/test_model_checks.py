"""Contracts for model-owned CAD check modules."""

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import MODELS  # noqa: E402
from model_checks import (  # noqa: E402
    check_path,
    extra_snapshots,
    load_check,
    mutations,
    snapshot_camera,
)


class ModelOwnedCheckTests(unittest.TestCase):
    def test_every_present_model_check_imports(self):
        for slug in MODELS:
            with self.subTest(slug=slug):
                path = check_path(slug)
                module = load_check(slug)
                if path.is_file():
                    self.assertIsNotNone(module)
                else:
                    self.assertIsNone(module)

    def test_optional_model_check_metadata_has_stable_shapes(self):
        for slug in MODELS:
            with self.subTest(slug=slug):
                self.assertIsInstance(mutations(slug), tuple)
                self.assertIsInstance(extra_snapshots(slug), tuple)
                camera = snapshot_camera(slug)
                self.assertTrue(camera is None or isinstance(camera, dict))


if __name__ == "__main__":
    unittest.main()
