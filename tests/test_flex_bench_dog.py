"""Regression checks for the reusable FlexBenchDog component."""

from pathlib import Path
import unittest

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "components" / "flex_bench_dog" / "scpf" / "model.py"


class FlexBenchDogTests(unittest.TestCase):
    def test_passive_flex_geometry_uses_simple_primitives(self):
        commands = run_script(MODEL)["commands"]
        names = [row["command"] for row in commands]

        self.assertEqual(names.count("solid.cylinder"), 3)
        self.assertEqual(names.count("solid.box"), 2)
        self.assertFalse(any(name.startswith("sketch.") for name in names))
        self.assertFalse(any(name == "solid.hole" for name in names))

    def test_default_fit_is_20_mm_hole_plus_point_two_interference(self):
        commands = run_script(MODEL)["commands"]
        params = {
            row["params"]["name"]: row["params"]["expression"]
            for row in commands
            if row["command"] == "parameters.add"
        }

        self.assertEqual(params["hole_diameter"], "20")
        self.assertEqual(params["interference"], "0.2")
        self.assertEqual(params["slot_width"], "1.5")
        self.assertEqual(params["slot_length"], "30")

        cylinders = [
            row["params"] for row in commands
            if row["command"] == "solid.cylinder"
        ]
        self.assertEqual(cylinders[2]["diameter"], "hole_diameter + interference")

    def test_cross_slots_are_two_perpendicular_box_cuts(self):
        commands = run_script(MODEL)["commands"]
        boxes = [
            row["params"] for row in commands
            if row["command"] == "solid.box"
        ]
        self.assertEqual(len(boxes), 2)
        self.assertEqual(boxes[0]["width"], "slot_width")
        self.assertEqual(boxes[1]["length"], "slot_width")


if __name__ == "__main__":
    unittest.main()
