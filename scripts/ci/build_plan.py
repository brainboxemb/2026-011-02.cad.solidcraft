#!/usr/bin/env python3
"""Create one tested CAD CI build plan from event metadata and model selection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from select_models import needs_site_refresh, parse_models, select_models


ROOT = Path(__file__).resolve().parents[2]
ZERO_SHA = "0" * 40


def changed_paths(base: str, head: str, *, root: Path = ROOT) -> tuple[str, ...]:
    if not head:
        raise ValueError("head commit is required")
    if base and base != ZERO_SHA:
        command = ["git", "diff", "--name-only", base, head, "--"]
    else:
        command = ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", head]
    completed = subprocess.run(
        command,
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip()
    )


def make_plan(
    *,
    mode: str,
    models: tuple[str, ...] = (),
    paths: tuple[str, ...] = (),
) -> dict:
    selections = {
        kind: select_models(
            mode=mode,
            kind=kind,
            changed_paths=paths,
            models=models,
        )
        for kind in (
            "scpf",
            "scpc",
            "native",
            "native-snapshot-required",
        )
    }
    return {
        "schema": 1,
        "mode": mode,
        "changed_paths": list(paths),
        "scpf_models": list(selections["scpf"]),
        "scpc_models": list(selections["scpc"]),
        "native_models": list(selections["native"]),
        "snapshot_models": list(selections["native-snapshot-required"]),
        "site_refresh": needs_site_refresh(paths, selections["scpf"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("changed", "models", "all"), default="changed")
    parser.add_argument("--models", default="")
    parser.add_argument("--base", default="")
    parser.add_argument("--head", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    paths = changed_paths(args.base, args.head) if args.mode == "changed" else ()
    result = make_plan(
        mode=args.mode,
        models=parse_models(args.models),
        paths=paths,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("Changed paths:")
    for path in result["changed_paths"]:
        print(f"  - {path}")
    for key in ("scpf_models", "scpc_models", "native_models", "snapshot_models"):
        print(f"{key}: " + (" ".join(result[key]) if result[key] else "none"))
    print(f"site_refresh: {str(result['site_refresh']).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
