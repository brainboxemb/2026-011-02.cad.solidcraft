#!/usr/bin/env python3
"""Remove one closed PR's build overlay and Pages preview with tool.cad.ci."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


def tool_path(source_root: Path) -> Path:
    """Return the pinned publication tool bootstrapped inside the source tree."""

    path = source_root / "ext" / "cad-ci" / "cad-ci.py"
    if not path.is_file():
        raise RuntimeError("missing pinned ext/cad-ci checkout")
    return path


def run_tool(source_root: Path, *args: str) -> None:
    """Run one cleanup mutation through the generic publication tool."""

    subprocess.run(
        [sys.executable, str(tool_path(source_root)), *args],
        cwd=source_root,
        check=True,
    )


def execute(*, source_root: Path, pull_request: int) -> None:
    """Remove only the requested PR namespaces from generated branches."""

    if pull_request < 1:
        raise ValueError("pull request number must be positive")

    # The workflow checks trusted cleanup code out below source/. Resolve that
    # path once so the tool path and its cwd cannot apply "source" twice.
    source_root = source_root.resolve()
    common = ["--repo", str(source_root), "--pull-request", str(pull_request)]
    run_tool(
        source_root,
        "publish",
        "build-cleanup",
        *common,
        "--message",
        f"Remove CAD build PR #{pull_request}",
    )
    run_tool(
        source_root,
        "publish",
        "pages-cleanup",
        *common,
        "--message",
        f"Remove CAD preview PR #{pull_request}",
    )


def main() -> int:
    """Parse the trusted closed-PR event and run scoped cleanup."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--pull-request", type=int, required=True)
    args = parser.parse_args()
    execute(
        source_root=args.source_root,
        pull_request=args.pull_request,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
