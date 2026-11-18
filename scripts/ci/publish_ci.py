#!/usr/bin/env python3
"""Publish verified CAD item output with the pinned tool.cad.ci release.

CAD still owns model verification, catalog rules, HTML content and CSS. This
module only translates the CAD build plan into generic tool.cad.ci build-store
and Pages commands, then asks the CAD site generator to render the resolved
technical result.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


PUBLIC_SITE = "https://brainboxemb.github.io/2026-011-02.cad.solidcraft"


def read_json(path: Path) -> object:
    """Read one required JSON file and return its decoded value."""

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"missing publication input: {path}") from exc


def tool_path(source_root: Path) -> Path:
    """Return the exact external tool entry point bootstrapped by the workflow."""

    path = source_root / "ext" / "cad-ci" / "cad-ci.py"
    if not path.is_file():
        raise RuntimeError(
            "missing ext/cad-ci/cad-ci.py; run bootstrap_cad_ci.py first"
        )
    return path


def run_tool(source_root: Path, *args: str) -> None:
    """Run one pinned tool.cad.ci command against this source checkout."""

    subprocess.run(
        [sys.executable, str(tool_path(source_root)), *args],
        cwd=source_root,
        check=True,
    )


def selected_items(bundle: Path) -> tuple[str, ...]:
    """Return item IDs from the exact tool plan executed by the CAD pipeline."""

    data = read_json(bundle / "tool-cad-ci-plan.json")
    if not isinstance(data, list):
        raise RuntimeError("tool-cad-ci-plan.json must contain a list")
    result: list[str] = []
    for row in data:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise RuntimeError("tool-cad-ci-plan.json contains an invalid item")
        if row["id"] not in result:
            result.append(row["id"])
    return tuple(result)


def validate_source(
    *,
    source_root: Path,
    workflow_event: str,
    workflow_head_branch: str,
    workflow_head_sha: str,
    plan: dict,
    pull_request: int,
) -> None:
    """Reject publication metadata that does not describe this exact checkout."""

    actual = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=source_root,
        text=True,
    ).strip()
    if actual != workflow_head_sha:
        raise RuntimeError(
            f"source checkout {actual} does not match {workflow_head_sha}"
        )

    if plan.get("channel") == "stable":
        if workflow_head_branch != "main":
            raise RuntimeError("stable publication is only allowed from main")
        if workflow_event not in {"push", "workflow_dispatch"}:
            raise RuntimeError(
                "stable publication requires a main push or manual main run"
            )
        return

    if workflow_event == "pull_request":
        if pull_request < 1 or plan.get("preview_key") != f"pr-{pull_request}":
            raise RuntimeError("PR preview metadata does not match the pull request")


def build_site(
    *,
    source_root: Path,
    stable_store: Path,
    previous_site: Path,
    out: Path,
    source_commit: str,
    public_base: str,
) -> Path:
    """Render and smoke-test the CAD website from one complete build view."""

    if out.exists():
        shutil.rmtree(out)
    subprocess.run(
        [
            sys.executable,
            str(source_root / "scripts/ci/build-results.py"),
            "--stable-store",
            str(stable_store),
            "--previous-site",
            str(previous_site),
            "--public-base",
            public_base,
            "--commit",
            source_commit,
            "--out",
            str(out),
        ],
        cwd=source_root,
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(source_root / "scripts/ci/test-results.py"),
            str(out),
            source_commit,
            public_base,
        ],
        cwd=source_root,
        check=True,
    )
    return out


def _tool_common(
    source_root: Path,
    workflow_head_branch: str,
    workflow_head_sha: str,
) -> list[str]:
    """Return source-freshness arguments shared by every generated push."""

    return [
        "--repo",
        str(source_root),
        "--source-ref",
        workflow_head_branch,
        "--expected-source",
        workflow_head_sha,
    ]


def execute(
    *,
    bundle: Path,
    source_root: Path,
    build_root: Path,
    pages_root: Path,
    workflow_event: str,
    workflow_head_branch: str,
    workflow_head_sha: str,
    pull_request: int,
) -> bool:
    """Prepare the complete build view, render CAD Pages and publish both.

    The first generic publication creates build/main from every local item.
    Later main runs replace only selected items with `build update-main`.
    PRs publish a sparse overlay and render their site from overlay + main.
    """

    plan = read_json(bundle / "plan.json")
    if not isinstance(plan, dict) or plan.get("schema") != 1:
        raise RuntimeError("plan.json has an unsupported schema")
    if not plan.get("publishable"):
        print("CAD plan has no publishable change.")
        return False

    validate_source(
        source_root=source_root,
        workflow_event=workflow_event,
        workflow_head_branch=workflow_head_branch,
        workflow_head_sha=workflow_head_sha,
        plan=plan,
        pull_request=pull_request,
    )

    # tool.cad.ci has a deliberate stable + PR-preview publication contract.
    # A manually dispatched non-main branch still runs all checks, but does not
    # create a second ad-hoc Pages namespace outside that contract.
    if plan.get("channel") == "preview" and workflow_event != "pull_request":
        print("Manual branch preview checked successfully; durable publish skipped.")
        return False

    items = selected_items(bundle)
    candidate_root = source_root / "build"
    generic_main = build_root / "main"
    has_generic_main = (generic_main / "build.json").is_file()
    work = bundle / "tool-publication"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    common = _tool_common(
        source_root,
        workflow_head_branch,
        workflow_head_sha,
    )

    if plan["channel"] == "stable":
        publish_main = False
        if has_generic_main:
            if items:
                complete = work / "main"
                run_tool(
                    source_root,
                    "build",
                    "update-main",
                    "--repo",
                    str(source_root),
                    "--main",
                    str(generic_main),
                    "--candidate-root",
                    str(candidate_root),
                    "--out",
                    str(complete),
                    "--source-commit",
                    workflow_head_sha,
                    "--items",
                    *items,
                )
                publish_main = True
            else:
                complete = generic_main
        else:
            # The cutover commit changes every model-root ci.yml, so the local
            # candidate is complete. prepare-main will fail if any item is
            # missing instead of publishing a partial baseline.
            complete = work / "main"
            run_tool(
                source_root,
                "build",
                "prepare-main",
                "--repo",
                str(source_root),
                "--candidate-root",
                str(candidate_root),
                "--out",
                str(complete),
                "--source-commit",
                workflow_head_sha,
            )
            publish_main = True

        if publish_main:
            run_tool(
                source_root,
                "publish",
                "build",
                *common,
                "--candidate",
                str(complete),
                "--scope",
                "main",
                "--message",
                f"Publish CAD build/main at {workflow_head_sha}",
            )

        site = build_site(
            source_root=source_root,
            stable_store=complete,
            previous_site=pages_root,
            out=work / "site",
            source_commit=workflow_head_sha,
            public_base=PUBLIC_SITE,
        )
        run_tool(
            source_root,
            "publish",
            "pages",
            *common,
            "--site",
            str(site),
            "--message",
            f"Publish stable CAD site at {workflow_head_sha}",
        )
        return True

    if pull_request < 1:
        raise RuntimeError("PR preview requires a positive pull request number")

    overlay: Path | None = None
    if items:
        overlay = work / "pr"
        run_tool(
            source_root,
            "build",
            "prepare-pr",
            "--repo",
            str(source_root),
            "--candidate-root",
            str(candidate_root),
            "--out",
            str(overlay),
            "--source-commit",
            workflow_head_sha,
            "--pull-request",
            str(pull_request),
            "--items",
            *items,
        )
        run_tool(
            source_root,
            "publish",
            "build",
            *common,
            "--candidate",
            str(overlay),
            "--scope",
            "pr",
            "--pull-request",
            str(pull_request),
            "--message",
            f"Publish CAD build PR #{pull_request} at {workflow_head_sha}",
        )

    if has_generic_main:
        if overlay is None:
            complete = generic_main
        else:
            complete = work / "resolved"
            run_tool(
                source_root,
                "build",
                "resolve",
                "--main",
                str(generic_main),
                "--overlay",
                str(overlay),
                "--out",
                str(complete),
            )
    else:
        # First cutover PR: every model-root item is selected, so the local
        # build can also provide the complete preview view.
        complete = work / "resolved"
        run_tool(
            source_root,
            "build",
            "prepare-main",
            "--repo",
            str(source_root),
            "--candidate-root",
            str(candidate_root),
            "--out",
            str(complete),
            "--source-commit",
            workflow_head_sha,
        )

    public_base = f"{PUBLIC_SITE}/previews/pr-{pull_request}"
    site = build_site(
        source_root=source_root,
        stable_store=complete,
        previous_site=pages_root,
        out=work / "site",
        source_commit=workflow_head_sha,
        public_base=public_base,
    )
    run_tool(
        source_root,
        "publish",
        "pages",
        *common,
        "--site",
        str(site),
        "--pull-request",
        str(pull_request),
        "--message",
        f"Publish CAD preview PR #{pull_request} at {workflow_head_sha}",
    )
    return True


def main() -> int:
    """Parse workflow metadata and run the consumer-side publication flow."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--build-root", type=Path, required=True)
    parser.add_argument("--pages-root", type=Path, required=True)
    parser.add_argument("--workflow-event", required=True)
    parser.add_argument("--workflow-head-branch", required=True)
    parser.add_argument("--workflow-head-sha", required=True)
    parser.add_argument("--pull-request", type=int, default=0)
    args = parser.parse_args()
    execute(
        bundle=args.bundle,
        source_root=args.source_root,
        build_root=args.build_root,
        pages_root=args.pages_root,
        workflow_event=args.workflow_event,
        workflow_head_branch=args.workflow_head_branch,
        workflow_head_sha=args.workflow_head_sha,
        pull_request=args.pull_request,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
