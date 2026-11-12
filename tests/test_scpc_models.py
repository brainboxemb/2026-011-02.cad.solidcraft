"""Compare independently written SCPF and SCPC native command plans.

Command-plan comparison catches accidental divergence, but SCPF may keep a
dimension symbolic where SCPC writes the equivalent native literal. Native CI
also executes and evaluates both designs, which remains the geometry proof.
"""
from copy import deepcopy
from pathlib import Path
import unittest

from scpf.runner import run_script as forge_script
from scpc import load_script as native_script

ROOT = Path(__file__).resolve().parents[1]


def resolve_fillet_radius(document):
    """Normalize only the intentional symbolic-vs-literal fillet difference."""
    result = deepcopy(document)
    parameters = {
        command["params"]["name"]: float(command["params"]["expression"])
        for command in result["commands"]
        if command["command"] == "parameters.add"
    }
    for command in result["commands"]:
        if command["command"] != "solid.fillet":
            continue
        radius = command["params"].get("radius")
        if isinstance(radius, str) and radius in parameters:
            command["params"]["radius"] = parameters[radius]
    return result


class ParallelModelTests(unittest.TestCase):
    def test_plate_and_corner_bracket_have_independent_native_scripts(self):
        for slug, base in (
            ("plate", ROOT / "models/basic/plate"),
            ("corner-bracket", ROOT / "models/components/corner-bracket"),
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

                # Plate currently lowers identically. CornerBracket deliberately
                # differs only because Forge preserves inside_corner_radius as
                # an editable named CAD parameter in solid.fillet, while the
                # independent SCPC script writes the same current value (4).
                self.assertEqual(
                    resolve_fillet_radius(scpc_doc),
                    resolve_fillet_radius(scpf_doc),
                )
                self.assertEqual(
                    len(scpc_doc["commands"]),
                    12 if slug == "plate" else 17,
                )


if __name__ == "__main__":
    unittest.main()
