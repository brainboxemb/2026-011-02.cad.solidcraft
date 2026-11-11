"""Regression tests for ONE parametrized wooden HUB75 assembly.

The Python model defines its wooden parts and ONE GlassStrip type locally.
SCPF creates editable native SolidCraft component definitions and instances.
The separate native workflow also checks the real saved BRep and transforms.
"""
import ast
from pathlib import Path
import tempfile
import unittest

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "models/advanced/hub75-wood-frame/scpf/model.py"


def commands(**overrides):
    if not overrides:
        return run_script(MODEL)["commands"]
    text = MODEL.read_text(encoding="utf-8")
    assert text.rstrip().endswith("WoodenHub75Box()")
    args = ", ".join(f"{key}={value!r}" for key, value in overrides.items())
    changed = text.rstrip()[:-len("WoodenHub75Box()")] + f"WoodenHub75Box({args})\n"
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "model.py"
        # Temp model still imports shared components through the project path:
        # runner auto-resolves only model-directory roots. Here tests have the
        # project root in sys.path from pytest/PYTHONPATH.
        path.write_text(changed, encoding="utf-8")
        return run_script(path)["commands"]


def of(all_commands, kind):
    return [entry["params"] for entry in all_commands
            if entry["command"] == kind]


def moved(all_commands, name):
    return [p for p in of(all_commands, "occurrence.move")
            if p["occurrence"].startswith(name + ":")]


