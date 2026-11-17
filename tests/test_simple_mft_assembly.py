"""Regression checks for the Simple MFT assembly."""
import unittest
from pathlib import Path

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/advanced/simple_mft_assembly/scpf/model.py"


class SimpleMFTAssemblyTests(unittest.TestCase):
    def setUp(self):
        self.commands = run_script(MODEL)["commands"]

    def of(self, kind):
        return [
            command["params"]
            for command in self.commands
            if command["command"] == kind
        ]

    def test_reuses_one_guide_rail_component(self):
        components = self.of("component.create")
        self.assertEqual(len(components), 1)
        self.assertEqual(components[0]["name"], "GuideRail")

        self.assertEqual(len(self.of("occurrence.copy")), 0)
        self.assertEqual(len(self.of("occurrence.move")), 1)

    def test_guide_rail_occurrence_uses_1080_mm_length(self):
        length_parameters = [
            params
            for params in self.of("parameters.add")
            if params["name"].endswith("_length")
        ]
        self.assertEqual(len(length_parameters), 1)
        self.assertEqual(length_parameters[0]["expression"], "1080")

        rail_extrude = next(
            params
            for params in self.of("solid.extrude")
            if params.get("distance") == length_parameters[0]["name"]
        )
        self.assertTrue(rail_extrude["symmetric"])

    def test_assembly_owns_centered_rail_placement(self):
        placement = self.of("occurrence.move")[0]
        self.assertEqual(
            placement["translate"],
            [-92.1, 0.0, 18.0],
        )
        self.assertNotIn("matrix", placement)
        self.assertNotIn("to", placement)

    def test_worktop_geometry_is_reused_unchanged(self):
        names = [command["command"] for command in self.commands]
        self.assertEqual(names.count("solid.box"), 1)
        self.assertEqual(names.count("solid.chamfer"), 1)
        self.assertEqual(names.count("sketch.circle.center"), 1)
        self.assertEqual(names.count("sketch.slot.center_to_center"), 1)
        self.assertEqual(names.count("sketch.pattern.rectangular"), 2)
        self.assertEqual(names.count("sketch.mirror"), 3)


if __name__ == "__main__":
    unittest.main()
