#!/usr/bin/env python3
"""Run selected cheap CAD CI work from one build-plan JSON file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from model_catalog import source_path
from model_checks import command_check


ROOT = Path(__file__).resolve().parents[2]


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def compile_models(plan: dict, output_root: Path) -> None:
    for slug in plan["scpf_models"]:
        target = output_root / "models" / slug / "scpf" / "solidcraft.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        run([
            sys.executable,
            "-m",
            "scpf",
            str(source_path(ROOT, slug)),
            "--out",
            str(target),
        ])
        command_check(slug, target)

    for slug in plan["scpc_models"]:
        target = output_root / "models" / slug / "scpc" / "solidcraft.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        run([
            sys.executable,
            "-m",
            "scpc",
            str(source_path(ROOT, slug, "scpc")),
            "--out",
            str(target),
        ])


def run_unit_tests() -> None:
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])


def build_site(
    *,
    plan: dict,
    output_root: Path,
    previous_site: Path,
    source_sha: str,
) -> None:
    if not plan["site_refresh"]:
        return
    site = output_root / "site"
    run([
        sys.executable,
        "scripts/ci/build-results.py",
        "--generated",
        str(output_root / "models"),
        "--previous-site",
        str(previous_site),
        "--commit",
        source_sha,
        "--out",
        str(site),
    ])
    run([
        sys.executable,
        "scripts/ci/test-results.py",
        str(site),
        source_sha,
    ])


def execute(
    *,
    plan_path: Path,
    output_root: Path,
    previous_site: Path,
    source_sha: str,
) -> dict:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("schema") != 1:
        raise ValueError("unsupported CAD build-plan schema")
    compile_models(plan, output_root)
    run_unit_tests()
    build_site(
        plan=plan,
        output_root=output_root,
        previous_site=previous_site,
        source_sha=source_sha,
    )
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--previous-site", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()
    execute(
        plan_path=args.plan,
        output_root=args.out,
        previous_site=args.previous_site,
        source_sha=args.source_sha,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
