"""Regression checks for the reusable guide rail component."""
from pathlib import Path
import tempfile
import unittest

from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "models" / "components" / "guide_rail" / "scpf" / "model.py"


class GuideRailTests(unittest.TestCase):
    def test_length_is_the_only_adjustable_parameter(self):
        commands = run_script(COMPONENT)["commands"]
        params = [
            command["params"]["name"]
            for command in commands
            if command["command"] == "parameters.add"
        ]
        self.assertEqual(params, ["length"])

    def test_profile_uses_tso_dimensions(self):
        commands = run_script(COMPONENT)["commands"]
        line = next(c for c in commands if c["command"] == "sketch.line")
        points = line["params"]["points"]

        xs = sorted({round(float(p[0]), 6) for p in points})
        zs = [float(p[1]) for p in points]

        self.assertAlmostEqual(xs[-1] - xs[0], 184.20)
        self.assertAlmostEqual(max(zs) - min(zs), 10.50)

        left_outer_l = 0.0
        left_inner_l = 3.90
        left_inner_r = 12.20
        left_outer_r = 16.10
        for x in (left_outer_l, left_inner_l, left_inner_r, left_outer_r):
            self.assertIn(x, xs)
        self.assertAlmostEqual(left_outer_r - left_outer_l, 16.10)
        self.assertAlmostEqual(left_inner_r - left_inner_l, 8.30)

        center_outer_l = 48.10
        center_inner_l = 52.00
        center_inner_r = 60.30
        center_outer_r = 64.20
        for x in (center_outer_l, center_inner_l, center_inner_r, center_outer_r):
            self.assertIn(x, xs)
        self.assertAlmostEqual(center_outer_r - center_outer_l, 16.10)
        self.assertAlmostEqual(center_inner_r - center_inner_l, 8.30)
        self.assertAlmostEqual(center_outer_r - left_outer_l, 64.20)

    def test_default_length_and_override_remain_native_parameter(self):
        commands = run_script(COMPONENT)["commands"]
        self.assertEqual(commands[0]["params"]["expression"], "1400")
        extrude = next(c for c in commands if c["command"] == "solid.extrude")
        self.assertEqual(extrude["params"]["distance"], "length")

        with tempfile.TemporaryDirectory() as directory:
            source = COMPONENT.read_text(encoding="utf-8")
            script = Path(directory) / "model.py"
            script.write_text(source + "\nGuideRail(length=1080)\n", encoding="utf-8")
            changed = run_script(script)["commands"]
        self.assertEqual(changed[0]["params"]["expression"], "1080")
        changed_extrude = next(c for c in changed if c["command"] == "solid.extrude")
        self.assertEqual(changed_extrude["params"]["distance"], "length")


if __name__ == "__main__":
    unittest.main()
