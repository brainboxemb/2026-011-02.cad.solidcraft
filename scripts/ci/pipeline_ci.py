#!/usr/bin/env python3
"""Run the complete selected CAD check pipeline from event metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import build_plan
import cad_ci
import native_ci
from output_store import migrate_legacy_store_layout
from select_models import parse_models


ROOT = Path(__file__).resolve().parents[2]


def configure_git_workspace() -> None:
    """Allow the container user to inspect the mounted Actions checkout."""
    subprocess.run(
        ["git", "config", "--global", "--add", "safe.directory", str(ROOT)],
        cwd=ROOT,
        check=True,
    )


def resolve_build_baseline(build_root: Path, destination: Path) -> Path:
    """Create a read-only resolved build copy for this CI run."""
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(
        build_root,
        destination,
        ignore=shutil.ignore_patterns(".git"),
    )
    if not (destination / "main").is_dir():
        migrate_legacy_store_layout(store=destination)
    if not (destination / "main").is_dir():
        raise RuntimeError(
            "build branch has neither build/main nor a complete legacy stable store"
        )
    return destination / "main"


def execute(
    *,
    mode: str,
    models: str,
    base_sha: str,
    head_sha: str,
    event_name: str,
    ref_name: str,
    pull_request: int | None,
    output_root: Path,
    build_root: Path,
    previous_site: Path,
    workflow_run: str,
    image_reference: str,
) -> dict:
    configure_git_workspace()
    paths = (
        build_plan.changed_paths(base_sha, head_sha)
        if mode == "changed"
        else ()
    )
    plan = build_plan.make_plan(
        mode=mode,
        models=parse_models(models),
        paths=paths,
        event_name=event_name,
        ref_name=ref_name,
        pull_request=pull_request,
    )
    output_root.mkdir(parents=True, exist_ok=True)
    plan_path = output_root / "plan.json"
    plan_path.write_text(
        json.dumps(plan, indent=2) + "\n",
        encoding="utf-8",
    )

    with tempfile.TemporaryDirectory(prefix="cad-build-baseline-") as temp:
        stable_store = resolve_build_baseline(
            build_root,
            Path(temp) / "build",
        )
        cad_ci.execute(
            plan_path=plan_path,
            output_root=output_root,
            previous_site=previous_site,
            source_sha=head_sha,
            build_site_output=False,
        )
        native_ci.execute(
            plan_path=plan_path,
            output_root=output_root,
            stable_store=stable_store,
            previous_site=previous_site,
            source_sha=head_sha,
            workflow_run=workflow_run,
            image_reference=image_reference,
        )
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("changed", "models", "all"), default="changed")
    parser.add_argument("--models", default="")
    parser.add_argument("--base-sha", default="")
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--event-name", required=True)
    parser.add_argument("--ref-name", required=True)
    parser.add_argument("--pull-request", type=int, default=0)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--build-root", type=Path, required=True)
    parser.add_argument("--previous-site", type=Path, required=True)
    parser.add_argument("--workflow-run", required=True)
    parser.add_argument("--image-reference", required=True)
    args = parser.parse_args()

    execute(
        mode=args.mode,
        models=args.models,
        base_sha=args.base_sha,
        head_sha=args.head_sha,
        event_name=args.event_name,
        ref_name=args.ref_name,
        pull_request=args.pull_request or None,
        output_root=args.out,
        build_root=args.build_root,
        previous_site=args.previous_site,
        workflow_run=args.workflow_run,
        image_reference=args.image_reference,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
