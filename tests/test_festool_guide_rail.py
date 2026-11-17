"""Regression checks for the reusable Festool guide rail component."""
from pathlib import Path
import tempfile
import unittest

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "models" / "components" / "festool_guide_rail" / "scpf" / "model.py"


class FestoolGuideRailTests(unittest.TestCase):
    def test_length_is_the_only_adjustable_parameter(self):
        commands = run_script(COMPONENT)["commands"]
        params = [
            command["params"]["name"]
            for command in commands
            if command["command"] == "parameters.add"
        ]
        self.assertEqual(params, ["length"])

    def test_profile_uses_tso_envelope_dimensions(self):
        commands = run_script(COMPONENT)["commands"]
        line = next(c for c in commands if c["command"] == "sketch.line")
        points = line["params"]["points"]
        xs = [float(p[0]) for p in points]
        zs = [float(p[1]) for p in points]
        self.assertAlmostEqual(max(xs) - min(xs), 184.20)
        self.assertAlmostEqual(max(zs) - min(zs), 10.50)

    def test_default_length_and_override_remain_native_parameter(self):
        commands = run_script(COMPONENT)["commands"]
        self.assertEqual(commands[0]["params"]["expression"], "1400")
        extrude = next(c for c in commands if c["command"] == "solid.extrude")
        self.assertEqual(extrude["params"]["distance"], "length")

        with tempfile.TemporaryDirectory() as directory:
            source = COMPONENT.read_text(encoding="utf-8")
            script = Path(directory) / "model.py"
            script.write_text(source + "\nFestoolGuideRail(length=1080)\n", encoding="utf-8")
            changed = run_script(script)["commands"]
        self.assertEqual(changed[0]["params"]["expression"], "1080")
        changed_extrude = next(c for c in changed if c["command"] == "solid.extrude")
        self.assertEqual(changed_extrude["params"]["distance"], "length")


if __name__ == "__main__":
    unittest.main()
