#!/usr/bin/env python3
"""Remove one closed PR's generated CAD build and Pages preview."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil

from publish_ci import commit_and_push


def execute(*, build_root: Path, pages_root: Path, pull_request: int) -> None:
    if pull_request < 1:
        raise ValueError("pull request number must be positive")

    build_target = build_root / "pr" / str(pull_request)
    pages_target = pages_root / "preview" / f"pr-{pull_request}"

    if build_target.exists():
        shutil.rmtree(build_target)
    if pages_target.exists():
        shutil.rmtree(pages_target)

    pr_root = build_root / "pr"
    if pr_root.is_dir() and not any(pr_root.iterdir()):
        pr_root.rmdir()

    preview_root = pages_root / "preview"
    if preview_root.is_dir() and not any(preview_root.iterdir()):
        preview_root.rmdir()

    commit_and_push(
        build_root,
        branch="build",
        message=f"Remove CAD build PR #{pull_request}",
    )
    commit_and_push(
        pages_root,
        branch="gh-pages",
        message=f"Remove CAD preview PR #{pull_request}",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-root", type=Path, required=True)
    parser.add_argument("--pages-root", type=Path, required=True)
    parser.add_argument("--pull-request", type=int, required=True)
    args = parser.parse_args()
    execute(
        build_root=args.build_root,
        pages_root=args.pages_root,
        pull_request=args.pull_request,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
