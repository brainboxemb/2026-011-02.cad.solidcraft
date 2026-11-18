"""Regression contract for the Bolted Flange circular pattern."""

import unittest
from pathlib import Path

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/basic/bolted_flange/scpf/model.py"


class BoltedFlangeTests(unittest.TestCase):
    def setUp(self):
        self.commands = run_script(MODEL)["commands"]

    def test_uses_one_seed_cut_and_one_native_circular_pattern(self):
        names = [row["command"] for row in self.commands]
        self.assertEqual(names.count("sketch.create"), 1)
        self.assertEqual(names.count("sketch.circle.center"), 1)
        self.assertEqual(names.count("solid.extrude"), 1)
        self.assertEqual(names.count("solid.pattern.circular"), 1)
        self.assertEqual(names.count("solid.hole"), 1)

        pattern = next(
            row["params"]
            for row in self.commands
            if row["command"] == "solid.pattern.circular"
        )
        self.assertEqual(
            pattern,
            {
                "features": ["BoltHole"],
                "axis": "Z",
                "count": "bolts",
                "alignment": "right",
                "reversed": False,
            },
        )

    def test_seed_circle_uses_pcd_parameter(self):
        circle = next(
            row["params"]
            for row in self.commands
            if row["command"] == "sketch.circle.center"
        )
        self.assertEqual(circle["center"], ["(pcd / 2)", 0.0])
        self.assertEqual(circle["diameter"], 9)

    def test_bolts_and_pcd_are_native_parameters(self):
        parameters = {
            row["params"]["name"]: row["params"]
            for row in self.commands
            if row["command"] == "parameters.add"
        }
        self.assertEqual(parameters["bolts"]["expression"], "6")
        self.assertEqual(parameters["bolts"]["unit"], "")
        self.assertEqual(parameters["pcd"]["expression"], "70")
        self.assertEqual(parameters["pcd"]["unit"], "mm")

    def test_no_python_expansion_of_bolt_coordinates(self):
        source = MODEL.read_text(encoding="utf-8")
        self.assertNotIn("for index in range", source)
        self.assertNotIn("sin(", source)
        self.assertNotIn("cos(", source)


if __name__ == "__main__":
    unittest.main()
