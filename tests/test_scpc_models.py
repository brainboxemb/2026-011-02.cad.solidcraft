"""Compare independently written SCPF and SCPC native command plans.

Equality of commands is a useful first regression, not proof of correct
physical geometry. Native CI also runs and evaluates BOTH designs.
"""
from pathlib import Path
import unittest

from scpf.runner import run_script as forge_script
from scpc import load_script as native_script

ROOT = Path(__file__).resolve().parents[1]


class ParallelModelTests(unittest.TestCase):
    def test_plate_and_corner_bracket_have_independent_native_scripts(self):
        for slug, base in (
            ("plate", ROOT / "models/basic/plate"),
            ("corner-bracket", ROOT / "models/component-examples/corner-bracket"),
        ):
            with self.subTest(slug=slug):
                forge = base / "scpf/model.py"
                native = base / "scpc/model.py"
                self.assertTrue(forge.is_file())
                self.assertTrue(native.is_file())
                source = native.read_text(encoding="utf-8")
                self.assertIn("script.add(", source)
                self.assertNotIn("from scpf", source)
                self.assertNotIn("scpf.runner", source)
                self.assertNotIn("json.load", source)
                self.assertNotIn("run_script", source)
                scpc_doc = native_script(native).to_dict()
                scpf_doc = forge_script(forge)
                self.assertEqual(scpc_doc, scpf_doc)
                self.assertEqual(len(scpc_doc["commands"]), 12 if slug == "plate" else 17)


if __name__ == "__main__":
    unittest.main()
