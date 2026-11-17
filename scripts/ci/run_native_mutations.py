#!/usr/bin/env python3
"""Run saved-design native parameter mutations declared in native_cases.py."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from native_cases import NATIVE_MUTATIONS


def run(command):
    subprocess.run(command, check=True)


def mutation_commands(changes):
    return {
        "commands": [
            {
                "command": "parameters.change",
                "params": {"name": name, "expression": expression},
            }
            for name, expression in changes.items()
        ]
    }


def run_mutations(root: Path):
    for slug, mutations in NATIVE_MUTATIONS.items():
        model_root = root / slug
        source = model_root / "model.sc"
        if not source.is_file():
            raise FileNotFoundError(source)

        for mutation in mutations:
            name = mutation["name"]
            command_file = model_root / f"change-{name}.json"
            saved = model_root / f"model-{name}.sc"
            measurements = model_root / f"measurements-{name}.json"

            command_file.write_text(
                json.dumps(mutation_commands(mutation["changes"]), indent=2) + "\n",
                encoding="utf-8",
            )
            run([
                "solidcraft-cli",
                "run",
                str(command_file),
                "--in",
                str(source),
                "--param-check",
                "strict",
                "--save",
                str(saved),
            ])
            run([
                "solidcraft-cli",
                "eval",
                str(saved),
                "--json-out",
                str(measurements),
            ])
            print(f"{slug}: mutation {name} complete")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("native_root", type=Path)
    args = parser.parse_args()
    run_mutations(args.native_root)


if __name__ == "__main__":
    main()
