#!/usr/bin/env python3
"""Create one tested CAD CI build plan from event metadata and model selection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess

from model_catalog import MODELS
from select_models import (
    PIPELINE_SMOKE_MODEL,
    needs_pipeline_smoke,
    needs_site_refresh,
    parse_models,
    select_models,
)


ROOT = Path(__file__).resolve().parents[2]
ZERO_SHA = "0" * 40
PUBLIC_SITE = "https://brainboxemb.github.io/2026-011-02.cad.solidcraft"


def safe_branch_key(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip(".-")
    if not value:
        raise ValueError("branch name must contain a usable character")
    return value.lower()


def publication_target(
    *,
    event_name: str,
    ref_name: str,
    pull_request: int | None = None,
) -> dict:
    if event_name == "pull_request":
        if not pull_request:
            raise ValueError("pull_request event requires PR number")
        channel = "preview"
        preview_key = f"pr-{pull_request}"
    elif event_name == "push" and ref_name == "main":
        channel = "stable"
        preview_key = ""
    elif event_name == "workflow_dispatch" and ref_name == "main":
        channel = "stable"
        preview_key = ""
    else:
        channel = "preview"
        preview_key = f"branch-{safe_branch_key(ref_name)}"

    public_base = (
        PUBLIC_SITE
        if channel == "stable"
        else f"{PUBLIC_SITE}/preview/{preview_key}"
    )
    return {
        "channel": channel,
        "preview_key": preview_key,
        "public_base": public_base,
    }


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
    event_name: str = "workflow_dispatch",
    ref_name: str = "local",
    pull_request: int | None = None,
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
    if mode == "changed" and needs_pipeline_smoke(paths):
        for kind in selections:
            smoke_models = select_models(
                mode="models",
                kind=kind,
                models=(PIPELINE_SMOKE_MODEL,),
            )
            selections[kind] = tuple(
                slug
                for slug in MODELS
                if slug in set(selections[kind]) | set(smoke_models)
            )

    target = publication_target(
        event_name=event_name,
        ref_name=ref_name,
        pull_request=pull_request,
    )
    site_refresh = needs_site_refresh(paths, selections["scpf"])
    return {
        "schema": 1,
        "mode": mode,
        "changed_paths": list(paths),
        "scpf_models": list(selections["scpf"]),
        "scpc_models": list(selections["scpc"]),
        "native_models": list(selections["native"]),
        "snapshot_models": list(selections["native-snapshot-required"]),
        "site_refresh": site_refresh,
        "publishable": bool(selections["native"]) or site_refresh,
        **target,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("changed", "models", "all"), default="changed")
    parser.add_argument("--models", default="")
    parser.add_argument("--base", default="")
    parser.add_argument("--head", required=True)
    parser.add_argument("--event-name", default="workflow_dispatch")
    parser.add_argument("--ref-name", default="local")
    parser.add_argument("--pull-request", type=int)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    paths = changed_paths(args.base, args.head) if args.mode == "changed" else ()
    result = make_plan(
        mode=args.mode,
        models=parse_models(args.models),
        paths=paths,
        event_name=args.event_name,
        ref_name=args.ref_name,
        pull_request=args.pull_request,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("Changed paths:")
    for path in result["changed_paths"]:
        print(f"  - {path}")
    for key in ("scpf_models", "scpc_models", "native_models", "snapshot_models"):
        print(f"{key}: " + (" ".join(result[key]) if result[key] else "none"))
    print(f"site_refresh: {str(result['site_refresh']).lower()}")
    print(f"publishable: {str(result['publishable']).lower()}")
    print(f"publication: {result['channel']} {result['preview_key']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
