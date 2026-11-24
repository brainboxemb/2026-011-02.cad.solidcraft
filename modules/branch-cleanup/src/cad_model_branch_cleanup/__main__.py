"""CLI for automatic post-merge cleanup and manual stale-branch sweep."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from .config import load_config
from .github import GitHubClient
from .service import post_merge_cleanup, sweep


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    sub = parser.add_subparsers(dest="command", required=True)

    post = sub.add_parser("post-merge")
    post.add_argument("--head", required=True)
    post.add_argument("--base", required=True)
    post.add_argument("--head-repository", required=True)
    post.add_argument("--merged", action="store_true")

    sub.add_parser("sweep")
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN is required")

    config = load_config(Path.cwd())
    client = GitHubClient(args.repository, token)

    if args.command == "post-merge":
        changed = post_merge_cleanup(
            client,
            head=args.head,
            base=args.base,
            same_repository=args.head_repository == args.repository,
            merged=args.merged,
            config=config,
        )
        print("deleted" if changed else "kept")
        return

    for branch in sweep(client, config=config):
        print(branch)


if __name__ == "__main__":
    main()
