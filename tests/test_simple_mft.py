"""Regression checks for the plate-only Simple MFT model."""

import unittest
from pathlib import Path

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/advanced/simple_mft/scpf/model.py"


class SimpleMFTTests(unittest.TestCase):
    def test_plate_uses_one_native_two_direction_mft_pattern(self):
        commands = run_script(MODEL)["commands"]
        names = [command["command"] for command in commands]

        self.assertEqual(names.count("solid.box"), 1)
        self.assertEqual(names.count("sketch.circle.center"), 1)
        self.assertEqual(names.count("solid.extrude"), 1)
        self.assertEqual(names.count("solid.pattern.rectangular"), 1)
        self.assertNotIn("solid.hole", names)
        self.assertNotIn("sketch.rectangle.rounded", names)
        self.assertNotIn("material.assign", names)
        self.assertNotIn("component.create", names)
        self.assertNotIn("occurrence.move", names)

        pattern = next(
            command["params"]
            for command in commands
            if command["command"] == "solid.pattern.rectangular"
        )
        self.assertEqual(pattern["features"], ["Dog hole"])
        self.assertEqual(pattern["dir1"], [1, 0, 0])
        self.assertEqual(pattern["count1"], 7)
        self.assertEqual(pattern["spacing1"], "hole_pitch")
        self.assertEqual(pattern["dir2"], [0, 1, 0])
        self.assertEqual(pattern["count2"], 5)
        self.assertEqual(pattern["spacing2"], "hole_pitch")

        circle = next(
            command["params"]
            for command in commands
            if command["command"] == "sketch.circle.center"
        )
        self.assertEqual(circle["diameter"], "hole_diameter")
        self.assertEqual(
            circle["center"],
            ["(-3 * hole_pitch)", "(-2 * hole_pitch)"],
        )

    def test_model_does_not_reintroduce_rejected_clamp_slots(self):
        source = MODEL.read_text(encoding="utf-8")
        self.assertNotIn("RoundedRectangle2D", source)
        self.assertNotIn("SLOT_CENTERS", source)
        self.assertNotIn("80.0", source)


if __name__ == "__main__":
    unittest.main()
