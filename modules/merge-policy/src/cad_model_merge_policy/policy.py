"""Classify allowed branch integrations."""

class MergePolicyError(RuntimeError):
    """Branch integration violates project policy."""


def is_main_governance(*, head: str, base: str) -> bool:
    """Return whether this is the narrow main-owned governance-docs lane."""

    return base == "main" and head.startswith("docs/")


def merge_method(*, head: str, base: str) -> str:
    if base == "dev" and head not in {"main", "dev"}:
        return "squash"
    if (head, base) in {("dev", "main"), ("main", "dev")}:
        return "merge"
    if is_main_governance(head=head, base=base):
        return "squash"
    raise MergePolicyError(f"unsupported branch integration: {head} -> {base}")
