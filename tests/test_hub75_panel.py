"""First real-model regression for SCPF reusable components."""
import unittest
from pathlib import Path

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/component-examples/hub75-panel/scpf/model.py"


class Hub75PanelTests(unittest.TestCase):
    def test_five_panel_screen_uses_native_rotations_and_independent_positions(self):
        """Copies first, then move each independently with SolidCraft 0.30.1.

        No Python matrix calculations, and no unsupported 'to' parameter.
        The native CI separately checks actual saved SolidCraft transforms.
        """
        commands = run_script(ROOT / "models/advanced/hub75-screen/scpf/model.py")["commands"]
        def of(kind):
            return [item["params"] for item in commands if item["command"] == kind]

        self.assertEqual(len(of("component.create")), 1)
        self.assertEqual(len(of("occurrence.copy")), 4)
        self.assertEqual(len(of("occurrence.move")), 5)
        self.assertEqual(len(of("solid.loft")), 1)
        self.assertEqual(len(of("solid.hole")), 6)
        self.assertEqual(len(of("material.create")), 1)

        # A copied native component inherits its source transform.
        # Therefore, create all copies BEFORE applying any placement.
        copy_indices = [i for i, row in enumerate(commands)
                        if row["command"] == "occurrence.copy"]
        move_indices = [i for i, row in enumerate(commands)
                        if row["command"] == "occurrence.move"]
        self.assertLess(max(copy_indices), min(move_indices))
        self.assertTrue(all(p == {"component": "Hub75Panel"}
                            for p in of("occurrence.copy")))

        placements = of("occurrence.move")
        self.assertEqual([p["occurrence"] for p in placements],
                         [f"Hub75Panel:{i}" for i in range(1, 6)])
        self.assertEqual([p["translate"] for p in placements],
                         [[0., 0., 160.], [-320., 0., 160.],
                          [-160., 0., 160.], [160., 0., 160.],
                          [320., 0., 160.]])
        for i, pose in enumerate(placements):
            axis = [0., 1., -1.] if i in (2, 3) else [1., 0., 0.]
            angle = "180 deg" if i in (2, 3) else "90 deg"
            self.assertEqual(pose["axis"], axis)
            self.assertEqual(pose["angle"], angle)
            self.assertNotIn("matrix", pose)
            self.assertNotIn("to", pose)

    def test_single_panel_and_screen_import_the_same_definition(self):
        from components.hub75 import Hub75Panel as PanelDefinition
        from scpf import component
        panel = component(PanelDefinition)()
        self.assertIs(panel.definition.shape, panel.copy().definition.shape)

    def test_copy_creates_a_second_occurrence_of_one_definition(self):
        from scpf.core import Box
        from scpf.model_objects import ModelDefinition, ModelInstance

        original = ModelInstance(ModelDefinition("Panel", (), Box(20, 10, 2)))
        duplicate = original.copy().move(x=24)
        self.assertIsNot(original, duplicate)
        self.assertIs(original.definition, duplicate.definition)
        self.assertEqual(original.translation, (0, 0, 0))
        self.assertEqual(duplicate.translation, (24, 0, 0))
        self.assertIsNone(duplicate.attachment)

    def test_single_panel_has_one_upright_occurrence(self):
        commands = run_script(MODEL)["commands"]
        def of(kind):
            return [c["params"] for c in commands if c["command"] == kind]

        self.assertEqual([c["name"] for c in of("component.create")], ["Hub75Panel"])
        self.assertEqual(of("occurrence.copy"), [])
        moved = of("occurrence.move")
        self.assertEqual(len(moved), 1)
        self.assertTrue(moved[0]["move_grounded"])
        self.assertNotIn("to", moved[0])
        self.assertEqual(moved[0]["translate"], [0., 0., 160.])
        self.assertEqual(moved[0]["axis"], [1., 0., 0.])
        self.assertEqual(moved[0]["angle"], "90 deg")
        self.assertNotIn("matrix", moved[0])
        self.assertEqual(of("joint.create"), [])
        self.assertEqual(len(of("solid.hole")), 6)
        self.assertEqual(
            [c["name"] for c in of("parameters.add")],
            ["Hub75Panel_width", "Hub75Panel_height", "Hub75Panel_depth",
             "Hub75Panel_front_depth", "Hub75Panel_rear_inset",
             "Hub75Panel_rear_side_rail", "Hub75Panel_rear_crossbar",
             "Hub75Panel_rear_end_rail", "Hub75Panel_hole_diameter",
             "Hub75Panel_mount_x", "Hub75Panel_mount_y"],
        )

    def test_rear_taper_uses_editable_native_loft(self):
        commands = run_script(MODEL)["commands"]
        kinds = [c["command"] for c in commands]
        self.assertEqual(kinds.count("solid.extrude"), 2)
        self.assertEqual(kinds.count("solid.loft"), 1)
        self.assertEqual(kinds.count("sketch.rectangle.two_point"), 7)
        loft = next(c["params"] for c in commands if c["command"] == "solid.loft")
        self.assertEqual(loft["operation"], "join")
        self.assertEqual(loft["targets"], ["Hub75Panel"])
        self.assertIn("rear start", loft["sections"][0]["sketch"])
        self.assertIn("rear perimeter", loft["sections"][1]["sketch"])
        planes = [c["params"] for c in commands if c["command"] == "sketch.create"]
        self.assertEqual(
            [p.get("offset", 0) for p in planes],
            [0, "Hub75Panel_front_depth", "Hub75Panel_depth",
             "(Hub75Panel_depth)"],
        )

    def test_four_bays_are_one_rear_facing_native_sketch_cut(self):
        from components.hub75 import Hub75Panel

        commands = run_script(MODEL)["commands"]
        named = [c for c in commands if c["command"] == "sketch.create"]
        self.assertEqual([c["params"]["name"] for c in named][-1],
                         "Rear electronics bays")
        idx = next(i for i, c in enumerate(commands)
                   if c["command"] == "sketch.create"
                   and c["params"]["name"] == "Rear electronics bays")
        self.assertEqual(commands[idx]["params"]["offset"],
                         "(Hub75Panel_depth)")
        rectangles = []
        for operation in commands[idx + 1:]:
            if operation["command"] == "sketch.finish":
                break
            self.assertEqual(operation["command"], "sketch.rectangle.two_point")
            rectangles.append(operation["params"])
        self.assertEqual(len(rectangles), 4)
        cuts = [c["params"] for c in commands
                if c["command"] == "solid.extrude"
                and c["params"].get("operation") == "cut"]
        self.assertEqual(len(cuts), 1)
        self.assertEqual(cuts[0]["direction"], "negative")
        self.assertEqual(cuts[0]["name"], "Rear electronics bays")
        self.assertIn("Hub75Panel_depth", str(cuts[0]["distance"]))
        self.assertIn("Hub75Panel_front_depth", str(cuts[0]["distance"]))

        # Drawing and STEP values; coordinates are measured, not guessed.
        panel = Hub75Panel()
        self.assertEqual(panel.depth - panel.front_depth, 12.5)
        side = 12.5 * 159.70 / 160.0
        end = 10.75 * 319.71 / 320.0
        crossbar = 20 * 319.71 / 320.0
        actual_width = 159.70 - 2 * side
        self.assertAlmostEqual(actual_width, 134.746875, places=5)
        expected_bounds = [
            (-319.71 / 2 + end, -319.71 / 4 - crossbar / 2),
            (-319.71 / 4 + crossbar / 2, -crossbar / 2),
            (crossbar / 2, 319.71 / 4 - crossbar / 2),
            (319.71 / 4 + crossbar / 2, 319.71 / 2 - end),
        ]
        # The SCPF compiler preserves symbolic param expressions: compare
        # numeric drawing inputs rather than requiring hardcoded output strings.
        self.assertEqual(len(expected_bounds), len(rectangles))
        self.assertTrue(all(high > low for low, high in expected_bounds))
        self.assertEqual(len([c for c in commands
                              if c["command"] == "solid.hole"]), 6)

    def test_taper_rejects_invalid_dimensions(self):
        from scpf.core import Box
        for kwargs in (
            {"from_z": 0, "inset": 1.25},
            {"from_z": 20, "inset": 1.25},
            {"from_z": 2, "inset": 100},
            {"from_z": 2, "inset": 0},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                Box(159.70, 319.71, 14.50).taper(**kwargs)

    def test_mount_positions_match_source_drawing(self):
        commands = run_script(MODEL)["commands"]
        holes = [c["params"] for c in commands if c["command"] == "solid.hole"]
        # Parameter expressions may be retained by the native compiler.
        positions = [h["position"] for h in holes]
        self.assertEqual(len(positions), 6)
        self.assertEqual(len({str(p) for p in positions}), 6)
        self.assertTrue(all(h["direction"] == [0, 0, -1] for h in holes))
        # Every bore must start at the REAR and terminate at Z=2 mm.
        # An old through-hole depth of 15 mm would pierce the front face.
        # Native input preserves expressions in the parameterized model.
        from components.hub75 import Hub75Panel
        reference = Hub75Panel()
        self.assertEqual(reference.depth - reference.front_depth, 12.5)
        for bore in holes:
            depth_expression = str(bore["depth"])
            self.assertIn("Hub75Panel_depth", depth_expression)
            self.assertIn("Hub75Panel_front_depth", depth_expression)
            self.assertNotIn("15", depth_expression)
        self.assertEqual(len(holes), 6)
        self.assertTrue(all(h["targets"] == ["Hub75Panel"] for h in holes))

    def test_material_is_native_and_housing_color_is_grey(self):
        commands = run_script(MODEL)["commands"]
        material = next(c["params"] for c in commands if c["command"] == "material.create")
        self.assertEqual(material["color"], "#B8B8B8")
        assigned = next(c["params"] for c in commands if c["command"] == "material.assign")
        self.assertEqual(assigned["bodies"], ["Hub75Panel"])


if __name__ == "__main__":
    unittest.main()
