"""Load branch cleanup policy from root ci.yml."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


class CleanupConfigError(ValueError):
    """Cleanup configuration is invalid."""


@dataclass(frozen=True)
class CleanupConfig:
    stable: str
    development: str
    temporary_prefixes: tuple[str, ...]
    experimental: str = "exp"

    @property
    def permanent(self) -> frozenset[str]:
        return frozenset({self.stable, self.development, self.experimental})


def load_config(repo: Path) -> CleanupConfig:
    path = repo / "ci.yml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema") != 1:
        raise CleanupConfigError(f"invalid root config: {path}")
    branches = data.get("branches")
    if not isinstance(branches, dict):
        raise CleanupConfigError(f"branches must be a mapping: {path}")
    stable = branches.get("stable")
    development = branches.get("development")
    experimental = branches.get("experimental")
    prefixes = branches.get("temporary_prefixes")
    if not all(
        isinstance(value, str)
        for value in (stable, development, experimental)
    ):
        raise CleanupConfigError(
            f"stable/development/experimental branches must be strings: {path}"
        )
    if (
        not isinstance(prefixes, list)
        or not prefixes
        or not all(isinstance(value, str) and value for value in prefixes)
    ):
        raise CleanupConfigError(f"temporary_prefixes must be a non-empty list: {path}")
    return CleanupConfig(
        stable,
        development,
        tuple(prefixes),
        experimental=experimental,
    )
