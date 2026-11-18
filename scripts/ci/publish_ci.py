#!/usr/bin/env python3
"""Publish one verified native CAD bundle to build and gh-pages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from build_plan import PUBLIC_SITE
from model_catalog import model_build_path, model_slugs
from output_store import (
    migrate_legacy_pages,
    migrate_legacy_store_layout,
    promote_candidate,
    prune_removed_models,
)


BUILD_README = """# CAD build output

This branch stores verified technical CAD build output only.

- `main/<source-item-path>/` contains the last promoted successful main build.
- `pr/<number>/<source-item-path>/` contains isolated verified PR output.
- `<source-item-path>` is the catalog source-file path without `.py`, for
  example `models/basic/plate/scpf/model/`.
- Every built model directory carries its own `verification.json`.

The website lives on `gh-pages`. Do not edit generated build output by hand.
"""


def run(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=cwd, check=True)


def load_publish(bundle: Path) -> dict | None:
    path = bundle / "publish.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("channel") not in {"stable", "preview"}:
        raise ValueError("publish bundle has invalid channel")
    if not isinstance(data.get("models"), list):
        raise ValueError("publish bundle has no model list")
    if not data.get("source_commit"):
        raise ValueError("publish bundle has no source commit")
    return data


def validate_publication(
    publish: dict,
    *,
    workflow_event: str,
    workflow_head_branch: str,
    workflow_head_sha: str,
) -> None:
    if publish["source_commit"] != workflow_head_sha:
        raise ValueError(
            "publish source commit does not match producing workflow head"
        )
    if publish["channel"] == "stable":
        if workflow_head_branch != "main":
            raise ValueError("stable publication is only allowed from main")
        if workflow_event not in {"push", "workflow_dispatch"}:
            raise ValueError(
                "stable publication requires a main push or manual main run"
            )
        if publish.get("preview_key"):
            raise ValueError("stable publication cannot have a preview key")
    elif not publish.get("preview_key"):
        raise ValueError("preview publication requires preview_key")


def is_pr_preview(publish: dict) -> bool:
    key = str(publish.get("preview_key", ""))
    return (
        publish.get("channel") == "preview"
        and key.startswith("pr-")
        and key[3:].isdigit()
    )


def stable_complete(build_root: Path) -> bool:
    return all(
        (
            build_root
            / "main"
            / model_build_path(slug)
            / "verification.json"
        ).is_file()
        for slug in model_slugs("native")
    )


def write_build_readme(build_root: Path) -> None:
    (build_root / "README.md").write_text(BUILD_README, encoding="utf-8")


def remove_legacy_build_layout(build_root: Path) -> None:
    for name in ("stable", "previews", "preview"):
        path = build_root / name
        if path.exists():
            shutil.rmtree(path)


def commit_and_push(
    root: Path,
    *,
    branch: str,
    message: str,
    attempts: int = 3,
) -> bool:
    """Commit generated output and retry non-fast-forward publication safely."""
    if attempts < 1:
        raise ValueError("attempts must be positive")

    run(["git", "config", "user.name", "github-actions[bot]"], cwd=root)
    run(
        [
            "git",
            "config",
            "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com",
        ],
        cwd=root,
    )
    run(["git", "add", "-A"], cwd=root)
    changed = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=root,
    ).returncode != 0
    if not changed:
        return False

    run(["git", "commit", "-m", message], cwd=root)

    for attempt in range(1, attempts + 1):
        pushed = subprocess.run(
            ["git", "push", "origin", f"HEAD:{branch}"],
            cwd=root,
            text=True,
            capture_output=True,
        )
        if pushed.returncode == 0:
            return True
        if attempt == attempts:
            detail = (pushed.stderr or pushed.stdout or "").strip()
            raise RuntimeError(
                f"failed to publish {branch} after {attempts} attempts"
                + (f": {detail}" if detail else "")
            )

        run(
            ["git", "fetch", "origin", branch],
            cwd=root,
        )
        run(
            ["git", "rebase", f"origin/{branch}"],
            cwd=root,
        )

    raise AssertionError("unreachable publication retry state")


def replace_stable_pages(site: Path, pages: Path) -> None:
    if not (site / "provenance.json").is_file():
        raise FileNotFoundError("stable site has no provenance.json")
    for child in tuple(pages.iterdir()):
        if child.name in {".git", "preview"}:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    for child in site.iterdir():
        target = pages / child.name
        if child.is_dir():
            shutil.copytree(child, target)
        else:
            shutil.copy2(child, target)


def publish_preview_site(site: Path, pages: Path, preview_key: str) -> None:
    if not (site / "provenance.json").is_file():
        raise FileNotFoundError("preview site has no provenance.json")
    target = pages / "preview" / preview_key
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(site, target)


def build_stable_site(
    *,
    source_root: Path,
    build_root: Path,
    pages_root: Path,
    out: Path,
    source_commit: str,
) -> Path:
    if out.exists():
        shutil.rmtree(out)
    run(
        [
            sys.executable,
            str(source_root / "scripts/ci/build-results.py"),
            "--stable-store",
            str(build_root / "main"),
            "--previous-site",
            str(pages_root),
            "--public-base",
            PUBLIC_SITE,
            "--commit",
            source_commit,
            "--out",
            str(out),
        ],
        cwd=source_root,
    )
    run(
        [
            sys.executable,
            str(source_root / "scripts/ci/test-results.py"),
            str(out),
            source_commit,
            PUBLIC_SITE,
        ],
        cwd=source_root,
    )
    return out


def execute(
    *,
    bundle: Path,
    source_root: Path,
    build_root: Path,
    pages_root: Path,
    workflow_event: str,
    workflow_head_branch: str,
    workflow_head_sha: str,
) -> bool:
    publish = load_publish(bundle)
    if publish is None:
        print("No publish.json; nothing to publish.")
        return False

    validate_publication(
        publish,
        workflow_event=workflow_event,
        workflow_head_branch=workflow_head_branch,
        workflow_head_sha=workflow_head_sha,
    )
    source_commit = publish["source_commit"]
    actual_source = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=source_root,
        text=True,
    ).strip()
    if actual_source != source_commit:
        raise ValueError(
            f"source checkout {actual_source} does not match {source_commit}"
        )

    models = tuple(publish["models"])
    candidate = bundle / "candidate"

    if publish["channel"] == "stable":
        if not stable_complete(build_root):
            migrated = migrate_legacy_store_layout(store=build_root)
            if not migrated:
                migrate_legacy_pages(
                    pages=pages_root,
                    store=build_root,
                    source_root=source_root,
                )
        if models:
            promote_candidate(
                candidate=candidate,
                store=build_root,
                models=models,
                channel="stable",
            )
        prune_removed_models(build_root, channel="stable")
        remove_legacy_build_layout(build_root)
        write_build_readme(build_root)
        if not stable_complete(build_root):
            raise RuntimeError("build/main is incomplete after stable promotion")
        commit_and_push(
            build_root,
            branch="build",
            message=f"Publish build/main at {source_commit}",
        )

        with tempfile.TemporaryDirectory(
            prefix="cad-stable-site-"
        ) as temp:
            stable_site = build_stable_site(
                source_root=source_root,
                build_root=build_root,
                pages_root=pages_root,
                out=Path(temp) / "site",
                source_commit=source_commit,
            )
            replace_stable_pages(stable_site, pages_root)
        commit_and_push(
            pages_root,
            branch="gh-pages",
            message=f"Publish stable CAD site at {source_commit}",
        )
        return True

    preview_key = publish["preview_key"]
    if models and is_pr_preview(publish):
        promote_candidate(
            candidate=candidate,
            store=build_root,
            models=models,
            channel="preview",
            preview_key=preview_key,
        )
        write_build_readme(build_root)
        commit_and_push(
            build_root,
            branch="build",
            message=f"Publish build/{preview_key} at {source_commit}",
        )

    site = bundle / "site"
    publish_preview_site(site, pages_root, preview_key)
    commit_and_push(
        pages_root,
        branch="gh-pages",
        message=f"Publish CAD preview {preview_key} at {source_commit}",
    )
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--build-root", type=Path, required=True)
    parser.add_argument("--pages-root", type=Path, required=True)
    parser.add_argument("--workflow-event", required=True)
    parser.add_argument("--workflow-head-branch", required=True)
    parser.add_argument("--workflow-head-sha", required=True)
    args = parser.parse_args()
    execute(
        bundle=args.bundle,
        source_root=args.source_root,
        build_root=args.build_root,
        pages_root=args.pages_root,
        workflow_event=args.workflow_event,
        workflow_head_branch=args.workflow_head_branch,
        workflow_head_sha=args.workflow_head_sha,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
