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


def normalize_native_plan(document):
    """Normalize representation details that do not change the native design."""
    result = deepcopy(document)
    parameters = {
        command["params"]["name"]: float(command["params"]["expression"])
        for command in result["commands"]
        if command["command"] == "parameters.add"
    }

    parameter_commands = sorted(
        (
            command for command in result["commands"]
            if command["command"] == "parameters.add"
        ),
        key=lambda command: command["params"]["name"],
    )
    feature_commands = [
        command for command in result["commands"]
        if command["command"] != "parameters.add"
    ]

    for command in feature_commands:
        params = command["params"]
        if command["command"] == "solid.fillet":
            radius = params.get("radius")
            if isinstance(radius, str) and radius in parameters:
                params["radius"] = parameters[radius]

        # A positioned XZ sketch at the component origin is equivalent to
        # the unpositioned default plane used by the independent SCPC script.
        if command["command"] == "sketch.create" and params.get("offset") == 0:
            params.pop("offset")

    result["commands"] = parameter_commands + feature_commands
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

                # Compare the native design, not incidental parameter-add
                # ordering. The independent SCPC script and Forge model must
                # still describe the same parameters, sketch and features.
                self.assertEqual(
                    normalize_native_plan(scpc_doc),
                    normalize_native_plan(scpf_doc),
                )
                self.assertEqual(
                    len(scpc_doc["commands"]),
                    12 if slug == "plate" else 17,
                )


if __name__ == "__main__":
    unittest.main()
