#!/usr/bin/env python3
"""Run the selected CAD checks and package model-root tool.cad.ci items.

CAD owns model selection and native verification. The pinned tool executes each
selected physical model-root item after native verification and writes the item
state consumed by the host-side build/Pages publisher.
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
from model_catalog import MODELS, model_slugs
from model_item import item_id_for_slug, stored_model_paths
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
    """Copy the accepted generic build baseline for read-only pipeline use.

    The one-time legacy migration is complete. A missing tool.cad.ci manifest is
    now a real repository error instead of a signal to rebuild old layouts.
    """

    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(
        build_root,
        destination,
        ignore=shutil.ignore_patterns(".git"),
    )
    main = destination / "main"
    if not (main / "build.json").is_file():
        raise RuntimeError(
            "build branch is missing the tool.cad.ci build/main baseline"
        )
    return main


def missing_stable_models(stable_store: Path) -> tuple[str, ...]:
    """Return current native catalog models absent from the stable build store.

    A verification file proves that one stored model is complete. A directory
    without that file still counts as missing.
    """

    missing: list[str] = []
    for slug in model_slugs("native"):
        try:
            stored_model_paths(stable_store, slug)
        except RuntimeError:
            missing.append(slug)
    return tuple(missing)


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


def _tool_selection_groups(
    *,
    mode: str,
    models: str,
    base_sha: str,
    head_sha: str,
    paths: tuple[str, ...],
) -> tuple[tuple[str, ...], ...]:
    """Translate CAD selection modes to one or more tool.cad.ci selections.

    Normal changed/all runs need one tool invocation. Named-model mode can name
    several catalog variants that share a model-root item, so duplicate item
    IDs are removed before one exact-item invocation per root.
    """

    if mode == "models":
        item_ids: list[str] = []
        for slug in parse_models(models):
            item_id = item_id_for_slug(slug)
            if item_id not in item_ids:
                item_ids.append(item_id)
        return tuple(("--item", item_id) for item_id in item_ids)

    if mode == "all":
        return ((),)

    if base_sha and base_sha != ZERO_SHA:
        return (("--base", base_sha, "--head", head_sha),)

    return (("--changed", *paths),)


def run_tool_cad_ci_items(
    *,
    mode: str,
    models: str,
    base_sha: str,
    head_sha: str,
    paths: tuple[str, ...],
    output_root: Path,
) -> tuple[str, ...]:
    """Run selected model-root items through the pinned external tool.

    Each item compiles every catalog variant owned by its folder, compares the
    new command JSON with current-run or accepted stable output, and packages
    verified native output produced earlier in this pipeline run.
    """

    if not TOOL_CAD_CI.is_file():
        raise FileNotFoundError(
            "missing ext/cad-ci/cad-ci.py; run scripts/ci/bootstrap_cad_ci.py"
        )

    selections = _tool_selection_groups(
        mode=mode,
        models=models,
        base_sha=base_sha,
        head_sha=head_sha,
        paths=paths,
    )
    output_root.mkdir(parents=True, exist_ok=True)
    plan_path = output_root / "tool-cad-ci-plan.json"

    combined: list[dict] = []
    seen: set[str] = set()
    for selection in selections:
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

        for row in plan:
            if not isinstance(row, dict) or not isinstance(row.get("id"), str):
                raise RuntimeError("tool.cad.ci plan contains an invalid item")
            if row["id"] not in seen:
                seen.add(row["id"])
                combined.append(row)

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

    plan_path.write_text(
        json.dumps(combined, indent=2) + "\n",
        encoding="utf-8",
    )
    return tuple(str(row["id"]) for row in combined)


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
    """Run current CAD checks, native verification and model-root packaging."""

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

        # Catalog growth must be fixed before cheap/native work. Model-root
        # items then package fresh native output against this same baseline.
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

        native_ci.execute(
            plan_path=plan_path,
            output_root=output_root,
            source_sha=head_sha,
            workflow_run=workflow_run,
            image_reference=image_reference,
        )

        # Run the model-root items only after native verification. Their final
        # package step can then use fresh candidate output or a stable sibling.
        run_tool_cad_ci_items(
            mode=mode,
            models=models,
            base_sha=base_sha,
            head_sha=head_sha,
            paths=paths,
            output_root=output_root,
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
