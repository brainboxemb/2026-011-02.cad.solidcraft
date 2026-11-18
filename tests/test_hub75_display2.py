"""Regression checks for the independent HUB75Display2 baseline."""

import ast
from pathlib import Path
import unittest

from scpf.runner import run_script


ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = ROOT / "models" / "advanced" / "hub75-display2"
SCPF_DIR = MODEL_ROOT / "scpf"
MODEL = SCPF_DIR / "model.py"


def commands():
    return run_script(MODEL)["commands"]


def of(rows, command):
    return [
        row["params"]
        for row in rows
        if row["command"] == command
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

    def test_initial_native_parameter_baseline_is_frozen(self):
        parameter_names = {
            row["name"] for row in of(commands(), "parameters.add")
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

    def test_initial_component_and_occurrence_baseline_is_frozen(self):
        rows = commands()
        creates = [row["name"] for row in of(rows, "component.create")]
        self.assertEqual(len(creates), 13)

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
            "Window",
            "GlassStrip",
            "GlassStrip 2",
            "CornerBracket",
        ):
            self.assertIn(name, creates)

        copies = of(rows, "occurrence.copy")
        expected = {
            "Hub75PanelBasic": 4,
            "Board": 1,
            "GlassStrip": 1,
            "GlassStrip 2": 1,
            "CornerBracket": 7,
        }
        for name, count in expected.items():
            self.assertEqual(
                sum(row["component"] == name for row in copies),
                count,
                name,
            )

    def test_initial_five_panel_layout_is_frozen(self):
        rows = commands()
        panels = [
            row for row in of(rows, "occurrence.move")
            if row["occurrence"].startswith("$hub75panelbasic")
        ]
        self.assertEqual(len(panels), 5)
        self.assertEqual(
            sorted(row["translate"][0] for row in panels),
            [-320.0, -160.0, 0.0, 160.0, 320.0],
        )
        self.assertTrue(
            all("panel_recess_depth" in str(row["translate"][1]) for row in panels)
        )
        self.assertTrue(
            all("opening_height" in str(row["translate"][2]) for row in panels)
        )

    def test_initial_eight_bracket_layout_is_frozen(self):
        rows = commands()
        brackets = [
            row for row in of(rows, "occurrence.move")
            if row["occurrence"].startswith("$cornerbracket")
        ]
        self.assertEqual(len(brackets), 8)
        self.assertEqual(
            sum("cabinet_depth" in str(row["translate"][1]) for row in brackets),
            4,
        )
        self.assertEqual(
            sum("opening_height" in str(row["translate"][2]) for row in brackets),
            4,
        )


if __name__ == "__main__":
    unittest.main()
