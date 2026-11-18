#!/usr/bin/env python3
"""Own the Plate commands used by the tool.cad.ci migration proof.

This file lives with Plate because the model folder owns its qualification
behaviour. The temporary compare-current step proves that tool.cad.ci produces
the same command document as the existing CAD pipeline before that pipeline is
replaced.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ITEM = Path(__file__).resolve().parent
ROOT = ITEM.parents[2]


def output_root() -> Path:
    """Return the item output directory supplied by tool.cad.ci."""

    value = os.environ.get("CAD_CI_OUTPUT")
    if not value:
        raise RuntimeError("CAD_CI_OUTPUT is required")
    return Path(value)


def generated_commands() -> Path:
    """Return the canonical command file produced by the new Plate item."""

    return output_root() / "generated" / "scpf" / "solidcraft.json"


def _read_json(path: Path) -> dict:
    """Read a JSON object and include its path when validation fails."""

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"missing Plate file: {path}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"Plate JSON must contain an object: {path}")
    return data


def _write_check(name: str, data: dict) -> None:
    """Write one small, inspectable proof below the Plate item output."""

    target = output_root() / "checks" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _sha256(path: Path) -> str:
    """Return the content hash recorded in comparison evidence."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def compile_model() -> None:
    """Compile the real Plate source to the item-owned generated path."""

    target = generated_commands()
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "scpf",
            str(ITEM / "scpf" / "model.py"),
            "--out",
            str(target),
        ],
        cwd=ROOT,
        check=True,
    )


def verify_reference() -> None:
    """Require generated commands to match the reviewed Plate reference."""

    generated = generated_commands()
    reference = ITEM / "scpf" / "reference.json"
    if _read_json(generated) != _read_json(reference):
        raise RuntimeError("tool.cad.ci Plate commands differ from scpf/reference.json")

    _write_check(
        "reference.json",
        {
            "schema": 1,
            "model": "plate",
            "status": "pass",
            "generated_sha256": _sha256(generated),
            "reference": "scpf/reference.json",
            "reference_sha256": _sha256(reference),
        },
    )


def compare_current_pipeline() -> None:
    """Prove the new item output equals the current pipeline output byte-for-byte."""

    generated = generated_commands()
    current = ROOT / "output" / "models" / "plate" / "scpf" / "solidcraft.json"
    if generated.read_bytes() != current.read_bytes():
        raise RuntimeError(
            "tool.cad.ci Plate commands differ from current CAD pipeline output"
        )

    _write_check(
        "current-pipeline.json",
        {
            "schema": 1,
            "model": "plate",
            "status": "pass",
            "generated_sha256": _sha256(generated),
            "current_pipeline_sha256": _sha256(current),
        },
    )


def main() -> int:
    """Run one named Plate qualification step."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("compile", "verify", "compare-current"),
    )
    args = parser.parse_args()

    if args.command == "compile":
        compile_model()
    elif args.command == "verify":
        verify_reference()
    else:
        compare_current_pipeline()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
