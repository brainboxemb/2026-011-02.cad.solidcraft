"""Regression checks for the independent WoodenHub75BoxIter2 design."""

import ast
from pathlib import Path
import tempfile
import unittest

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "advanced" / "hub75_wood_frame_iter2"
SCPF_DIR = MODEL_ROOT / "scpf"
MODEL = SCPF_DIR / "model.py"


def commands(**overrides):
    if not overrides:
        return run_script(MODEL)["commands"]

    text = MODEL.read_text(encoding="utf-8")
    args = ", ".join(f"{key}={value!r}" for key, value in overrides.items())
    changed = text.rstrip() + f"\n\nWoodenHub75BoxIter2({args})\n"

    handle = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        prefix="_hub75_wood_frame_iter2_test_",
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


def of(rows, command):
    return [
        row["params"]
        for row in rows
        if row["command"] == command
    ]


def moved(rows, prefix):
    return [
        row for row in of(rows, "occurrence.move")
        if row["occurrence"].startswith(prefix)
    ]


class WoodenHub75BoxIter2Tests(unittest.TestCase):
    def test_v2_has_its_own_model_local_source_tree(self):
        classes = [
            node.name
            for node in ast.parse(MODEL.read_text(encoding="utf-8")).body
            if isinstance(node, ast.ClassDef)
        ]
        self.assertEqual(classes, ["WoodenHub75BoxIter2"])

        self.assertEqual(
            {path.name for path in (SCPF_DIR / "assemblies").glob("*.py")},
            {
                "corner_brackets.py",
                "glass_frame.py",
                "hub75_panels.py",
                "side_handles.py",
                "wood_frame.py",
            },
        )
        self.assertEqual(
            {path.name for path in (SCPF_DIR / "parts").glob("*.py")},
            {
                "board.py",
                "glass_strip.py",
                "roundwood_handle.py",
                "side_board.py",
                "window.py",
            },
        )

        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SCPF_DIR.glob("**/*.py")
        )
        self.assertNotIn("hub75_wood_frame", source)

    def test_native_parameters_include_lower_compartment_height(self):
        parameter_names = {
            row["name"] for row in of(commands(), "parameters.add")
        }
        self.assertEqual(
            parameter_names,
            {
                "opening_width",
                "opening_height",
                "lower_compartment_height",
                "frame_wood_thickness",
                "panel_wood_thickness",
                "cabinet_depth",
                "side_panel_depth",
                "panel_recess_depth",
                "roof_front_overhang",
                "roof_rear_overhang",
                "corner_radius",
                "side_recess_depth",
                "side_recess_radius",
                "side_recess_lower_keep",
                "side_recess_upper_keep",
                "bracket_width",
                "glazing_wood_width",
                "glazing_wood_depth",
            },
        )

    def test_12_mm_wood_and_70_mm_compartment_make_94_mm_opening_datum(self):
        source = MODEL.read_text(encoding="utf-8")
        frame_source = (
            SCPF_DIR / "assemblies" / "wood_frame.py"
        ).read_text(encoding="utf-8")

        self.assertIn("frame_wood_thickness = 12.0", source)
        self.assertIn("lower_compartment_height = 70.0", source)
        self.assertIn(
            "2 * self.frame_wood_thickness\n            + self.lower_compartment_height",
            source,
        )
        self.assertIn(
            "shelf_bottom = bottom_top + self.lower_compartment_height",
            frame_source,
        )
        self.assertIn(
            "opening_bottom = shelf_bottom + self.frame_wood_thickness",
            frame_source,
        )

    def test_lower_compartment_parameter_moves_display_consumers(self):
        rows = commands(lower_compartment_height=90.0)

        panels = moved(rows, "$hub75panelbasic")
        self.assertEqual(len(panels), 5)
        self.assertTrue(
            all("lower_compartment_height" in str(row["translate"][2]) for row in panels)
        )

        window = moved(rows, "$window")
        self.assertEqual(len(window), 1)
        self.assertIn(
            "lower_compartment_height",
            str(window[0]["translate"][2]),
        )

        strips = [
            row for row in of(rows, "occurrence.move")
            if row["occurrence"].startswith("$glassstrip")
        ]
        self.assertEqual(len(strips), 4)
        self.assertTrue(
            all("lower_compartment_height" in str(row["translate"][2]) for row in strips)
        )

    def test_frame_contains_intermediate_shelf_and_longer_sidewalls(self):
        rows = commands()
        creates = [row["name"] for row in of(rows, "component.create")]

        # The intermediate shelf adds one Board shape. The two equal lower
        # dividers share one additional Board shape and become two occurrences.
        self.assertEqual(len(creates), 15)

        frame_source = (
            SCPF_DIR / "assemblies" / "wood_frame.py"
        ).read_text(encoding="utf-8")
        shelf_start = frame_source.index('name="intermediate_shelf"')
        shelf_end = frame_source.index(').group("WoodBoxFrame")', shelf_start)
        shelf_source = frame_source[shelf_start:shelf_end]
        self.assertIn("width=self.opening_width", shelf_source)
        self.assertNotIn("width=outer_width", shelf_source)

        moves = of(rows, "occurrence.move")
        shelf = [row for row in moves if row["occurrence"] == "$intermediate_shelf"]
        self.assertEqual(len(shelf), 1)
        self.assertIn("lower_compartment_height", str(shelf[0]["translate"][2]))

        sides = [
            row for row in moves
            if row["occurrence"] in {"$left", "$right"}
        ]
        self.assertEqual(len(sides), 2)
        self.assertTrue(
            all("frame_wood_thickness" in str(row["translate"][2]) for row in sides)
        )

        dividers = [
            row for row in moves
            if row["occurrence"] in {
                "$lower_divider_left",
                "$lower_divider_right",
            }
        ]
        self.assertEqual(len(dividers), 2)
        self.assertTrue(
            all(
                "opening_width" in str(row["translate"][0])
                and "frame_wood_thickness" in str(row["translate"][0])
                for row in dividers
            )
        )

        # The rear board is intentionally disabled during the current
        # iteration-2 layout work.
        self.assertFalse(
            any(row["occurrence"] == "$rear" for row in moves)
        )
        self.assertTrue(
            all(
                "frame_wood_thickness" in str(row["translate"][2])
                for row in dividers
            )
        )

    def test_lower_compartment_clear_bays_are_30_40_30(self):
        frame_source = (
            SCPF_DIR / "assemblies" / "wood_frame.py"
        ).read_text(encoding="utf-8")

        self.assertIn("LOWER_SIDE_BAY_FRACTION = 0.30", frame_source)
        self.assertIn("LOWER_CENTER_BAY_FRACTION = 0.40", frame_source)
        self.assertIn(
            "self.opening_width\n            - 2 * self.frame_wood_thickness",
            frame_source,
        )

        # Default geometry: 844 mm internal width minus two 12 mm dividers
        # leaves 820 mm of clear bay width: 246 / 328 / 246 mm.
        clear_width = 844.0 - 2 * 12.0
        self.assertEqual(clear_width * 0.30, 246.0)
        self.assertEqual(clear_width * 0.40, 328.0)
        self.assertEqual(
            844.0 / 2 - 246.0 - 12.0 / 2,
            170.0,
        )

    def test_side_walls_follow_v11_rear_recess_principle(self):
        source = MODEL.read_text(encoding="utf-8")
        frame_source = (
            SCPF_DIR / "assemblies" / "wood_frame.py"
        ).read_text(encoding="utf-8")
        side_source = (
            SCPF_DIR / "parts" / "side_board.py"
        ).read_text(encoding="utf-8")

        self.assertIn("side_panel_depth = 110.0", source)
        self.assertIn("side_recess_depth = 50.0", source)
        self.assertIn("side_recess_radius = 20.0", source)
        self.assertIn("side_recess_lower_keep = 80.0", source)
        self.assertIn("side_recess_upper_keep = 80.0", source)

        # The assembly derives the recess from the top of the intermediate
        # shelf and from the roof, so changing the vertical stack keeps both
        # 80 mm full-depth end zones.
        self.assertIn(
            "self.lower_compartment_height\n            + self.frame_wood_thickness",
            frame_source,
        )
        self.assertIn(
            "side_height\n            - self.side_recess_upper_keep",
            frame_source,
        )
        self.assertIn("depth=self.side_panel_depth", frame_source)

        # The side part uses one real rounded YZ cut, not a faceted polygon.
        # The sketch is attached to the SideBoard body because Forge #354
        # currently blocks standalone sketch extrusions as boolean operands.
        self.assertIn('name="Rear recess"', side_source)
        self.assertIn("on=body", side_source)
        self.assertIn('plane="YZ"', side_source)
        self.assertIn("RoundedRectangle2D(", side_source)
        self.assertIn("self.recess_radius", side_source)

        # Default local geometry:
        # shelf top 82 mm; +80 mm = recess starts at 162 mm.
        # side height 444 mm; -80 mm = recess ends at 364 mm.
        self.assertEqual(70.0 + 12.0 + 80.0, 162.0)
        self.assertEqual(70.0 + 12.0 + 362.0 - 80.0, 364.0)

    def test_side_handle_is_flush_with_rear_and_fills_recess_height(self):
        rows = commands()
        moves = of(rows, "occurrence.move")

        rods = [
            row for row in moves
            if row["occurrence"] in {
                "$left_handle_rod",
                "$right_handle_rod",
            }
        ]
        self.assertEqual(len(rods), 2)

        # Ø22 radius is 11 mm. With a 110 mm side-panel depth, Y=99 puts the
        # rear surface of the rod exactly flush with the rear panel edge.
        self.assertTrue(all(row["translate"][1] == 99.0 for row in rods))

        # No mounting hardware is part of this first ergonomic study.
        self.assertFalse(
            any("socket" in row["occurrence"] for row in moves)
        )

        handle_source = (
            SCPF_DIR / "assemblies" / "side_handles.py"
        ).read_text(encoding="utf-8")
        self.assertIn("ROD_DIAMETER = 22.0", handle_source)
        self.assertIn(
            "self.side_panel_depth - half(ROD_DIAMETER)",
            handle_source,
        )
        self.assertIn(
            "rod_length = recess_top_z - recess_bottom_z",
            handle_source,
        )

    def test_five_panel_x_layout_is_unchanged(self):
        panels = moved(commands(), "$hub75panelbasic")
        self.assertEqual(len(panels), 5)
        self.assertEqual(
            sorted(row["translate"][0] for row in panels),
            [-320.0, -160.0, 0.0, 160.0, 320.0],
        )

    def test_top_brackets_follow_complete_vertical_stack(self):
        brackets = moved(commands(), "$cornerbracket")
        self.assertEqual(len(brackets), 8)

        top = [
            row for row in brackets
            if "opening_height" in str(row["translate"][2])
        ]
        self.assertEqual(len(top), 4)
        self.assertTrue(
            all(
                "lower_compartment_height" in str(row["translate"][2])
                and "frame_wood_thickness" in str(row["translate"][2])
                for row in top
            )
        )

        bottom = [
            row for row in brackets
            if row["translate"][2] == 0
        ]
        self.assertEqual(len(bottom), 4)


if __name__ == "__main__":
    unittest.main()
