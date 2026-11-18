#!/usr/bin/env python3
"""Run the complete selected CAD check pipeline from event metadata.

The current CAD pipeline remains authoritative during change 0012. The
pipeline also handles catalog growth before site generation and, in parallel,
runs Plate through the pinned tool.cad.ci release as the first migration proof.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import build_plan
import cad_ci
import native_ci
from model_catalog import MODELS, model_build_path, model_slugs
from output_store import migrate_legacy_store_layout
from select_models import parse_models


ROOT = Path(__file__).resolve().parents[2]
ZERO_SHA = "0" * 40
TOOL_CAD_CI = ROOT / "ext" / "cad-ci" / "cad-ci.py"


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


def missing_stable_models(stable_store: Path) -> tuple[str, ...]:
    """Return current native catalog models absent from the stable build store.

    A verification file proves that one stored model is complete. A directory
    without that file still counts as missing.
    """

    return tuple(
        slug
        for slug in model_slugs("native")
        if not (
            stable_store
            / model_build_path(slug)
            / "verification.json"
        ).is_file()
    )


def extend_plan_for_missing_stable(plan: dict, stable_store: Path) -> dict:
    """Add missing stable models to every build kind they support."""

    missing = set(missing_stable_models(stable_store))
    if not missing:
        return plan

    result = dict(plan)
    kinds = {
        "scpf_models": "scpf",
        "scpc_models": "scpc",
        "native_models": "native",
        "snapshot_models": "native-snapshot-required",
    }
    for key, kind in kinds.items():
        eligible = set(model_slugs(kind))
        selected = set(plan.get(key, ())) | (missing & eligible)

        # Keep catalog order so generated plans stay stable and readable.
        result[key] = [
            slug for slug in MODELS
            if slug in selected
        ]

    # Filling a stable-store gap changes both technical output and the site.
    result["site_refresh"] = True
    result["publishable"] = True
    return result


def _tool_selection_args(
    *,
    mode: str,
    models: str,
    base_sha: str,
    head_sha: str,
    paths: tuple[str, ...],
) -> list[str] | None:
    """Translate the current CAD selection to the one-item migration proof."""

    if mode == "models":
        # A deliberate named-model run must not unexpectedly execute Plate.
        if "plate" not in parse_models(models):
            return None
        return ["--item", "plate"]

    if mode == "all":
        # The temporary root cad-ci.yml currently contains only Plate.
        return []

    if base_sha and base_sha != ZERO_SHA:
        return ["--base", base_sha, "--head", head_sha]

    # Initial pushes can have a zero/missing base revision. The current planner
    # already calculated the changed paths, so reuse those exact paths.
    return ["--changed", *paths]


def run_tool_cad_ci_proof(
    *,
    mode: str,
    models: str,
    base_sha: str,
    head_sha: str,
    paths: tuple[str, ...],
    output_root: Path,
) -> tuple[str, ...]:
    """Plan and run Plate through the pinned external tool.

    The plan is stored beside normal diagnostics. Plate itself compares its
    command document with both the reviewed reference and the current pipeline.
    """

    if not TOOL_CAD_CI.is_file():
        raise FileNotFoundError(
            "missing ext/cad-ci/cad-ci.py; run scripts/ci/bootstrap_cad_ci.py"
        )

    selection = _tool_selection_args(
        mode=mode,
        models=models,
        base_sha=base_sha,
        head_sha=head_sha,
        paths=paths,
    )
    output_root.mkdir(parents=True, exist_ok=True)
    plan_path = output_root / "tool-cad-ci-plan.json"

    if selection is None:
        plan_path.write_text("[]\n", encoding="utf-8")
        return ()

    common = ["--repo", str(ROOT), *selection]
    plan_text = subprocess.check_output(
        [
            sys.executable,
            str(TOOL_CAD_CI),
            "plan",
            *common,
            "--json",
        ],
        cwd=ROOT,
        text=True,
    )
    plan = json.loads(plan_text)
    if not isinstance(plan, list):
        raise RuntimeError("tool.cad.ci plan did not return a list")
    plan_path.write_text(
        json.dumps(plan, indent=2) + "\n",
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            str(TOOL_CAD_CI),
            "run",
            *common,
        ],
        cwd=ROOT,
        check=True,
    )
    return tuple(str(row["id"]) for row in plan)


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
    """Run current CAD checks plus the temporary tool.cad.ci Plate proof."""

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

    with tempfile.TemporaryDirectory(prefix="cad-build-baseline-") as temp:
        stable_store = resolve_build_baseline(
            build_root,
            Path(temp) / "build",
        )

        # Catalog growth must be fixed before cheap/native work and site
        # generation. The Plate proof then compares against that same run.
        plan = extend_plan_for_missing_stable(plan, stable_store)
        plan_path.write_text(
            json.dumps(plan, indent=2) + "\n",
            encoding="utf-8",
        )

        cad_ci.execute(
            plan_path=plan_path,
            output_root=output_root,
            previous_site=previous_site,
            source_sha=head_sha,
            build_site_output=False,
        )

        # Run the new Plate item after the old cheap compile so compare-current
        # can prove both command documents are identical.
        run_tool_cad_ci_proof(
            mode=mode,
            models=models,
            base_sha=base_sha,
            head_sha=head_sha,
            paths=paths,
            output_root=output_root,
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
    """Parse workflow metadata and run the same pipeline used by local checks."""

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
