"""Classify allowed branch integrations."""

class MergePolicyError(RuntimeError):
    """Branch integration violates project policy."""


def is_main_governance(*, head: str, base: str) -> bool:
    """Return whether this is the narrow main-owned governance-docs lane."""

    return base == "main" and head.startswith("docs/")


def merge_method(*, head: str, base: str) -> str:
    permanent = {"main", "dev", "exp"}
    if base in {"dev", "exp"} and head not in permanent:
        return "squash"
    if (head, base) in {
        ("dev", "main"),
        ("main", "dev"),
        ("dev", "exp"),
        ("exp", "dev"),
    }:
        return "merge"
    if is_main_governance(head=head, base=base):
        return "squash"
    raise MergePolicyError(f"unsupported branch integration: {head} -> {base}")
