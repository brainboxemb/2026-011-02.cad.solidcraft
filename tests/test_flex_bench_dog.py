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

        self.assertEqual(names.count("solid.cylinder"), 4)
        self.assertEqual(names.count("solid.box"), 4)
        self.assertEqual(names.count("solid.fillet"), 1)
        self.assertEqual(names.count("solid.chamfer"), 1)
        self.assertFalse(any(name.startswith("sketch.") for name in names))
        self.assertFalse(any(name == "solid.hole" for name in names))

    def test_native_parameters_are_fit_dimensions(self):
        commands = run_script(MODEL)["commands"]
        params = {
            row["params"]["name"]: row["params"]["expression"]
            for row in commands
            if row["command"] == "parameters.add"
        }
        self.assertEqual(
            params,
            {
                "hole_diameter": "20",
                "interference": "0.2",
                "rim_diameter": "24",
                "slot_width": "1.5",
            },
        )

    def test_functional_orientation_and_flex_tip(self):
        commands = run_script(MODEL)["commands"]
        cylinders = [
            row["params"] for row in commands
            if row["command"] == "solid.cylinder"
        ]

        self.assertEqual(cylinders[0]["base"], [0, 0, 0])
        self.assertEqual(cylinders[0]["height"], 3)
        self.assertEqual(cylinders[1]["base"], [0, 0, 3])
        self.assertEqual(cylinders[1]["height"], 17)
        self.assertEqual(cylinders[2]["base"], [0, 0, -18])
        self.assertEqual(cylinders[2]["height"], 18)
        self.assertEqual(cylinders[3]["base"], [0, 0, -18])
        self.assertEqual(cylinders[3]["height"], 2)
        self.assertIn(
            cylinders[3]["diameter"],
            ("hole_diameter + interference", "hole_diameter + (interference)"),
        )

    def test_cross_slots_leave_four_mm_flex_root(self):
        commands = run_script(MODEL)["commands"]
        boxes = [
            row["params"] for row in commands
            if row["command"] == "solid.box"
        ]
        slots = boxes[:2]
        self.assertEqual(slots[0]["height"], 14)
        self.assertEqual(slots[1]["height"], 14)
        self.assertEqual(slots[0]["corner"][2], -18)
        self.assertEqual(slots[1]["corner"][2], -18)
        self.assertEqual(slots[0]["width"], "slot_width")
        self.assertEqual(slots[1]["length"], "slot_width")

    def test_top_finish_and_logo_are_present(self):
        commands = run_script(MODEL)["commands"]

        fillet = next(row["params"] for row in commands if row["command"] == "solid.fillet")
        chamfer = next(row["params"] for row in commands if row["command"] == "solid.chamfer")
        self.assertEqual(fillet["radius"], 1.0)
        self.assertEqual(chamfer["distance"], 0.6)

        boxes = [
            row["params"] for row in commands
            if row["command"] == "solid.box"
        ]
        logo_outer, logo_inner = boxes[2], boxes[3]
        self.assertEqual((logo_outer["length"], logo_outer["width"], logo_outer["height"]), (8, 8, 0.6))
        self.assertEqual((logo_inner["length"], logo_inner["width"], logo_inner["height"]), (5, 5, 0.6))


if __name__ == "__main__":
    unittest.main()
