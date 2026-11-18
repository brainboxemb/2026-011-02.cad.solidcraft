"""Regression checks for the reusable FlexBenchDog component."""

from pathlib import Path
import unittest

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "components" / "flex_bench_dog" / "scpf" / "model.py"


class FlexBenchDogTests(unittest.TestCase):
    def test_uses_native_cylinders_sketch_cuts_and_edge_finish(self):
        commands = run_script(MODEL)["commands"]
        names = [row["command"] for row in commands]

        self.assertEqual(names.count("solid.cylinder"), 4)
        self.assertEqual(names.count("sketch.create"), 3)
        self.assertEqual(names.count("sketch.rectangle.two_point"), 3)
        self.assertEqual(names.count("solid.extrude"), 3)
        self.assertEqual(names.count("solid.fillet"), 1)
        self.assertEqual(names.count("solid.chamfer"), 1)
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

    def test_cross_slots_start_at_insert_tip_and_leave_four_mm_root(self):
        commands = run_script(MODEL)["commands"]
        sketches = [
            row["params"]
            for row in commands
            if row["command"] == "sketch.create"
        ]
        self.assertEqual([row["name"] for row in sketches[:2]], ["Flex slot X", "Flex slot Y"])
        self.assertEqual(sketches[0]["origin"], [0, 0, -18])
        self.assertEqual(sketches[1]["origin"], [0, 0, -18])

        cuts = [
            row["params"]
            for row in commands
            if row["command"] == "solid.extrude"
            and row["params"]["operation"] == "cut"
        ]
        self.assertEqual(len(cuts), 2)
        self.assertTrue(all(row["distance"] == 14 for row in cuts))

    def test_top_finish_and_logo_are_present(self):
        commands = run_script(MODEL)["commands"]

        fillet = next(row["params"] for row in commands if row["command"] == "solid.fillet")
        chamfer = next(row["params"] for row in commands if row["command"] == "solid.chamfer")
        self.assertEqual(fillet["radius"], 1.0)
        self.assertEqual(chamfer["distance"], 0.6)

        sketches = [
            row["params"]
            for row in commands
            if row["command"] == "sketch.create"
        ]
        self.assertEqual(sketches[-1]["name"], "Top logo")
        self.assertEqual(sketches[-1]["origin"], [0, 0, 20])

        joins = [
            row["params"]
            for row in commands
            if row["command"] == "solid.extrude"
            and row["params"]["operation"] == "join"
        ]
        self.assertEqual(len(joins), 1)
        self.assertEqual(joins[0]["distance"], 0.6)


if __name__ == "__main__":
    unittest.main()
