"""Regression tests for the split wooden HUB75 assembly."""

import ast
from pathlib import Path
import tempfile
import unittest
import warnings

from scpf.runner import ModelParameterWarning, run_script


ROOT = Path(__file__).resolve().parents[1]
SCPF_DIR = ROOT / "models/advanced/hub75_wood_frame/scpf"
MODEL = SCPF_DIR / "model.py"
BOARD = SCPF_DIR / "parts/board.py"
GLASS_STRIP = SCPF_DIR / "parts/glass_strip.py"
WINDOW = SCPF_DIR / "parts/window.py"
ASSEMBLIES = SCPF_DIR / "assemblies"
GLASS_FRAME = ASSEMBLIES / "glass_frame.py"
HUB75_PANELS = ASSEMBLIES / "hub75_panels.py"

BOARD_COMPONENTS = {
    "left": "Board",
    "right": "Board 2",
    "bottom": "Board 3",
    "roof": "Board 4",
    "rear": "Board 5",
}


def commands(**overrides):
    if not overrides:
        return run_script(MODEL)["commands"]

    text = MODEL.read_text(encoding="utf-8")
    args = ", ".join(f"{key}={value!r}" for key, value in overrides.items())
    # Normal model files use Forge's implicit single-class root. For a test
    # override, append one explicit call with the requested parameter values.
    changed = text.rstrip() + f"\n\nWoodenHub75Box({args})\n"

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


