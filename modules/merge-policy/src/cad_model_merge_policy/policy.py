"""Classify allowed branch integrations."""

class MergePolicyError(RuntimeError):
    """Branch integration violates project policy."""


def merge_method(*, head: str, base: str) -> str:
    if base == "dev" and head not in {"main", "dev"}:
        return "squash"
    if (head, base) in {("dev", "main"), ("main", "dev")}:
        return "merge"
    raise MergePolicyError(f"unsupported branch integration: {head} -> {base}")
