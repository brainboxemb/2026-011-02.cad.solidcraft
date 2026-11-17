"""Regression checks for the Craftmaker-inspired Simple MFT worktop."""

import math
import unittest
from pathlib import Path

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/advanced/simple_mft/scpf/model.py"


class SimpleMFTTests(unittest.TestCase):
    def setUp(self):
        self.commands = run_script(MODEL)["commands"]
        self.names = [command["command"] for command in self.commands]

    def test_plate_keeps_rectangular_base_for_native_top_anchors(self):
        self.assertEqual(self.names.count("solid.box"), 1)
        self.assertEqual(self.names.count("solid.chamfer"), 1)
        self.assertEqual(self.names.count("sketch.polygon"), 0)
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

    def test_slots_match_photo_based_two_ring_pattern(self):
        slots = [
            command["params"]
            for command in self.commands
            if command["command"] == "sketch.slot.center_to_center"
        ]
        self.assertEqual(len(slots), 8)
        self.assertTrue(all(slot["width"] == 24.0 for slot in slots))
        self.assertNotIn("sketch.slot.overall", self.names)

        delta = 80.0 / math.sqrt(2)
        expected = set()
        for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
            expected.add((
                (sx * 76.0, sy * 76.0),
                (sx * (76.0 + delta), sy * (76.0 + delta)),
            ))
            expected.add((
                (sx * (228.0 - delta), sy * (228.0 - delta)),
                (sx * 228.0, sy * 228.0),
            ))

        actual = {
            (tuple(slot["p0"]), tuple(slot["p1"]))
            for slot in slots
        }
        for p0, p1 in expected:
            self.assertTrue(any(
                all(abs(a - b) < 1e-9 for a, b in zip(p0, q0))
                and all(abs(a - b) < 1e-9 for a, b in zip(p1, q1))
                for q0, q1 in actual
            ))

    def test_middle_diagonal_ring_remains_clear(self):
        slots = [
            command["params"]
            for command in self.commands
            if command["command"] == "sketch.slot.center_to_center"
        ]
        middle = {(sx * 152.0, sy * 152.0)
                  for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1))}
        endpoints = {
            tuple(point)
            for slot in slots
            for point in (slot["p0"], slot["p1"])
        }
        self.assertTrue(middle.isdisjoint(endpoints))

    def test_model_keeps_measured_estimates_explicit(self):
        source = MODEL.read_text(encoding="utf-8")
        self.assertIn("hole_pitch = 76.0", source)
        self.assertIn("COLUMNS = 9", source)
        self.assertIn("ROWS = 7", source)
        self.assertIn("SLOT_WIDTH = 24.0", source)
        self.assertIn("SLOT_CENTER_DISTANCE = 80.0", source)
        self.assertNotIn("SLOT_LENGTH = 75.0", source)


if __name__ == "__main__":
    unittest.main()
