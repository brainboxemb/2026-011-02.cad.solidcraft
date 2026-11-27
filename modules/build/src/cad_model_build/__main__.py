"""CLI entrypoint for one resolved repository CAD build batch."""

from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import execute


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--model", action="append", default=[])
    parser.add_argument("--solidcraft-image")
    parser.add_argument("--solidcraft-version")
    args = parser.parse_args(argv)

    path = execute(
        repo=args.repo,
        namespace=args.namespace,
        selected_ids=tuple(args.model),
        solidcraft_image=args.solidcraft_image,
        solidcraft_version=args.solidcraft_version,
    )
    print(f"CAD build plan: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
