"""CLI entrypoint for one resolved repository CAD build batch."""

from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import execute


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--source-ref")
    parser.add_argument("--model", action="append", default=[])
    parser.add_argument("--forge-ref")
    args = parser.parse_args(argv)

    path = execute(
        repo=args.repo,
        namespace=args.namespace,
        source_ref=args.source_ref,
        selected_ids=tuple(args.model),
        forge_ref=args.forge_ref,
    )
    print(f"CAD build plan: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
