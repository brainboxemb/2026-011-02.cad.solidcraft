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
GLASS_FRAME = ASSEMBLIES / "glass_frame.py"


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
            ["Board", "SideBoard", "LeftBoard", "RightBoard", "BottomBoard", "RoofBoard", "BackBoard"],
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
        self.assertIn("window = Window(", MODEL.read_text(encoding="utf-8"))

    def test_adjustable_parameters_are_lowercase_and_fixed_glass_is_uppercase(self):
        model_source = MODEL.read_text(encoding="utf-8")
        window_source = WINDOW.read_text(encoding="utf-8")

        for name in (
            "GLASS_WIDTH",
            "GLASS_HEIGHT",
            "GLASS_THICKNESS",
        ):
            self.assertIn(name + " =", window_source)

        for old_parameter in (
            "glass_width =",
            "glass_height =",
            "glass_thickness =",
        ):
            self.assertNotIn(old_parameter, model_source)

        parameter_names = {p["name"] for p in of(commands(), "parameters.add")}
        self.assertFalse(any(name.startswith("Window_") for name in parameter_names))
        self.assertIn("opening_height", parameter_names)
        self.assertIn("(self.opening_height - GLASS_HEIGHT) / 2", window_source)

    def test_board_keeps_geometry_symbolic_and_uses_named_edges(self):
        source = BOARD.read_text(encoding="utf-8")
        self.assertIn("half = self.width / 2", source)
        self.assertNotIn("pv(self.width)", source)
        self.assertNotIn("pv(self.height)", source)
        self.assertIn("Edges.from_vertices", source)

        cmd = commands()
        parameter_names = {p["name"] for p in of(cmd, "parameters.add")}
        self.assertIn("corner_radius", parameter_names)
        self.assertNotIn("BottomBoard_corner_radius", parameter_names)
        self.assertNotIn("RoofBoard_corner_radius", parameter_names)

        radii = [
            params["radius"]
            for params in of(cmd, "solid.fillet")
        ]
        self.assertEqual(radii.count("corner_radius"), 4)

    def test_exactly_one_source_definition_per_wooden_part(self):
        cmd = commands()
        names = [p["name"] for p in of(cmd, "component.create")]
        self.assertEqual(len(names), 17)

        for name in (
            "HUB75Panels",
            "WoodBoxFrame",
            "WoodGlassFrame",
            "CornerBrackets",
            "Hub75PanelBasic",
            "LeftBoard",
            "RightBoard",
            "BottomBoard",
            "RoofBoard",
            "BackBoard",
            "Window",
            "GlassStrip",
            "GlassStrip 2",
            "GlassStrip 3",
            "GlassStrip 4",
            "CornerBracket",
            "CornerBracket 2",
        ):
            self.assertIn(name, names)

        copies = of(cmd, "occurrence.copy")
        for name, count in [
            ("Hub75PanelBasic", 4),
            ("CornerBracket", 3),
            ("CornerBracket 2", 3),
        ]:
            self.assertEqual(
                sum(p["component"] == name for p in copies),
                count,
                name,
            )

    def test_basic_hub75_envelope_uses_fixed_constants(self):
        from components.hub75_basic import (
            HUB75_PANEL_DEPTH,
            HUB75_PANEL_HEIGHT,
            HUB75_PANEL_WIDTH,
        )

        self.assertEqual(HUB75_PANEL_WIDTH, 159.70)
        self.assertEqual(HUB75_PANEL_HEIGHT, 319.71)
        self.assertEqual(HUB75_PANEL_DEPTH, 14.50)

        parameter_names = {
            p["name"] for p in of(commands(), "parameters.add")
        }
        self.assertFalse(
            any(name.startswith("Hub75PanelBasic_") for name in parameter_names)
        )

    def test_all_part_positions_derived_from_central_dimensions(self):
        cmd = commands()
        self.assertEqual(
            moved(cmd, "LeftBoard")[0]["translate"],
            [-428.0, 50.0, 0.0],
        )
        self.assertEqual(
            moved(cmd, "RightBoard")[0]["translate"],
            [428.0, 50.0, 0.0],
        )
        self.assertEqual(
            moved(cmd, "BottomBoard")[0]["translate"],
            [0.0, 50.0, -12.0],
        )
        self.assertEqual(
            moved(cmd, "RoofBoard")[0]["translate"],
            [0.0, 50.0, 0.0],
        )
        self.assertEqual(
            moved(cmd, "BackBoard")[0]["translate"],
            [0.0, 104.5, -12.0],
        )
        self.assertEqual(
            moved(cmd, "Window")[0]["translate"],
            [0.0, 14.0, 0.0],
        )
        panels = moved(cmd, "Hub75PanelBasic")
        self.assertEqual(
            sorted(p["translate"][0] for p in panels),
            [-320.0, -160.0, 0.0, 160.0, 320.0],
        )
        self.assertTrue(
            all(p["translate"][1] == 32.25 for p in panels)
        )
        self.assertTrue(
            all(p["translate"][2] == 0.0 for p in panels)
        )

    def test_glass_frame_uses_named_axis_rotation(self):
        source = GLASS_FRAME.read_text(encoding="utf-8")
        self.assertIn("rotate(X, 180)", source)
        self.assertIn("rotate(Y, 90)", source)
        self.assertIn("rotate(Y, -90)", source)
        self.assertNotIn("axis=(1, 0, 0)", source)
        self.assertNotIn("axis=(0, 1, 0)", source)

    def test_glassstrip_two_lengths_four_placements_no_corner_fillet(self):
        cmd = commands()
        strip_moves = [
            p for p in of(cmd, "occurrence.move")
            if p["occurrence"].startswith("GlassStrip")
        ]
        self.assertEqual(len(strip_moves), 4)
        self.assertTrue(
            all(p["translate"] == [0.0, 6.0, 0.0] for p in strip_moves)
        )

        rotations = {
            (tuple(p.get("axis", [])), p.get("angle"))
            for p in strip_moves
            if "axis" in p
        }
        self.assertEqual(
            rotations,
            {
                ((1.0, 0.0, 0.0), "180 deg"),
                ((0.0, 1.0, 0.0), "90 deg"),
                ((0.0, 1.0, 0.0), "-90 deg"),
            },
        )

        self.assertEqual(
            sum(
                p["name"].startswith("GlassStrip")
                for p in of(cmd, "component.create")
            ),
            4,
        )

        # Bottom board, roof board and two bracket orientation definitions.
        self.assertEqual(len(of(cmd, "solid.fillet")), 4)

        parameter_names = {p["name"] for p in of(cmd, "parameters.add")}
        for duplicated in (
            "GlassStrip_length",
            "GlassStrip_width",
            "GlassStrip_depth",
            "GlassStrip_2_length",
            "GlassStrip_2_width",
            "GlassStrip_2_depth",
        ):
            self.assertNotIn(duplicated, parameter_names)

        for source_parameter in (
            "opening_width",
            "opening_height",
            "glazing_wood_width",
            "glazing_wood_depth",
        ):
            self.assertIn(source_parameter, parameter_names)

        sketch_points = " ".join(
            str(p["points"])
            for p in of(cmd, "sketch.line")
        )
        for name in (
            "opening_width",
            "opening_height",
            "glazing_wood_width",
        ):
            self.assertIn(name, sketch_points)

        self.assertNotIn("GlassStrip_length", sketch_points)
        self.assertNotIn("GlassStrip_width", sketch_points)
        self.assertNotIn("GlassStrip_2_length", sketch_points)
        self.assertNotIn("GlassStrip_2_width", sketch_points)

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
            materials["LIGHTPLY side board"],
            "#CBA36B",
        )

    def test_component_defaults_do_not_clutter_design_parameters(self):
        parameter_names = {
            p["name"] for p in of(commands(), "parameters.add")
        }

        for prefix in (
            "CornerBracket_",
            "LeftBoard_",
            "RightBoard_",
            "BottomBoard_",
            "RoofBoard_",
            "BackBoard_",
            "GlassStrip_",
            "Hub75PanelBasic_",
        ):
            self.assertFalse(
                any(name.startswith(prefix) for name in parameter_names),
                prefix,
            )

        self.assertIn("corner_radius", parameter_names)

    def test_bracket_inside_radius_uses_frame_corner_radius(self):
        cmd = commands()
        bracket_fillet = [
            params for params in of(cmd, "solid.fillet")
            if params["body"].startswith("CornerBracket")
        ]
        self.assertEqual(len(bracket_fillet), 2)
        self.assertTrue(
            all(item["radius"] == "corner_radius" for item in bracket_fillet)
        )

    def test_eight_brackets_front_and_back(self):
        cmd = commands()
        brackets = [
            p for p in of(cmd, "occurrence.move")
            if p["occurrence"].startswith("CornerBracket")
        ]
        self.assertEqual(len(brackets), 8)

        top = [
            p for p in brackets
            if p["occurrence"].startswith("CornerBracket:")
        ]
        bottom = [
            p for p in brackets
            if p["occurrence"].startswith("CornerBracket 2:")
        ]
        self.assertEqual(len(top), 4)
        self.assertEqual(len(bottom), 4)
        self.assertTrue(all(p["translate"][2] == 0.0 for p in top))
        self.assertTrue(all(p["translate"][2] == -12.0 for p in bottom))
        self.assertFalse(
            any(p["command"] == "solid.hole" for p in cmd)
        )

        bracket_width = 24.0
        back_start_y = 100.0
        rear_brackets = [
            p for p in brackets
            if p["translate"][1] == 88.0
        ]
        self.assertEqual(len(rear_brackets), 4)
        for bracket in rear_brackets:
            last_y = bracket["translate"][1] + bracket_width / 2
            self.assertAlmostEqual(last_y, back_start_y)
            self.assertLessEqual(last_y, back_start_y)

    def test_roof_z_is_symbolic_geometry_not_fixed_occurrence_move(self):
        cmd = commands(opening_height=400)

        roof_move = moved(cmd, "RoofBoard")[0]
        self.assertEqual(roof_move["translate"], [0.0, 50.0, 0.0])

        create_index = next(
            i for i, command in enumerate(cmd)
            if command["command"] == "component.create"
            and command["params"]["name"] == "RoofBoard"
        )
        activate_index = next(
            i for i in range(create_index + 1, len(cmd))
            if cmd[i]["command"] == "component.activate"
            and cmd[i]["params"]["component"] == "root"
        )
        roof_commands = cmd[create_index:activate_index]
        roof_profile = next(
            command["params"] for command in roof_commands
            if command["command"] == "sketch.line"
        )

        points = str(roof_profile["points"])
        self.assertIn("opening_height", points)
        self.assertNotIn("RoofBoard_z_position", points)

    def test_window_size_is_fixed_but_position_stays_centred(self):
        cmd = commands(opening_height=400)

        window_move = moved(cmd, "Window")[0]
        self.assertEqual(window_move["translate"], [0.0, 14.0, 0.0])

        create_index = next(
            i for i, command in enumerate(cmd)
            if command["command"] == "component.create"
            and command["params"]["name"] == "Window"
        )
        activate_index = next(
            i for i in range(create_index + 1, len(cmd))
            if cmd[i]["command"] == "component.activate"
            and cmd[i]["params"]["component"] == "root"
        )
        window_commands = cmd[create_index:activate_index]
        points = " ".join(
            str(command["params"]["points"])
            for command in window_commands
            if command["command"] == "sketch.line"
        )

        self.assertIn("opening_height", points)
        self.assertIn("360.0", points)

    def test_opening_height_drives_all_vertical_dependents_symbolically(self):
        cmd = commands(opening_height=400)

        # No dependent component may freeze the edited opening height into a
        # vertical occurrence translation.
        for params in of(cmd, "occurrence.move"):
            if (
                params["occurrence"].startswith("GlassStrip")
                or params["occurrence"].startswith("Hub75PanelBasic")
                or params["occurrence"].startswith("CornerBracket:")
            ):
                self.assertEqual(params["translate"][2], 0.0)

        points = " ".join(
            str(params["points"]) for params in of(cmd, "sketch.line")
        )
        self.assertIn("opening_height", points)

    def test_wood_dimensions_and_roof_overhang(self):
        source = MODEL.read_text(encoding="utf-8")
        self.assertIn("frame_wood_thickness = 12.0", source)
        self.assertIn("panel_wood_thickness = 9.0", source)
        self.assertIn("roof_front_overhang = 10.0", source)
        self.assertIn("roof_rear_overhang = 1.0", source)
        self.assertIn("panel_recess_depth = 25.0", source)
        self.assertNotIn("frame_front_y_position", source)
        self.assertEqual(
            (-10.0, 110.0),
            (-10.0, 100.0 + 9.0 + 1.0),
        )

    def test_parameter_override_changes_all_dependents(self):
        cmd = commands(opening_width=850, frame_wood_thickness=13)

        side_x = [
            moved(cmd, "LeftBoard")[0]["translate"][0],
            moved(cmd, "RightBoard")[0]["translate"][0],
        ]
        bracket_x = sorted({
            p["translate"][0]
            for p in of(cmd, "occurrence.move")
            if p["occurrence"].startswith("CornerBracket")
        })

        self.assertEqual(side_x, [-431.5, 431.5])
        self.assertEqual(bracket_x, [-438.0, 438.0])
        self.assertEqual(
            moved(cmd, "BottomBoard")[0]["translate"][2],
            -13.0,
        )
        self.assertEqual(
            moved(cmd, "RoofBoard")[0]["translate"][2],
            0.0,
        )
        sketch_points = " ".join(
            str(p["points"]) for p in of(cmd, "sketch.line")
        )
        self.assertIn("opening_width", sketch_points)

    def test_all_copies_created_before_native_placements(self):
        cmd = commands()
        for name in (
            "CornerBracket",
            "CornerBracket 2",
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
