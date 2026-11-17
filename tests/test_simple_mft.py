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

    def test_plate_uses_two_compact_associative_sketches(self):
        self.assertEqual(self.names.count("solid.box"), 1)
        self.assertEqual(self.names.count("solid.chamfer"), 1)
        self.assertEqual(self.names.count("sketch.polygon"), 0)

        self.assertEqual(self.names.count("sketch.create"), 2)
        self.assertEqual(self.names.count("sketch.finish"), 2)
        self.assertEqual(self.names.count("solid.extrude"), 2)

        # One Circle seed drives the complete 9 x 7 dog-hole grid.
        self.assertEqual(self.names.count("sketch.circle.center"), 1)
        # One Slot seed drives all eight clamp slots.
        self.assertEqual(self.names.count("sketch.slot.center_to_center"), 1)

        # One dog-hole pattern plus one Slot pattern.
        self.assertEqual(self.names.count("sketch.pattern.rectangular"), 2)
        # Only the Slot sketch needs mirrors.
        self.assertEqual(self.names.count("sketch.mirror"), 3)

        self.assertNotIn("solid.pattern.rectangular", self.names)
        self.assertNotIn("sketch.slot.overall", self.names)

    def test_dog_holes_use_one_complete_pattern_and_selective_cut(self):
        circle = next(
            command
            for command in self.commands
            if command["command"] == "sketch.circle.center"
        )
        self.assertEqual(circle["params"]["diameter"], "hole_diameter")
        self.assertIn("bind", circle)

        pattern = next(
            command
            for command in self.commands
            if command["command"] == "sketch.pattern.rectangular"
        )
        self.assertEqual(pattern["params"]["count"], 9)
        self.assertEqual(pattern["params"]["count2"], 7)
        self.assertEqual(pattern["params"]["spacing"], "hole_pitch")
        self.assertEqual(pattern["params"]["spacing2"], "hole_pitch")
        self.assertEqual(pattern["params"]["dir"], [1.0, 0.0])
        self.assertEqual(pattern["params"]["dir2"], [0.0, 1.0])

        dog_cut = next(
            command
            for command in self.commands
            if command["command"] == "solid.extrude"
            and command["params"].get("name") == "Dog holes"
        )
        picks = [tuple(item["point"]) for item in dog_cut["params"]["profiles"]]
        self.assertTrue(dog_cut["params"]["exact_regions"])
        self.assertEqual(len(picks), 59)
        self.assertEqual(len(set(picks)), 59)

        excluded = {
            (-152.0, -152.0),
            (-152.0, 152.0),
            (152.0, -152.0),
            (152.0, 152.0),
        }
        self.assertTrue(excluded.isdisjoint(picks))
        self.assertIn((0.0, 0.0), picks)
        self.assertIn((-304.0, -228.0), picks)
        self.assertIn((304.0, 228.0), picks)

    def test_slots_use_one_seed_pattern_and_three_mirrors(self):
        slot = next(
            command
            for command in self.commands
            if command["command"] == "sketch.slot.center_to_center"
        )
        self.assertEqual(slot["params"]["p0"], [76.0, 76.0])

        delta = 80.0 / math.sqrt(2)
        self.assertAlmostEqual(slot["params"]["p1"][0], 76.0 + delta)
        self.assertAlmostEqual(slot["params"]["p1"][1], 76.0 + delta)
        self.assertEqual(slot["params"]["width"], 24.0)
        self.assertIn("bind", slot)

        patterns = [
            command
            for command in self.commands
            if command["command"] == "sketch.pattern.rectangular"
        ]
        slot_pattern = patterns[-1]
        self.assertEqual(slot_pattern["params"]["count"], 2)
        self.assertEqual(slot_pattern["params"]["dir"], [1.0, 1.0])

        expected_spacing = 2 * math.sqrt(2) * 76.0 - 80.0
        self.assertAlmostEqual(
            slot_pattern["params"]["spacing"],
            expected_spacing,
        )

        mirrors = [
            command
            for command in self.commands
            if command["command"] == "sketch.mirror"
        ]
        self.assertEqual(
            [command["params"]["line"] for command in mirrors],
            ["y", "x", "x"],
        )

    def test_corner_chamfer_uses_named_vertical_edges(self):
        chamfer = next(
            command
            for command in self.commands
            if command["command"] == "solid.chamfer"
        )
        self.assertEqual(chamfer["params"]["distance"], "corner_chamfer")
        self.assertEqual(len(chamfer["params"]["edges"]), 4)

        source = MODEL.read_text(encoding="utf-8")
        self.assertIn("edges=Edges.VERTICAL", source)
        self.assertNotIn("edge_z =", source)

    def test_model_keeps_measured_estimates_explicit(self):
        source = MODEL.read_text(encoding="utf-8")
        self.assertIn("hole_pitch = 76.0", source)
        self.assertIn("COLUMNS = 9", source)
        self.assertIn("ROWS = 7", source)
        self.assertIn("SLOT_WIDTH = 24.0", source)
        self.assertIn("SLOT_CENTER_DISTANCE = 80.0", source)

        self.assertIn(
            'Sketch(name="Dog holes", on=board, parent=Anchor.TOP)',
            source,
        )
        self.assertIn(
            'Sketch(name="Clamp slots", on=board, parent=Anchor.TOP)',
            source,
        )
        self.assertEqual(source.count("Depth.THROUGH_ALL"), 2)
        self.assertIn("profiles=dog_hole_profiles", source)
        self.assertIn("exact_regions=True", source)


if __name__ == "__main__":
    unittest.main()