class WoodenFrameTests(unittest.TestCase):
    def test_one_script_and_one_glassstrip_type(self):
        source = MODEL.read_text(encoding="utf-8")
        definitions = ast.parse(source).body
        names = [obj.name for obj in definitions if isinstance(obj, ast.ClassDef)]
        self.assertEqual(names, [
            "SideWall", "BottomBoard", "RoofBoard", "BackBoard",
            "Window", "GlassStrip", "WoodenHub75Box",
        ])
        self.assertNotIn("from math import", source)
        self.assertNotIn("GlassSideStrip", source)
        self.assertNotIn("GlassCrossStrip", source)
        self.assertNotIn("hub75_wood_frame", source)

    def test_exactly_one_source_definition_per_wooden_part(self):
        cmd = commands()
        names = [p["name"] for p in of(cmd, "component.create")]
        self.assertEqual(len(names), 13)
        for name in ("HUB75Panels", "WoodBoxFrame", "WoodGlassFrame",
                     "CornerBrackets", "Hub75PanelBasic", "SideWall",
                     "BottomBoard", "RoofBoard", "BackBoard", "Window",
                     "GlassStrip", "GlassStrip 2", "CornerBracket"):
            self.assertIn(name, names)
        copies = of(cmd, "occurrence.copy")
        for name, count in [
            ("Hub75PanelBasic", 4),
            ("SideWall", 1),
            ("GlassStrip", 1),
            ("GlassStrip 2", 1),
            ("CornerBracket", 7),
        ]:
            self.assertEqual(sum(p["component"] == name for p in copies),
                             count, name)

    def test_all_part_positions_derived_from_central_dimensions(self):
        cmd = commands()
        self.assertEqual([p["translate"] for p in moved(cmd, "SideWall")],
                         [[-428., 25., 0.], [428., 25., 0.]])
        self.assertEqual(moved(cmd, "BottomBoard")[0]["translate"],
                         [0., 25., -12.])
        self.assertEqual(moved(cmd, "RoofBoard")[0]["translate"],
                         [0., 25., 362.])
        self.assertEqual(moved(cmd, "BackBoard")[0]["translate"],
                         [0., 79.5, -12.])
        self.assertEqual(moved(cmd, "Window")[0]["translate"],
                         [0., -8., 1.])
        self.assertEqual(sorted([p["translate"][0]
                                 for p in moved(cmd, "Hub75PanelBasic")]),
                         [-320., -160., 0., 160., 320.])

    def test_glassstrip_two_lengths_four_placements_no_corner_fillet(self):
        cmd = commands()
        horizontal = moved(cmd, "GlassStrip")
        vertical = moved(cmd, "GlassStrip 2")
        self.assertEqual(len(horizontal), 2)
        self.assertEqual(len(vertical), 2)
        self.assertEqual([p["translate"] for p in horizontal], [
            [0., -17.5, 0.], [0., -17.5, 362.],
        ])
        self.assertEqual([p["translate"] for p in vertical], [
            [-422., -17.5, 181.], [422., -17.5, 181.],
        ])
        self.assertEqual(vertical[0]["axis"], [0., 1., 0.])
        self.assertEqual(vertical[0]["angle"], "90 deg")
        self.assertEqual(vertical[1]["angle"], "-90 deg")
        self.assertEqual(horizontal[1]["axis"], [1., 0., 0.])
        self.assertEqual(horizontal[1]["angle"], "180 deg")
        # Both lengths are instances of the SAME Python GlassStrip type,
        # with two native definitions due to different dimensions/finishes.
        self.assertEqual(sum("GlassStrip" in p["name"]
                             for p in of(cmd, "component.create")), 2)

        # One fillet for each plywood board and one for shared bracket.
        self.assertEqual(len(of(cmd, "solid.fillet")), 3)
        materials = {p["name"]: p["color"]
                     for p in of(cmd, "material.create")}
        self.assertEqual(materials["LIGHTPLY glazing vertical"], "#A9793E")
        self.assertEqual(materials["LIGHTPLY glazing horizontal"], "#E3BF80")
        self.assertEqual(materials["LIGHTPLY side wall"], "#CBA36B")

    def test_eight_brackets_front_and_back(self):
        cmd = commands()
        brackets = moved(cmd, "CornerBracket")
        self.assertEqual(len(brackets), 8)
        coords = {(p["translate"][0], p["translate"][1], p["translate"][2])
                  for p in brackets}
        expected = {(x, y, z)
                    for x in (-434., 434.)
                    for y in (-13., 72.)
                    for z in (-12., 374.)}
        self.assertEqual(coords, expected)
        self.assertFalse(any(p["command"] == "solid.hole" for p in cmd))

    def test_wood_dimensions_and_roof_overhang(self):
        source = MODEL.read_text(encoding="utf-8")
        self.assertIn("wood_thickness = 12.0", source)
        self.assertIn("back_thickness = 9.0", source)
        self.assertIn("roof_front_overhang = 10.0", source)
        self.assertIn("roof_rear_overhang = 1.0", source)
        # Roof from -35 to +85; sidewalls -25..+75; rear board +75..+84.
        # Thus 10 mm front overhang relative to side and 1 mm beyond rear ply.
        self.assertEqual((-35., 85.), (-25. - 10., 75. + 9. + 1.))

    def test_parameter_override_changes_all_dependents(self):
        cmd = commands(opening_width=850, wood_thickness=13)
        side_x = [p["translate"][0] for p in moved(cmd, "SideWall")]
        bracket_x = sorted({p["translate"][0] for p in moved(cmd, "CornerBracket")})
        self.assertEqual(side_x, [-431.5, 431.5])
        self.assertEqual(bracket_x, [-438., 438.])
        self.assertEqual(moved(cmd, "BottomBoard")[0]["translate"][2], -13.)
        self.assertEqual(moved(cmd, "RoofBoard")[0]["translate"][2], 362.)
        self.assertEqual(moved(cmd, "GlassStrip 2")[0]["translate"][0], -425.)

    def test_all_copies_created_before_native_placements(self):
        cmd = commands()
        for name in ("CornerBracket", "GlassStrip", "GlassStrip 2",
                     "SideWall", "Hub75PanelBasic"):
            copy_idx = [i for i, p in enumerate(cmd) if
                        p["command"] == "occurrence.copy"
                        and p["params"]["component"] == name]
            move_idx = [i for i, p in enumerate(cmd) if
                        p["command"] == "occurrence.move"
                        and p["params"]["occurrence"].startswith(name + ":")]
            self.assertTrue(copy_idx and move_idx)
            self.assertLess(max(copy_idx), min(move_idx))
        for p in of(cmd, "occurrence.move"):
            self.assertNotIn("matrix", p)
            self.assertNotIn("to", p)


if __name__ == "__main__":
    unittest.main()
