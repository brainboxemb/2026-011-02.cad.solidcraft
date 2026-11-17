"""Regression checks for the Simple MFT + GuideRail assembly."""
from pathlib import Path
import unittest

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
MODEL = (
    ROOT
    / "models"
    / "advanced"
    / "simple_mft"
    / "scpf"
    / "assemblies"
    / "guide_rail.py"
)


def of(commands, kind):
    return [
        command["params"]
        for command in commands
        if command["command"] == kind
    ]


class SimpleMFTAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.commands = run_script(MODEL)["commands"]

    def test_reuses_worktop_and_guide_rail_components(self):
        components = [params["name"] for params in of(self.commands, "component.create")]
        self.assertEqual(components.count("SimpleMFT"), 1)
        self.assertEqual(components.count("GuideRail"), 1)

    def test_shared_parent_parameters_drive_worktop_and_rail(self):
        parameter_names = {
            params["name"] for params in of(self.commands, "parameters.add")
        }
        self.assertIn("worktop_thickness", parameter_names)
        self.assertIn("guide_rail_length", parameter_names)

        board = next(params for params in of(self.commands, "solid.box"))
        self.assertEqual(board["height"], "worktop_thickness")

        rail = next(
            params
            for params in of(self.commands, "solid.extrude")
            if params.get("name") == "Guide rail profile - festool"
        )
        self.assertEqual(rail["distance"], "guide_rail_length")
        self.assertEqual(rail["direction"], "symmetric")

    def test_assembly_centres_rail_on_x_and_places_it_on_worktop_top(self):
        rail_move = next(
            params
            for params in of(self.commands, "occurrence.move")
            if str(params["occurrence"]).startswith("$guiderail")
        )
        self.assertAlmostEqual(float(rail_move["translate"][0]), -92.1)
        self.assertEqual(rail_move["translate"][1], 0.0)
        self.assertIn("worktop_thickness", str(rail_move["translate"][2]))
        self.assertNotIn("matrix", rail_move)
        self.assertNotIn("to", rail_move)


if __name__ == "__main__":
    unittest.main()
