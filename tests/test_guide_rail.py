"""Regression checks for the reusable GuideRail component."""
from pathlib import Path
import tempfile
import unittest

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "models" / "components" / "guide_rail" / "scpf" / "model.py"
MAKITA = ROOT / "models" / "components" / "guide_rail" / "scpf" / "makita.py"


def profile_points(commands):
    line = next(c for c in commands if c["command"] == "sketch.line")
    return line["params"]["points"]


def envelope(points):
    xs = [float(p[0]) for p in points]
    zs = [float(p[1]) for p in points]
    return max(xs) - min(xs), max(zs) - min(zs)


class GuideRailTests(unittest.TestCase):
    def test_festool_is_default_and_length_is_only_native_parameter(self):
        commands = run_script(COMPONENT)["commands"]

        params = [
            command["params"]["name"]
            for command in commands
            if command["command"] == "parameters.add"
        ]
        self.assertEqual(params, ["length"])

        points = profile_points(commands)
        self.assertEqual(len(points), 59)
        width, height = envelope(points)
        self.assertAlmostEqual(width, 184.20)
        self.assertAlmostEqual(height, 10.50)

    def test_makita_variant_reuses_same_component_with_measured_profile(self):
        commands = run_script(MAKITA)["commands"]

        params = [
            command["params"]
            for command in commands
            if command["command"] == "parameters.add"
        ]
        self.assertEqual(
            [(row["name"], row["expression"]) for row in params],
            [("length", "1500")],
        )

        points = profile_points(commands)
        self.assertEqual(len(points), 99)
        width, height = envelope(points)
        self.assertAlmostEqual(width, 182.50)
        self.assertAlmostEqual(height, 10.28)

        self.assertEqual(
            sum(c["command"] == "component.create" for c in commands),
            0,
        )

    def test_length_override_remains_native_parameter(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "model.py"
            script.write_text(
                "from models.components.guide_rail.scpf.model import GuideRail\n"
                "GuideRail(length=1080)\n",
                encoding="utf-8",
            )
            commands = run_script(script)["commands"]

        parameter = next(
            c["params"]
            for c in commands
            if c["command"] == "parameters.add"
        )
        self.assertEqual(parameter, {
            "name": "length",
            "expression": "1080",
            "unit": "mm",
        })

        extrude = next(
            c["params"]
            for c in commands
            if c["command"] == "solid.extrude"
        )
        self.assertEqual(extrude["distance"], "length")
        self.assertEqual(extrude["direction"], "symmetric")

    def test_profile_choice_is_not_a_native_parameter(self):
        source = COMPONENT.read_text(encoding="utf-8")
        self.assertIn('@component(include=("length",))', source)
        self.assertIn("profile = None", source)
        self.assertIn('get_profile(self.profile or "festool")', source)

        for script in (COMPONENT, MAKITA):
            commands = run_script(script)["commands"]
            names = [
                command["params"]["name"]
                for command in commands
                if command["command"] == "parameters.add"
            ]
            self.assertEqual(names, ["length"])

    def test_unknown_profile_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "model.py"
            script.write_text(
                "from models.components.guide_rail.scpf.model import GuideRail\n"
                'GuideRail(profile="unknown")\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "unknown guide rail profile"):
                run_script(script)


if __name__ == "__main__":
    unittest.main()
