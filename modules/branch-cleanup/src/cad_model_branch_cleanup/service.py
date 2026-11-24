"""Execute automatic and manual branch cleanup."""

from __future__ import annotations

from .config import CleanupConfig
from .policy import eligible_post_merge, eligible_sweep


def post_merge_cleanup(
    client,
    *,
    head: str,
    base: str,
    same_repository: bool,
    merged: bool,
    config: CleanupConfig,
) -> bool:
    if not eligible_post_merge(
        head=head,
        base=base,
        same_repository=same_repository,
        merged=merged,
        config=config,
    ):
        return False
    client.delete_branch(head)
    return True


def sweep(client, *, config: CleanupConfig) -> tuple[str, ...]:
    deleted: list[str] = []
    for branch in client.branches():
        if eligible_sweep(
            branch=branch,
            has_open_pr=client.open_pr_exists(branch),
            has_merged_pr_to_development=client.merged_pr_to(
                branch, config.development
            ),
            config=config,
        ):
            client.delete_branch(branch)
            deleted.append(branch)
    return tuple(deleted)
