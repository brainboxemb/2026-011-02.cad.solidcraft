"""Regression checks for the Craftmaker-inspired Simple MFT worktop."""

import unittest
from pathlib import Path

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/advanced/simple_mft/scpf/model.py"


class SimpleMFTTests(unittest.TestCase):
    def setUp(self):
        self.commands = run_script(MODEL)["commands"]
        self.names = [command["command"] for command in self.commands]

    def test_plate_uses_polygon_and_one_native_two_direction_hole_pattern(self):
        self.assertEqual(self.names.count("sketch.polygon"), 1)
        self.assertEqual(self.names.count("sketch.circle.center"), 1)
        self.assertEqual(self.names.count("solid.pattern.rectangular"), 1)

        hole_pattern = next(
            command["params"]
            for command in self.commands
            if command["command"] == "solid.pattern.rectangular"
        )
        self.assertEqual(hole_pattern["features"], ["Dog hole"])
        self.assertEqual(hole_pattern["count1"], 9)
        self.assertEqual(hole_pattern["spacing1"], "hole_pitch")
        self.assertEqual(hole_pattern["count2"], 7)
        self.assertEqual(hole_pattern["spacing2"], "hole_pitch")

    def test_slots_connect_three_diagonal_grid_positions(self):
        slots = [
            command["params"]
            for command in self.commands
            if command["command"] == "sketch.slot.center_to_center"
        ]
        self.assertEqual(len(slots), 4)
        self.assertTrue(all(slot["width"] == 24.0 for slot in slots))

        expected = {
            ((76.0, 76.0), (228.0, 228.0)),
            ((-76.0, 76.0), (-228.0, 228.0)),
            ((-76.0, -76.0), (-228.0, -228.0)),
            ((76.0, -76.0), (228.0, -228.0)),
        }
        actual = {
            (tuple(slot["p0"]), tuple(slot["p1"]))
            for slot in slots
        }
        self.assertEqual(actual, expected)
        self.assertNotIn("sketch.slot.overall", self.names)

    def test_model_keeps_reference_estimates_explicit(self):
        source = MODEL.read_text(encoding="utf-8")
        self.assertIn("hole_pitch = 76.0", source)
        self.assertIn("COLUMNS = 9", source)
        self.assertIn("ROWS = 7", source)
        self.assertIn("SLOT_WIDTH = 24.0", source)
        self.assertIn("SLOT_START_INDEX = 1", source)
        self.assertIn("SLOT_END_INDEX = 3", source)
        self.assertNotIn("SLOT_LENGTH = 75.0", source)


if __name__ == "__main__":
    unittest.main()
