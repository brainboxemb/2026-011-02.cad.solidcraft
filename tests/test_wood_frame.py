"""Regression tests for the split wooden HUB75 assembly."""

import ast
from pathlib import Path
import tempfile
import unittest

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
SCPF_DIR = ROOT / "models/advanced/hub75-wood-frame/scpf"
MODEL = SCPF_DIR / "model.py"
BOARD = SCPF_DIR / "parts/board.py"
GLASS_STRIP = SCPF_DIR / "parts/glass_strip.py"
WINDOW = SCPF_DIR / "parts/window.py"
ASSEMBLIES = SCPF_DIR / "assemblies"


def commands(**overrides):
    if not overrides:
        return run_script(MODEL)["commands"]

    text = MODEL.read_text(encoding="utf-8")
    assert text.rstrip().endswith("WoodenHub75Box()")
    args = ", ".join(f"{key}={value!r}" for key, value in overrides.items())
    changed = text.rstrip()[:-len("WoodenHub75Box()")] + f"WoodenHub75Box({args})\n"

    # Keep the temporary entrypoint beside model.py so its local
    # parts/ and assemblies/ imports resolve exactly as in normal use.
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        prefix="_wood_frame_test_",
        dir=SCPF_DIR,
        delete=False,
        encoding="utf-8",
    )
    try:
        with handle:
            handle.write(changed)
        return run_script(Path(handle.name))["commands"]
    finally:
        Path(handle.name).unlink(missing_ok=True)


def of(all_commands, kind):
    return [
        entry["params"]
        for entry in all_commands
        if entry["command"] == kind
    ]


def moved(all_commands, name):
    return [
        params
        for params in of(all_commands, "occurrence.move")
        if params["occurrence"].startswith(name + ":")
    ]


