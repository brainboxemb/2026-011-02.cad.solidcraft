"""Regression checks for the reusable FlexBenchDog component."""

from pathlib import Path
import unittest

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models" / "components" / "flex_bench_dog" / "scpf" / "model.py"


class FlexBenchDogTests(unittest.TestCase):
    def test_uses_native_taper_sketch_cuts_and_chamfers(self):
        commands = run_script(MODEL)["commands"]
        names = [row["command"] for row in commands]

        self.assertEqual(names.count("solid.cylinder"), 2)
        self.assertEqual(names.count("solid.cone"), 1)
        self.assertEqual(names.count("sketch.create"), 3)
        self.assertEqual(names.count("sketch.rectangle.two_point"), 2)
        self.assertEqual(names.count("sketch.slot.center_to_center"), 9)
        self.assertEqual(names.count("solid.extrude"), 3)
        self.assertEqual(names.count("solid.fillet"), 0)
        self.assertEqual(names.count("solid.chamfer"), 2)
        self.assertFalse(any(name == "solid.box" for name in names))
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
                "rim_diameter": "22",
                "slot_width": "1.5",
            },
        )

    def test_small_rim_and_twenty_mm_upper_body(self):
        commands = run_script(MODEL)["commands"]
        cylinders = [
            row["params"]
            for row in commands
            if row["command"] == "solid.cylinder"
        ]

        self.assertEqual(len(cylinders), 2)
        self.assertEqual(cylinders[0]["base"], [0, 0, 0])
        self.assertEqual(cylinders[0]["height"], 1.5)
        self.assertEqual(cylinders[0]["diameter"], "rim_diameter")

        self.assertEqual(cylinders[1]["base"], [0, 0, 1.5])
        self.assertEqual(cylinders[1]["height"], 18.5)
        self.assertEqual(cylinders[1]["diameter"], "hole_diameter")

    def test_insert_is_one_full_length_conical_frustum(self):
        commands = run_script(MODEL)["commands"]
        cone = next(
            row["params"]
            for row in commands
            if row["command"] == "solid.cone"
        )

        self.assertEqual(cone["base"], [0, 0, -20])
        self.assertEqual(cone["height"], 20)
        self.assertEqual(cone["axis"], "Z")
        self.assertEqual(cone["top_diameter"], "hole_diameter")
        self.assertIn(
            cone["diameter"],
            (
                "hole_diameter + interference",
                "hole_diameter + (interference)",
            ),
        )

    def test_cross_slots_leave_four_mm_flex_root(self):
        commands = run_script(MODEL)["commands"]
        sketches = [
            row["params"]
            for row in commands
            if row["command"] == "sketch.create"
        ]
        self.assertEqual(
            [row["name"] for row in sketches[:2]],
            ["Flex slot X", "Flex slot Y"],
        )
        self.assertEqual(sketches[0]["plane"]["origin"], [0, 0, -20])
        self.assertEqual(sketches[1]["plane"]["origin"], [0, 0, -20])

        cuts = [
            row["params"]
            for row in commands
            if row["command"] == "solid.extrude"
            and row["params"]["operation"] == "cut"
            and row["params"]["name"] in ("Flex slot X", "Flex slot Y")
        ]
        self.assertEqual(len(cuts), 2)
        self.assertTrue(all(row["distance"] == 16 for row in cuts))

    def test_top_and_bottom_chamfers_have_different_sizes(self):
        commands = run_script(MODEL)["commands"]
        chamfers = [
            row["params"]
            for row in commands
            if row["command"] == "solid.chamfer"
        ]
        self.assertEqual(len(chamfers), 2)
        self.assertEqual(chamfers[0]["distance"], 1.0)
        self.assertEqual(chamfers[1]["distance"], 0.6)

    def test_recessed_logo_is_cube_wireframe_not_filled_square(self):
        commands = run_script(MODEL)["commands"]
        sketches = [
            row["params"]
            for row in commands
            if row["command"] == "sketch.create"
        ]
        self.assertEqual(sketches[-1]["name"], "Top logo")
        self.assertEqual(sketches[-1]["plane"]["origin"], [0, 0, 20])

        logo_slots = [
            row["params"]
            for row in commands
            if row["command"] == "sketch.slot.center_to_center"
        ]
        self.assertEqual(len(logo_slots), 9)
        self.assertTrue(all(row["width"] == 0.6 for row in logo_slots))

        # Six perimeter edges plus three spokes to the cube's centre.
        expected = {
            ((0.0, 4.0), (3.5, 2.0)),
            ((3.5, 2.0), (3.5, -2.0)),
            ((3.5, -2.0), (0.0, -4.0)),
            ((0.0, -4.0), (-3.5, -2.0)),
            ((-3.5, -2.0), (-3.5, 2.0)),
            ((-3.5, 2.0), (0.0, 4.0)),
            ((0.0, 0.0), (0.0, 4.0)),
            ((0.0, 0.0), (3.5, -2.0)),
            ((0.0, 0.0), (-3.5, -2.0)),
        }
        actual = {
            (tuple(row["p0"]), tuple(row["p1"]))
            for row in logo_slots
        }
        self.assertEqual(actual, expected)

        logo_cut = next(
            row["params"]
            for row in commands
            if row["command"] == "solid.extrude"
            and row["params"]["name"] == "Top logo"
        )
        self.assertEqual(logo_cut["operation"], "cut")
        self.assertEqual(logo_cut["distance"], 0.6)
        self.assertEqual(logo_cut["direction"], "negative")


if __name__ == "__main__":
    unittest.main()
