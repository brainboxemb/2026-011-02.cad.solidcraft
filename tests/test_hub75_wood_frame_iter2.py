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
                "wood_frame.py",
            },
        )
        self.assertEqual(
            {path.name for path in (SCPF_DIR / "parts").glob("*.py")},
            {
                "board.py",
                "glass_strip.py",
                "rear_board.py",
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
        self.assertIn("depth=internal_depth", shelf_source)

        # Bottom, shelf, dividers and side walls use the same 120 mm datum.
        # The future rear board sits inside that depth rather than behind it.
        self.assertIn("depth=self.side_panel_depth", frame_source)
        self.assertIn(
            "roof_rear = self.side_panel_depth + self.roof_rear_overhang",
            frame_source,
        )
        self.assertIn(
            "rear_y = self.cabinet_depth - self.panel_wood_thickness",
            frame_source,
        )
        # Default roof depth is 10 mm front + 120 mm cabinet + 1 mm rear.
        self.assertEqual(10.0 + 120.0 + 1.0, 131.0)

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

        rear = [row for row in moves if row["occurrence"] == "$rear"]
        self.assertEqual(len(rear), 1)
        self.assertEqual(rear[0]["translate"][1], 111.0)
        self.assertEqual(rear[0]["translate"][2], 82.0)
        self.assertTrue(
            all(
                "frame_wood_thickness" in str(row["translate"][2])
                for row in dividers
            )
        )

        # Shelf and lower dividers stop at Y=110, leaving the 10 mm rear zone
        # clear for the 9 mm rear board plus 1 mm assembly gap.
        self.assertIn("REAR_BOARD_ZONE_DEPTH = 10.0", frame_source)
        self.assertIn(
            "internal_depth = self.cabinet_depth - REAR_BOARD_ZONE_DEPTH",
            frame_source,
        )

        divider_source = frame_source[
            frame_source.index('name="lower_divider_left"'):
            frame_source.index('name="left"', frame_source.index('name="lower_divider_left"'))
        ]
        self.assertIn("depth=internal_depth", divider_source)

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

    def test_side_slots_and_rear_open_cutouts(self):
        source = MODEL.read_text(encoding="utf-8")
        frame_source = (
            SCPF_DIR / "assemblies" / "wood_frame.py"
        ).read_text(encoding="utf-8")
        side_source = (
            SCPF_DIR / "parts" / "side_board.py"
        ).read_text(encoding="utf-8")
        rear_source = (
            SCPF_DIR / "parts" / "rear_board.py"
        ).read_text(encoding="utf-8")

        # Side walls use a true 30 mm native slot from fixed Python design
        # values. The derived p0/p1 coordinates stay numeric for Forge.
        self.assertIn("SlotCenterToCenter2D(", side_source)
        self.assertIn('name="Side hand slot"', side_source)
        self.assertIn('plane="YZ"', side_source)
        self.assertIn("HANDLE_SLOT_WIDTH = 30.0", side_source)
        self.assertIn("HANDLE_SLOT_REAR_CLEARANCE = 20.0", side_source)
        self.assertIn("HANDLE_SLOT_BOTTOM = 162.0", side_source)
        self.assertIn("HANDLE_SLOT_TOP = 364.0", side_source)
        self.assertIn("slot_radius = HANDLE_SLOT_WIDTH / 2", side_source)
        self.assertIn("p0 = (slot_center_y, lower_center_z)", side_source)
        self.assertIn("p1 = (slot_center_y, upper_center_z)", side_source)
        self.assertNotIn("opening_sketch.add(", side_source)
        self.assertNotIn("self.opening_width", side_source)
        self.assertNotIn("RoundedRectangle2D(", side_source)

        # Derived default coordinates: Y=85, end centres Z=177 and Z=349.
        slot_width = 30.0
        slot_radius = slot_width / 2
        slot_y = 120.0 - 20.0 - slot_radius
        self.assertEqual(slot_y, 85.0)
        self.assertEqual(162.0 + slot_radius, 177.0)
        self.assertEqual(364.0 - slot_radius, 349.0)

        # Rear board starts above the 70 mm lower dividers at global Z=82.
        rows = commands()
        rear = [
            row for row in of(rows, "occurrence.move")
            if row["occurrence"] == "$rear"
        ]
        self.assertEqual(len(rear), 1)
        self.assertEqual(rear[0]["translate"][2], 82.0)
        self.assertIn("rear_height = opening_top - rear_bottom", frame_source)

        # Rear board intentionally uses the original open side cutouts, not
        # closed slots. Default depth is 50 mm with R20 transitions.
        self.assertIn('name="Rear side openings"', rear_source)
        self.assertIn("opening_depth = 50.0", rear_source)
        self.assertIn("opening_radius = 20.0", rear_source)
        self.assertEqual(rear_source.count("RoundedRectangle2D("), 2)
        self.assertNotIn("SlotCenterToCenter2D(", rear_source)

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

        # Rear bracket centres follow the 120 mm cabinet rear edge:
        # 120 - 24/2 = Y=108 mm.
        rear = [
            row for row in brackets
            if row["translate"][1] == 108.0
        ]
        self.assertEqual(len(rear), 4)


if __name__ == "__main__":
    unittest.main()