class WoodenFrameTests(unittest.TestCase):
    def test_model_is_composition_only_and_sources_are_split(self):
        definitions = ast.parse(MODEL.read_text(encoding="utf-8")).body
        classes = [
            obj.name for obj in definitions
            if isinstance(obj, ast.ClassDef)
        ]
        self.assertEqual(classes, ["WoodenHub75Box"])

        board_classes = [
            obj.name for obj in ast.parse(
                BOARD.read_text(encoding="utf-8")
            ).body
            if isinstance(obj, ast.ClassDef)
        ]
        self.assertEqual(
            board_classes,
            ["Board", "SideWall", "BottomBoard", "RoofBoard", "BackBoard"],
        )

        glass_classes = [
            obj.name for obj in ast.parse(
                GLASS_STRIP.read_text(encoding="utf-8")
            ).body
            if isinstance(obj, ast.ClassDef)
        ]
        self.assertEqual(glass_classes, ["GlassStrip"])
        self.assertTrue(WINDOW.exists())

        self.assertEqual(
            {path.name for path in ASSEMBLIES.glob("*.py")},
            {
                "hub75_panels.py",
                "wood_frame.py",
                "glass_frame.py",
                "corner_brackets.py",
            },
        )

        sources = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SCPF_DIR.glob("**/*.py")
        )
        self.assertNotIn("value_of", sources)
        self.assertNotIn("GlassSideStrip", sources)
        self.assertNotIn("GlassCrossStrip", sources)
        self.assertNotIn("def build_window", sources)
        self.assertNotIn("def build_wood_frame", sources)
        self.assertIn("window = Window().move(", MODEL.read_text(encoding="utf-8"))

    def test_adjustable_parameters_are_lowercase_and_fixed_glass_is_uppercase(self):
        model_source = MODEL.read_text(encoding="utf-8")
        window_source = WINDOW.read_text(encoding="utf-8")

        for name in (
            "GLASS_WIDTH",
            "GLASS_HEIGHT",
            "GLASS_THICKNESS",
            "GLASS_BOTTOM_CLEARANCE",
        ):
            self.assertIn(name + " =", window_source)

        for old_parameter in (
            "glass_width =",
            "glass_height =",
            "glass_thickness =",
            "glass_bottom_clearance =",
        ):
            self.assertNotIn(old_parameter, model_source)

        parameter_names = {p["name"] for p in of(commands(), "parameters.add")}
        self.assertFalse(any(name.startswith("Window_") for name in parameter_names))

    def test_board_keeps_geometry_symbolic_and_uses_named_edges(self):
        source = BOARD.read_text(encoding="utf-8")
        self.assertIn("half = self.width / 2", source)
        self.assertNotIn("pv(self.width)", source)
        self.assertNotIn("pv(self.height)", source)
        self.assertIn("Edges.from_vertices", source)

        cmd = commands()
        parameter_names = {p["name"] for p in of(cmd, "parameters.add")}
        self.assertIn("BottomBoard_corner_radius", parameter_names)
        self.assertIn("RoofBoard_corner_radius", parameter_names)

        radii = {
            params["radius"]
            for params in of(cmd, "solid.fillet")
        }
        self.assertIn("BottomBoard_corner_radius", radii)
        self.assertIn("RoofBoard_corner_radius", radii)

    def test_exactly_one_source_definition_per_wooden_part(self):
        cmd = commands()
        names = [p["name"] for p in of(cmd, "component.create")]
        self.assertEqual(len(names), 13)

        for name in (
            "HUB75Panels",
            "WoodBoxFrame",
            "WoodGlassFrame",
            "CornerBrackets",
            "Hub75PanelBasic",
            "SideWall",
            "BottomBoard",
            "RoofBoard",
            "BackBoard",
            "Window",
            "GlassStrip",
            "GlassStrip 2",
            "CornerBracket",
        ):
            self.assertIn(name, names)

        copies = of(cmd, "occurrence.copy")
        for name, count in [
            ("Hub75PanelBasic", 4),
            ("SideWall", 1),
            ("GlassStrip", 1),
            ("GlassStrip 2", 1),
            ("CornerBracket", 7),
        ]:
            self.assertEqual(
                sum(p["component"] == name for p in copies),
                count,
                name,
            )

    def test_all_part_positions_derived_from_central_dimensions(self):
        cmd = commands()
        self.assertEqual(
            [p["translate"] for p in moved(cmd, "SideWall")],
            [[-428.0, 25.0, 0.0], [428.0, 25.0, 0.0]],
        )
        self.assertEqual(
            moved(cmd, "BottomBoard")[0]["translate"],
            [0.0, 25.0, -12.0],
        )
        self.assertEqual(
            moved(cmd, "RoofBoard")[0]["translate"],
            [0.0, 25.0, 362.0],
        )
        self.assertEqual(
            moved(cmd, "BackBoard")[0]["translate"],
            [0.0, 79.5, -12.0],
        )
        self.assertEqual(
            moved(cmd, "Window")[0]["translate"],
            [0.0, -11.0, 1.0],
        )
        self.assertEqual(
            sorted(
                p["translate"][0]
                for p in moved(cmd, "Hub75PanelBasic")
            ),
            [-320.0, -160.0, 0.0, 160.0, 320.0],
        )

    def test_glassstrip_two_lengths_four_placements_no_corner_fillet(self):
        cmd = commands()
        horizontal = moved(cmd, "GlassStrip")
        vertical = moved(cmd, "GlassStrip 2")

        self.assertEqual(len(horizontal), 2)
        self.assertEqual(len(vertical), 2)
        self.assertEqual(
            [p["translate"] for p in horizontal],
            [[0.0, -19.0, 0.0], [0.0, -19.0, 362.0]],
        )
        self.assertEqual(
            [p["translate"] for p in vertical],
            [[-422.0, -19.0, 181.0], [422.0, -19.0, 181.0]],
        )
        self.assertEqual(vertical[0]["axis"], [0.0, 1.0, 0.0])
        self.assertEqual(vertical[0]["angle"], "90 deg")
        self.assertEqual(vertical[1]["angle"], "-90 deg")
        self.assertEqual(horizontal[1]["axis"], [1.0, 0.0, 0.0])
        self.assertEqual(horizontal[1]["angle"], "180 deg")

        self.assertEqual(
            sum(
                "GlassStrip" in p["name"]
                for p in of(cmd, "component.create")
            ),
            2,
        )

        # Bottom board, roof board and shared CornerBracket.
        self.assertEqual(len(of(cmd, "solid.fillet")), 3)

        parameter_names = {p["name"] for p in of(cmd, "parameters.add")}
        for part in ("GlassStrip", "GlassStrip_2"):
            self.assertTrue(
                {
                    part + "_length",
                    part + "_width",
                    part + "_depth",
                }.issubset(parameter_names)
            )

        sketch_points = " ".join(
            str(p["points"])
            for p in of(cmd, "sketch.line")
        )
        for name in (
            "GlassStrip_length",
            "GlassStrip_width",
            "GlassStrip_2_length",
            "GlassStrip_2_width",
        ):
            self.assertIn(name, sketch_points)

        materials = {
            p["name"]: p["color"]
            for p in of(cmd, "material.create")
        }
        self.assertEqual(
            materials["LIGHTPLY glazing vertical"],
            "#A9793E",
        )
        self.assertEqual(
            materials["LIGHTPLY glazing horizontal"],
            "#E3BF80",
        )
        self.assertEqual(
            materials["LIGHTPLY side wall"],
            "#CBA36B",
        )

    def test_eight_brackets_front_and_back(self):
        cmd = commands()
        brackets = moved(cmd, "CornerBracket")
        self.assertEqual(len(brackets), 8)

        coords = {
            (
                p["translate"][0],
                p["translate"][1],
                p["translate"][2],
            )
            for p in brackets
        }
        expected = {
            (x, y, z)
            for x in (-434.0, 434.0)
            for y in (-13.0, 63.0)
            for z in (-12.0, 374.0)
        }
        self.assertEqual(coords, expected)
        self.assertFalse(
            any(p["command"] == "solid.hole" for p in cmd)
        )

        bracket_width = 24.0
        back_start_y = 75.0
        rear_brackets = [
            p for p in brackets
            if p["translate"][1] > 0
        ]
        self.assertEqual(len(rear_brackets), 4)
        for bracket in rear_brackets:
            last_y = bracket["translate"][1] + bracket_width / 2
            self.assertAlmostEqual(last_y, back_start_y)
            self.assertLessEqual(last_y, back_start_y)

    def test_wood_dimensions_and_roof_overhang(self):
        source = MODEL.read_text(encoding="utf-8")
        self.assertIn("frame_wood_thickness = 12.0", source)
        self.assertIn("panel_wood_thickness = 9.0", source)
        self.assertIn("roof_front_overhang = 10.0", source)
        self.assertIn("roof_rear_overhang = 1.0", source)
        self.assertEqual(
            (-35.0, 85.0),
            (-25.0 - 10.0, 75.0 + 9.0 + 1.0),
        )

    def test_parameter_override_changes_all_dependents(self):
        cmd = commands(opening_width=850, frame_wood_thickness=13)

        side_x = [
            p["translate"][0]
            for p in moved(cmd, "SideWall")
        ]
        bracket_x = sorted({
            p["translate"][0]
            for p in moved(cmd, "CornerBracket")
        })

        self.assertEqual(side_x, [-431.5, 431.5])
        self.assertEqual(bracket_x, [-438.0, 438.0])
        self.assertEqual(
            moved(cmd, "BottomBoard")[0]["translate"][2],
            -13.0,
        )
        self.assertEqual(
            moved(cmd, "RoofBoard")[0]["translate"][2],
            362.0,
        )
        self.assertEqual(
            moved(cmd, "GlassStrip 2")[0]["translate"][0],
            -425.0,
        )

    def test_all_copies_created_before_native_placements(self):
        cmd = commands()
        for name in (
            "CornerBracket",
            "GlassStrip",
            "GlassStrip 2",
            "SideWall",
            "Hub75PanelBasic",
        ):
            copy_idx = [
                i for i, command in enumerate(cmd)
                if command["command"] == "occurrence.copy"
                and command["params"]["component"] == name
            ]
            move_idx = [
                i for i, command in enumerate(cmd)
                if command["command"] == "occurrence.move"
                and command["params"]["occurrence"].startswith(name + ":")
            ]
            self.assertTrue(copy_idx and move_idx)
            self.assertLess(max(copy_idx), min(move_idx))

        for params in of(cmd, "occurrence.move"):
            self.assertNotIn("matrix", params)
            self.assertNotIn("to", params)


if __name__ == "__main__":
    unittest.main()