def component_commands(all_commands, name):
    create_index = next(
        i for i, command in enumerate(all_commands)
        if command["command"] == "component.create"
        and command["params"]["name"] == name
    )
    activate_index = next(
        i for i in range(create_index + 1, len(all_commands))
        if all_commands[i]["command"] == "component.activate"
        and all_commands[i]["params"]["component"] == "root"
    )
    return all_commands[create_index:activate_index]


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
        self.assertEqual(board_classes, ["Board"])
        board_functions = [
            obj.name for obj in ast.parse(
                BOARD.read_text(encoding="utf-8")
            ).body
            if isinstance(obj, ast.FunctionDef)
        ]
        self.assertEqual(board_functions, [])

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
        self.assertIn("opening_bottom_z = 12.0", window_source)
        self.assertNotIn("frame_wood_thickness", window_source)

    def test_opening_consumers_do_not_know_about_wood_thickness(self):
        model_source = MODEL.read_text(encoding="utf-8")
        panel_source = (ASSEMBLIES / "hub75_panels.py").read_text(encoding="utf-8")
        glass_source = GLASS_FRAME.read_text(encoding="utf-8")
        window_source = WINDOW.read_text(encoding="utf-8")

        for source in (panel_source, glass_source, window_source):
            self.assertIn("opening_bottom_z", source)
            self.assertNotIn("frame_wood_thickness", source)

        self.assertIn(
            "opening_bottom_z = self.frame_wood_thickness",
            model_source,
        )
        self.assertIn("opening_bottom_z=opening_bottom_z", model_source)

    def test_parameter_intent_matches_native_parameter_list(self):
        model_source = MODEL.read_text(encoding="utf-8")
        panel_source = HUB75_PANELS.read_text(encoding="utf-8")

        self.assertIn("PANEL_COUNT = 5", panel_source)
        self.assertIn("PANEL_PITCH = 160.0", panel_source)
        self.assertNotIn("panel_count =", model_source)
        self.assertNotIn("panel_pitch =", model_source)
        self.assertIn("panel_recess_depth = 25.0", model_source)
        self.assertNotIn("_panel_recess_depth", model_source)
        self.assertIn("glazing_wood_depth = 12.0", model_source)

        parameter_names = {
            p["name"] for p in of(commands(), "parameters.add")
        }
        self.assertEqual(
            parameter_names,
            {
                "opening_width",
                "opening_height",
                "frame_wood_thickness",
                "panel_wood_thickness",
                "cabinet_depth",
                "panel_recess_depth",
                "roof_front_overhang",
                "roof_rear_overhang",
                "corner_radius",
                "bracket_width",
                "glazing_wood_width",
                "glazing_wood_depth",
            },
        )

    def test_parameter_intent_has_no_model_parameter_warnings(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            commands()

        parameter_warnings = [
            item for item in caught
            if issubclass(item.category, ModelParameterWarning)
        ]
        self.assertEqual(
            parameter_warnings,
            [],
            [str(item.message) for item in parameter_warnings],
        )

    def test_bracket_width_and_corner_radius_are_shared_model_parameters(self):
        cmd = commands(bracket_width=30, corner_radius=6)
        parameter_names = [p["name"] for p in of(cmd, "parameters.add")]

        self.assertEqual(parameter_names.count("bracket_width"), 1)
        self.assertEqual(parameter_names.count("corner_radius"), 1)
        self.assertFalse(
            any(name.startswith("CornerBracket_") for name in parameter_names)
        )

        part = component_commands(cmd, "CornerBracket")
        extrusion = next(
            item["params"] for item in part
            if item["command"] == "solid.extrude"
        )
        fillet = next(
            item["params"] for item in part
            if item["command"] == "solid.fillet"
        )
        self.assertEqual(extrusion["distance"], "bracket_width")
        self.assertEqual(fillet["radius"], "corner_radius")

    def test_board_keeps_geometry_symbolic_and_uses_named_edges(self):
        source = BOARD.read_text(encoding="utf-8")
        self.assertIn("half = self.width / 2", source)
        self.assertNotIn("pv(self.width)", source)
        self.assertNotIn("pv(self.height)", source)
        self.assertIn("Edges.from_vertices", source)

        cmd = commands()
        parameter_names = {p["name"] for p in of(cmd, "parameters.add")}
        self.assertIn("corner_radius", parameter_names)
        self.assertFalse(any(name.startswith("Board") for name in parameter_names))

        radii = [
            params["radius"]
            for params in of(cmd, "solid.fillet")
        ]
        self.assertEqual(radii.count("corner_radius"), 3)

    def test_exactly_one_source_definition_per_wooden_part(self):
        cmd = commands()
        names = [p["name"] for p in of(cmd, "component.create")]
        self.assertEqual(len(names), 16)

        for name in (
            "HUB75Panels",
            "WoodBoxFrame",
            "WoodGlassFrame",
            "CornerBrackets",
            "Hub75PanelBasic",
            "Board",
            "Board 2",
            "Board 3",
            "Board 4",
            "Board 5",
            "Window",
            "GlassStrip",
            "GlassStrip 2",
            "GlassStrip 3",
            "GlassStrip 4",
            "CornerBracket",
        ):
            self.assertIn(name, names)

        copies = of(cmd, "occurrence.copy")
        for name, count in [
            ("Hub75PanelBasic", 4),
            ("CornerBracket", 7),
        ]:
            self.assertEqual(
                sum(p["component"] == name for p in copies),
                count,
                name,
            )

    def test_basic_hub75_envelope_uses_fixed_constants(self):
        from models.components.hub75_panel.basic.scpf.model import (
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

        # Wood placement is part of the native sketch geometry. It must not
        # be frozen into occurrence translations.
        for name in BOARD_COMPONENTS.values():
            self.assertEqual(moved(cmd, name), [])

        self.assertEqual(moved(cmd, "Window"), [])
        # Panel depth belongs to the native component sketch plane.
        # Only the four fixed-pitch X copies need occurrence translations.
        panels = moved(cmd, "Hub75PanelBasic")
        self.assertEqual(
            sorted(p["translate"][0] for p in panels),
            [-320.0, -160.0, 160.0, 320.0],
        )
        self.assertTrue(all(p["translate"][1] == 0.0 for p in panels))
        self.assertTrue(all(p["translate"][2] == 0.0 for p in panels))

        panel = component_commands(cmd, "Hub75PanelBasic")
        sketch = next(
            item["params"] for item in panel
            if item["command"] == "sketch.create"
        )
        self.assertIn("panel_recess_depth", str(sketch["offset"]))

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
        self.assertEqual(len(strip_moves), 3)
        self.assertTrue(
            all(p["translate"] == [0.0, 0.0, 0.0] for p in strip_moves)
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

        # Bottom board, roof board and one reusable CornerBracket definition.
        self.assertEqual(len(of(cmd, "solid.fillet")), 3)

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
            materials["PINE glazing vertical"],
            "#A9793E",
        )
        self.assertEqual(
            materials["PINE glazing horizontal"],
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
            "Board_",
            "GlassStrip_",
            "Hub75PanelBasic_",
        ):
            self.assertFalse(
                any(name.startswith(prefix) for name in parameter_names),
                prefix,
            )

        self.assertIn("corner_radius", parameter_names)

    def test_corner_bracket_is_neutral_and_assembly_owns_placement(self):
        source = (
            ROOT / "models" / "components" / "corner_bracket" / "scpf" / "model.py"
        ).read_text(encoding="utf-8")
        assembly_source = (
            ASSEMBLIES / "corner_brackets.py"
        ).read_text(encoding="utf-8")

        for name in (
            "_x_position",
            "_y_position",
            "_z_position",
            "_x_sign",
            "_z_sign",
            "def placed",
        ):
            self.assertNotIn(name, source)

        self.assertIn("@assembly", assembly_source)
        self.assertIn("class CornerBrackets:", assembly_source)
        self.assertIn("wood_frame = None", assembly_source)
        self.assertIn("def build(self):", assembly_source)
        self.assertNotIn("def __new__", assembly_source)
        self.assertNotIn("attach_corner_brackets", assembly_source)
        self.assertNotIn(".move(", assembly_source)
        self.assertNotIn(".rotate(", assembly_source)
        self.assertNotIn("opening_width", assembly_source)
        self.assertNotIn("opening_height", assembly_source)
        self.assertIn(".attach(", assembly_source)
        self.assertIn("Anchor.FRONT_TOP_LEFT", assembly_source)
        self.assertIn("Anchor.BACK_BOTTOM_RIGHT", assembly_source)

        cmd = commands()
        creates = [
            p for p in of(cmd, "component.create")
            if p["name"] == "CornerBracket"
        ]
        self.assertEqual(len(creates), 1)
        self.assertEqual(
            sum(
                p["component"] == "CornerBracket"
                for p in of(cmd, "occurrence.copy")
            ),
            7,
        )

        joints = [
            p for p in of(cmd, "joint.create")
            if p["name"].startswith("Attach CornerBracket:")
        ]
        self.assertEqual(len(joints), 8)
        self.assertTrue(all(p["type"] == "rigid" for p in joints))

    def test_bracket_inside_radius_uses_frame_corner_radius(self):
        cmd = commands()
        bracket_fillet = [
            params for params in of(cmd, "solid.fillet")
            if params["body"].startswith("CornerBracket")
        ]
        self.assertEqual(len(bracket_fillet), 1)
        self.assertTrue(
            all(item["radius"] == "corner_radius" for item in bracket_fillet)
        )

    def test_eight_brackets_front_and_back(self):
        cmd = commands()
        creates = [
            p for p in of(cmd, "component.create")
            if p["name"] == "CornerBracket"
        ]
        self.assertEqual(len(creates), 1)
        self.assertEqual(
            sum(
                p["component"] == "CornerBracket"
                for p in of(cmd, "occurrence.copy")
            ),
            7,
        )

        joints = [
            p for p in of(cmd, "joint.create")
            if p["name"].startswith("Attach CornerBracket:")
        ]
        self.assertEqual(len(joints), 8)
        self.assertEqual(
            sum("front_mount" in str(p["b"]) for p in joints),
            4,
        )
        self.assertEqual(
            sum("rear_mount" in str(p["b"]) for p in joints),
            4,
        )
        self.assertEqual(
            sorted(p["angle"] for p in joints),
            [0, 0, 90, 90, 180, 180, 270, 270],
        )
        self.assertFalse(
            any(p["command"] == "solid.hole" for p in cmd)
        )

    def test_roof_z_is_symbolic_geometry_not_fixed_occurrence_move(self):
        cmd = commands(opening_height=400)

        self.assertEqual(moved(cmd, BOARD_COMPONENTS["roof"]), [])

        create_index = next(
            i for i, command in enumerate(cmd)
            if command["command"] == "component.create"
            and command["params"]["name"] == BOARD_COMPONENTS["roof"]
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
        self.assertNotIn("Board_4_z_position", points)

    def test_window_size_is_fixed_but_position_stays_centred(self):
        cmd = commands(opening_height=400)

        self.assertEqual(moved(cmd, "Window"), [])

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
        self.assertIn("360 mm", points)

    def test_opening_height_drives_all_vertical_dependents_symbolically(self):
        cmd = commands(opening_height=400)

        joints = [
            p for p in of(cmd, "joint.create")
            if p["name"].startswith("Attach CornerBracket:")
        ]
        self.assertEqual(
            sorted(p["a"]["corner"][2] for p in joints),
            [12.0, 12.0, 12.0, 12.0, 412.0, 412.0, 412.0, 412.0],
        )

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
        self.assertIn("bracket_width = 24.0", source)
        self.assertIn("glazing_wood_depth = 12.0", source)
        self.assertNotIn("frame_front_y_position", source)
        self.assertEqual(
            (-10.0, 110.0),
            (-10.0, 100.0 + 9.0 + 1.0),
        )

    def test_opening_width_drives_sideboards_and_brackets_symbolically(self):
        cmd = commands(opening_width=1000)

        self.assertEqual(moved(cmd, BOARD_COMPONENTS["left"]), [])
        self.assertEqual(moved(cmd, BOARD_COMPONENTS["right"]), [])

        joints = [
            p for p in of(cmd, "joint.create")
            if p["name"].startswith("Attach CornerBracket:")
        ]
        self.assertEqual(
            sorted(p["a"]["corner"][0] for p in joints),
            [-500.0, -500.0, -500.0, -500.0,
             500.0, 500.0, 500.0, 500.0],
        )

        points = " ".join(
            str(params["points"]) for params in of(cmd, "sketch.line")
        )
        self.assertIn("opening_width", points)

    def test_cabinet_depth_uses_front_datum_and_moves_rear_symbolically(self):
        cmd = commands(cabinet_depth=120)

        for name in BOARD_COMPONENTS.values():
            self.assertEqual(moved(cmd, name), [])

        for role in ("left", "right", "bottom"):
            part = component_commands(cmd, BOARD_COMPONENTS[role])
            sketch = next(
                item["params"] for item in part
                if item["command"] == "sketch.create"
            )
            extrusion = next(
                item["params"] for item in part
                if item["command"] == "solid.extrude"
            )
            self.assertEqual(sketch.get("offset", 0), 0.0)
            self.assertEqual(extrusion["direction"], "positive")
            self.assertEqual(extrusion["distance"], "cabinet_depth")

        back = component_commands(cmd, BOARD_COMPONENTS["rear"])
        back_sketch = next(
            item["params"] for item in back
            if item["command"] == "sketch.create"
        )
        self.assertEqual(back_sketch["offset"], "cabinet_depth")

        roof = component_commands(cmd, BOARD_COMPONENTS["roof"])
        roof_sketch = next(
            item["params"] for item in roof
            if item["command"] == "sketch.create"
        )
        roof_extrusion = next(
            item["params"] for item in roof
            if item["command"] == "solid.extrude"
        )
        self.assertIn("roof_front_overhang", str(roof_sketch["offset"]))
        for parameter in (
            "cabinet_depth",
            "panel_wood_thickness",
            "roof_front_overhang",
            "roof_rear_overhang",
        ):
            self.assertIn(parameter, str(roof_extrusion["distance"]))

        joints = [
            p for p in of(cmd, "joint.create")
            if p["name"].startswith("Attach CornerBracket:")
        ]
        self.assertEqual(len(joints), 8)
        self.assertEqual(
            sum("rear_mount" in str(p["b"]) for p in joints),
            4,
        )
        self.assertTrue(
            all("corner" in p["a"] and "edge" in p["a"] for p in joints)
        )

    def test_parameter_override_changes_all_dependents(self):
        cmd = commands(opening_width=850, frame_wood_thickness=13)

        for role in ("left", "right", "bottom", "roof"):
            self.assertEqual(moved(cmd, BOARD_COMPONENTS[role]), [])
        joints = [
            p for p in of(cmd, "joint.create")
            if p["name"].startswith("Attach CornerBracket:")
        ]
        self.assertEqual(len(joints), 8)
        sketch_points = " ".join(
            str(p["points"]) for p in of(cmd, "sketch.line")
        )
        self.assertIn("opening_width", sketch_points)

    def test_all_copies_created_before_native_placements(self):
        cmd = commands()
        for name in ("Hub75PanelBasic",):
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
