"""Focused tests for shared model-root mapping and output lookup."""

from __future__ import annotations

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

import model_item  # noqa: E402


class ModelItemTests(unittest.TestCase):
    def test_shared_roots_expose_all_catalog_members(self):
        self.assertEqual(
            model_item.item_members(ROOT / "models/components/guide_rail"),
            ("guide-rail", "guide-rail-makita"),
        )
        self.assertEqual(
            model_item.item_members(ROOT / "models/advanced/simple_mft"),
            ("simple-mft", "simple-mft-assembly"),
        )

    def test_item_dependencies_are_unique_folder_dependencies(self):
        self.assertEqual(
            model_item.item_dependencies("simple-mft"),
            ("guide-rail",),
        )
        self.assertEqual(
            model_item.item_dependencies("hub75-wood-frame"),
            ("corner-bracket",),
        )
        self.assertEqual(
            model_item.item_dependencies("hub75-display2"),
            ("corner-bracket",),
        )

    def test_current_output_is_preferred_over_stable_fallback(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            current = root / "output/models/plate/scpf/solidcraft.json"
            stable = (
                root
                / "generated-build/main/models/basic/plate/scpf/model"
                / "generated/scpf/solidcraft.json"
            )
            current.parent.mkdir(parents=True)
            stable.parent.mkdir(parents=True)
            current.write_text("current", encoding="utf-8")
            stable.write_text("stable", encoding="utf-8")

            with patch.object(model_item, "ROOT", root):
                path, source = model_item._existing_commands("plate", "scpf")

            self.assertEqual(path, current)
            self.assertEqual(source, "current-run")


if __name__ == "__main__":
    unittest.main()
