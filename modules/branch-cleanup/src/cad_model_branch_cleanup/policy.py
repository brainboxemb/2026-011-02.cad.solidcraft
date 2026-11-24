"""Pure cleanup eligibility rules."""

from __future__ import annotations

from .config import CleanupConfig


def is_temporary(branch: str, config: CleanupConfig) -> bool:
    if branch in config.permanent:
        return False
    return branch.startswith(config.temporary_prefixes)


def eligible_post_merge(
    *,
    head: str,
    base: str,
    same_repository: bool,
    merged: bool,
    config: CleanupConfig,
) -> bool:
    return (
        merged
        and same_repository
        and base == config.development
        and is_temporary(head, config)
    )


def eligible_sweep(
    *,
    branch: str,
    has_open_pr: bool,
    has_merged_pr_to_development: bool,
    config: CleanupConfig,
) -> bool:
    return (
        is_temporary(branch, config)
        and not has_open_pr
        and has_merged_pr_to_development
    )
