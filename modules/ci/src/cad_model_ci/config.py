"""Load stable project config and optional branch-local work selection."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess
from typing import Any

import yaml


class ConfigError(ValueError):
    """Repository configuration is missing or invalid."""


_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_VERSION = re.compile(r"^v\d+\.\d+\.\d+$")
_SOLIDCRAFT_VERSION = re.compile(r"^\d+\.\d+\.\d+$")
_SOLIDCRAFT_CANDIDATE_IMAGE = re.compile(
    r"^ghcr\.io/brainboxemb/cad-solidcraft@sha256:[0-9a-f]{64}$"
)


@dataclass(frozen=True)
class ForgeDependency:
    repository: str
    version: str


@dataclass(frozen=True)
class SolidCraftCandidate:
    image: str
    version: str


@dataclass(frozen=True)
class ProjectConfig:
    stable_branch: str
    development_branch: str
    forge: ForgeDependency
    modules_root: Path
    models_root: Path
    output_root: Path


@dataclass(frozen=True)
class BuildSelection:
    branch: str
    modules: tuple[str, ...] | None
    models: tuple[str, ...] | None
    tasks: tuple[str, ...]
    solidcraft_candidate: SolidCraftCandidate | None = None


def full_selection(branch: str) -> BuildSelection:
    return BuildSelection(
        branch=branch,
        modules=None,
        models=None,
        tasks=("test", "build"),
    )


def _mapping(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"missing config: {path}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"invalid YAML: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ConfigError(f"config must be a mapping: {path}")
    return value


def _relative(value: object, field: str, path: Path) -> Path:
    if not isinstance(value, str) or not value:
        raise ConfigError(f"{field} must be a non-empty string: {path}")
    result = Path(value)
    if result.is_absolute() or ".." in result.parts:
        raise ConfigError(f"{field} must remain inside the repository: {path}")
    return result


def _ids(value: object, field: str, path: Path) -> tuple[str, ...] | None:
    if value == "all":
        return None
    if not isinstance(value, list):
        raise ConfigError(f"{field} must be 'all' or a list: {path}")
    if not all(isinstance(item, str) and _ID.fullmatch(item) for item in value):
        raise ConfigError(f"{field} contains an invalid id: {path}")
    return tuple(value)


def _solidcraft_candidate(
    data: dict[str, Any],
    path: Path,
) -> SolidCraftCandidate | None:
    runtime = data.get("runtime")
    if runtime is None:
        return None
    if not isinstance(runtime, dict) or set(runtime) != {"solidcraft"}:
        raise ConfigError(
            f"runtime may contain only solidcraft on a work branch: {path}"
        )
    solidcraft = runtime["solidcraft"]
    if (
        not isinstance(solidcraft, dict)
        or set(solidcraft) != {"image", "version"}
    ):
        raise ConfigError(
            f"runtime.solidcraft must contain image and version: {path}"
        )
    image = solidcraft.get("image")
    version = solidcraft.get("version")
    if (
        not isinstance(image, str)
        or _SOLIDCRAFT_CANDIDATE_IMAGE.fullmatch(image) is None
    ):
        raise ConfigError(
            "runtime.solidcraft.image must be the canonical cad-solidcraft "
            f"image pinned by sha256 digest: {path}"
        )
    if (
        not isinstance(version, str)
        or _SOLIDCRAFT_VERSION.fullmatch(version) is None
    ):
        raise ConfigError(
            f"runtime.solidcraft.version must be X.Y.Z: {path}"
        )
    return SolidCraftCandidate(image=image, version=version)


def load_project(repo: Path) -> ProjectConfig:
    path = repo / "ci.yml"
    data = _mapping(path)
    if data.get("schema") != 1:
        raise ConfigError(f"unsupported schema: {path}")

    branches = data.get("branches")
    dependencies = data.get("dependencies")
    roots = data.get("roots")
    if not all(isinstance(value, dict) for value in (branches, dependencies, roots)):
        raise ConfigError(f"branches, dependencies and roots must be mappings: {path}")

    stable = branches.get("stable")
    development = branches.get("development")
    if not isinstance(stable, str) or not isinstance(development, str):
        raise ConfigError(f"branch names must be strings: {path}")

    forge = dependencies.get("forge")
    if not isinstance(forge, dict):
        raise ConfigError(f"dependencies.forge must be a mapping: {path}")
    repository = forge.get("repository")
    version = forge.get("version")
    if not isinstance(repository, str) or not _REPOSITORY.fullmatch(repository):
        raise ConfigError(f"invalid Forge repository: {path}")
    if not isinstance(version, str) or not _VERSION.fullmatch(version):
        raise ConfigError(f"Forge version must be a v-prefixed release tag: {path}")

    return ProjectConfig(
        stable_branch=stable,
        development_branch=development,
        forge=ForgeDependency(repository, version),
        modules_root=_relative(roots.get("modules"), "roots.modules", path),
        models_root=_relative(roots.get("models"), "roots.models", path),
        output_root=_relative(roots.get("output"), "roots.output", path),
    )


def load_build(repo: Path, branch: str) -> BuildSelection | None:
    path = repo / "build.yml"
    if not path.is_file():
        return None

    data = _mapping(path)
    if data.get("schema") != 1:
        raise ConfigError(f"unsupported schema: {path}")

    configured_branch = data.get("branch")
    if configured_branch != branch:
        return None

    tasks = data.get("tasks")
    if (
        not isinstance(tasks, list)
        or not tasks
        or not all(isinstance(task, str) for task in tasks)
    ):
        raise ConfigError(f"tasks must be a non-empty string list: {path}")
    unsupported = sorted(set(tasks) - {"test", "build"})
    if unsupported:
        raise ConfigError(f"unsupported task(s): {', '.join(unsupported)}")

    return BuildSelection(
        branch=branch,
        modules=_ids(data.get("modules"), "modules", path),
        models=_ids(data.get("models"), "models", path),
        tasks=tuple(tasks),
        solidcraft_candidate=_solidcraft_candidate(data, path),
    )


def current_branch(repo: Path) -> str:
    for key in ("GITHUB_HEAD_REF", "GITHUB_REF_NAME"):
        value = os.environ.get(key, "").strip()
        if value:
            return value

    result = subprocess.run(
        ["git", "-C", str(repo), "branch", "--show-current"],
        check=True,
        capture_output=True,
        text=True,
    )
    branch = result.stdout.strip()
    if not branch:
        raise ConfigError("cannot determine current branch")
    return branch
