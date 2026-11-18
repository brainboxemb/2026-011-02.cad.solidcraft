"""Regression checks for the independent HUB75Display2 design."""

import ast
from pathlib import Path
import tempfile
import unittest

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "advanced" / "hub75_display2"
SCPF_DIR = MODEL_ROOT / "scpf"
MODEL = SCPF_DIR / "model.py"


def commands(**overrides):
    if not overrides:
        return run_script(MODEL)["commands"]

    text = MODEL.read_text(encoding="utf-8")
    args = ", ".join(f"{key}={value!r}" for key, value in overrides.items())
    changed = text.rstrip() + f"\n\nHUB75Display2({args})\n"

    handle = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        prefix="_hub75_display2_test_",
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


class HUB75Display2Tests(unittest.TestCase):
    def test_v2_has_its_own_model_local_source_tree(self):
        classes = [
            node.name
            for node in ast.parse(MODEL.read_text(encoding="utf-8")).body
            if isinstance(node, ast.ClassDef)
        ]
        self.assertEqual(classes, ["HUB75Display2"])

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

        # One additional Board component is introduced for the unfilleted
        # intermediate shelf. Left and right remain copies of one side board.
        self.assertEqual(len(creates), 14)
        self.assertIn("Board 5", creates)

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
