"""Load root toolchain pins and model-local build configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml


class BuildConfigError(ValueError):
    """Build configuration is missing or invalid."""


_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_VERSION = re.compile(r"^v\d+\.\d+\.\d+$")
_PNG = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*\.png$")
_SUPPORTED_ARTIFACTS = frozenset({"stl"})
_CAMERA_KEYS = frozenset({"target", "yaw", "pitch", "distance", "fov"})
_DEFAULT_MODEL_PRIORITY = 1000


@dataclass(frozen=True)
class ForgePin:
    repository: str
    version: str


@dataclass(frozen=True)
class SolidCraftPin:
    image: str
    version: str


@dataclass(frozen=True)
class SnapshotSpec:
    name: str
    camera: dict[str, object] | None = None


@dataclass(frozen=True)
class ModelVariant:
    id: str
    source: Path


@dataclass(frozen=True)
class ModelConfig:
    id: str
    root: Path
    variants: tuple[ModelVariant, ...]
    artifacts: tuple[str, ...]
    snapshots: tuple[SnapshotSpec, ...]
    snapshot_camera: dict[str, object] | None = None
    priority: int = _DEFAULT_MODEL_PRIORITY
    dependencies: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProjectConfig:
    stable_branch: str
    development_branch: str
    build_branch: str
    forge: ForgePin
    solidcraft: SolidCraftPin
    models_root: Path
    output_root: Path


def _mapping(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BuildConfigError(f"missing config: {path}") from exc
    except yaml.YAMLError as exc:
        raise BuildConfigError(f"invalid YAML: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BuildConfigError(f"config must be a mapping: {path}")
    return value


def _relative(value: object, field: str, path: Path) -> Path:
    if not isinstance(value, str) or not value:
        raise BuildConfigError(f"{field} must be a non-empty string: {path}")
    result = Path(value)
    if result.is_absolute() or ".." in result.parts:
        raise BuildConfigError(f"{field} must remain inside the repository: {path}")
    return result


def _camera(value: object, field: str, path: Path) -> dict[str, object] | None:
    if value is None:
        return None
    if not isinstance(value, dict) or set(value) - _CAMERA_KEYS:
        raise BuildConfigError(f"{field} has invalid camera fields: {path}")
    target = value.get("target")
    if target is not None:
        if (
            not isinstance(target, list)
            or len(target) != 3
            or any(type(item) not in (int, float) for item in target)
        ):
            raise BuildConfigError(f"{field}.target must contain three numbers: {path}")
    for key in ("yaw", "pitch", "distance", "fov"):
        item = value.get(key)
        if item is not None and type(item) not in (int, float):
            raise BuildConfigError(f"{field}.{key} must be numeric: {path}")
    return dict(value)


def _primary_snapshot_camera(
    data: dict[str, Any],
    path: Path,
) -> dict[str, object] | None:
    raw = data.get("snapshot")
    if raw is None:
        return None
    if not isinstance(raw, dict) or set(raw) != {"camera"}:
        raise BuildConfigError(
            f"snapshot must contain only camera: {path}"
        )
    return _camera(raw.get("camera"), "snapshot.camera", path)


def _snapshots(data: dict[str, Any], path: Path) -> tuple[SnapshotSpec, ...]:
    raw = data.get("snapshots", [])
    if raw is None:
        raw = []
    if not isinstance(raw, list):
        raise BuildConfigError(f"snapshots must be a list: {path}")

    result: list[SnapshotSpec] = []
    names: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict) or set(item) - {"name", "camera"}:
            raise BuildConfigError(f"snapshots[{index}] is invalid: {path}")
        name = item.get("name")
        if not isinstance(name, str) or not _PNG.fullmatch(name):
            raise BuildConfigError(f"invalid snapshot name {name!r}: {path}")
        if name == "model.png" or name in names:
            raise BuildConfigError(f"duplicate/reserved snapshot name {name!r}: {path}")
        names.add(name)
        result.append(
            SnapshotSpec(
                name=name,
                camera=_camera(
                    item.get("camera"),
                    f"snapshots[{index}].camera",
                    path,
                ),
            )
        )
    return tuple(result)


def _dependencies(
    data: dict[str, Any],
    *,
    owner_id: str,
    path: Path,
) -> tuple[str, ...]:
    raw = data.get("dependencies", [])
    if not isinstance(raw, list):
        raise BuildConfigError(f"dependencies must be a list: {path}")
    if not all(isinstance(item, str) and _ID.fullmatch(item) for item in raw):
        raise BuildConfigError(f"dependencies contains an invalid id: {path}")
    if len(set(raw)) != len(raw):
        raise BuildConfigError(f"dependencies must be unique: {path}")
    if owner_id in raw:
        raise BuildConfigError(f"model cannot depend on itself: {path}")
    return tuple(raw)


def _validate_dependencies(models: list[ModelConfig]) -> None:
    by_id = {model.id: model for model in models}
    for model in models:
        unknown = [item for item in model.dependencies if item not in by_id]
        if unknown:
            raise BuildConfigError(
                f"unknown model dependency {unknown[0]!r}: {model.root / 'ci.yml'}"
            )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(model_id: str, trail: tuple[str, ...]) -> None:
        if model_id in visited:
            return
        if model_id in visiting:
            cycle = " -> ".join((*trail, model_id))
            raise BuildConfigError(f"cyclic model dependency: {cycle}")
        visiting.add(model_id)
        model = by_id[model_id]
        for dependency in model.dependencies:
            visit(dependency, (*trail, model_id))
        visiting.remove(model_id)
        visited.add(model_id)

    for model in models:
        visit(model.id, ())


def _source_variant(
    *,
    owner_id: str,
    model_root: Path,
    data: dict[str, Any],
    path: Path,
) -> tuple[ModelVariant, ...]:
    source = _relative(data.get("source"), "source", path)
    if not (model_root / source).is_file():
        raise BuildConfigError(f"model source does not exist: {model_root / source}")
    return (ModelVariant(owner_id, source),)


def _variant_list(
    *,
    model_root: Path,
    data: dict[str, Any],
    path: Path,
) -> tuple[ModelVariant, ...]:
    raw = data.get("variants")
    if not isinstance(raw, list) or not raw:
        raise BuildConfigError(f"variants must be a non-empty list: {path}")

    result: list[ModelVariant] = []
    local_ids: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict) or set(item) != {"id", "source"}:
            raise BuildConfigError(
                f"variants[{index}] must contain only id and source: {path}"
            )
        variant_id = item.get("id")
        if not isinstance(variant_id, str) or not _ID.fullmatch(variant_id):
            raise BuildConfigError(f"invalid variant id: {path}")
        if variant_id in local_ids:
            raise BuildConfigError(f"duplicate variant id {variant_id!r}: {path}")
        local_ids.add(variant_id)

        source = _relative(item.get("source"), f"variants[{index}].source", path)
        if not (model_root / source).is_file():
            raise BuildConfigError(
                f"variant source does not exist: {model_root / source}"
            )
        result.append(ModelVariant(variant_id, source))

    return tuple(result)


def _variants(
    *,
    owner_id: str,
    model_root: Path,
    data: dict[str, Any],
    path: Path,
) -> tuple[ModelVariant, ...]:
    has_source = "source" in data
    has_variants = "variants" in data
    if has_source == has_variants:
        raise BuildConfigError(
            f"exactly one of source or variants is required: {path}"
        )
    if has_source:
        return _source_variant(
            owner_id=owner_id,
            model_root=model_root,
            data=data,
            path=path,
        )
    return _variant_list(model_root=model_root, data=data, path=path)


def load_project(repo: Path) -> ProjectConfig:
    path = repo / "ci.yml"
    data = _mapping(path)
    if data.get("schema") != 1:
        raise BuildConfigError(f"unsupported schema: {path}")

    branches = data.get("branches")
    dependencies = data.get("dependencies")
    generated = data.get("generated")
    roots = data.get("roots")
    if not all(
        isinstance(value, dict)
        for value in (branches, generated, dependencies, roots)
    ):
        raise BuildConfigError(
            f"branches, generated, dependencies and roots must be mappings: {path}"
        )

    stable = branches.get("stable")
    development = branches.get("development")
    if not isinstance(stable, str) or not isinstance(development, str):
        raise BuildConfigError(f"branch names must be strings: {path}")
    build_branch = generated.get("build_branch")
    if not isinstance(build_branch, str) or not _ID.fullmatch(build_branch):
        raise BuildConfigError(f"generated.build_branch is invalid: {path}")

    forge = dependencies.get("forge")
    solidcraft = dependencies.get("solidcraft")
    if not isinstance(forge, dict) or not isinstance(solidcraft, dict):
        raise BuildConfigError(
            f"dependencies.forge and dependencies.solidcraft are required: {path}"
        )

    repository = forge.get("repository")
    version = forge.get("version")
    if not isinstance(repository, str) or not _REPOSITORY.fullmatch(repository):
        raise BuildConfigError(f"invalid Forge repository: {path}")
    if not isinstance(version, str) or not _VERSION.fullmatch(version):
        raise BuildConfigError(f"Forge version must be a v-prefixed release tag: {path}")

    image = solidcraft.get("image")
    solidcraft_version = solidcraft.get("version")
    # Qualification-only allowance on #64. Permanent branches still pin an
    # immutable v-prefixed image; this branch may exercise the exact runtime
    # owner :edge candidate before v0.3.6 exists.
    candidate_edge = image == "ghcr.io/brainboxemb/cad-solidcraft:edge"
    if (
        not isinstance(image, str)
        or (
            not image.startswith("ghcr.io/brainboxemb/cad-solidcraft:v")
            and not candidate_edge
        )
    ):
        raise BuildConfigError(
            f"released SolidCraft runtime image or qualification edge required: {path}"
        )
    if not isinstance(solidcraft_version, str) or not solidcraft_version:
        raise BuildConfigError(f"invalid SolidCraft version: {path}")

    return ProjectConfig(
        stable_branch=stable,
        development_branch=development,
        build_branch=build_branch,
        forge=ForgePin(repository, version),
        solidcraft=SolidCraftPin(image, solidcraft_version),
        models_root=_relative(roots.get("models"), "roots.models", path),
        output_root=_relative(roots.get("output"), "roots.output", path),
    )


def _group_priorities(root: Path) -> dict[Path, int]:
    groups: dict[Path, int] = {}
    for path in sorted(root.rglob("ci.yml")):
        data = _mapping(path)
        if data.get("kind") != "group":
            continue
        if set(data) != {"schema", "kind", "priority"}:
            raise BuildConfigError(
                f"group config may contain only schema, kind and priority: {path}"
            )
        if data.get("schema") != 1:
            raise BuildConfigError(f"unsupported group schema: {path}")
        priority = data.get("priority")
        if type(priority) is not int or priority < 0:
            raise BuildConfigError(f"group priority must be a non-negative integer: {path}")
        groups[path.parent] = priority
    return groups


def _resolved_priority(
    *,
    model_root: Path,
    models_root: Path,
    groups: dict[Path, int],
) -> int:
    current = model_root.parent
    while True:
        if current in groups:
            return groups[current]
        if current == models_root:
            break
        if models_root not in current.parents:
            break
        current = current.parent
    return groups.get(models_root, _DEFAULT_MODEL_PRIORITY)


def discover_models(repo: Path, project: ProjectConfig) -> tuple[ModelConfig, ...]:
    root = repo / project.models_root
    groups = _group_priorities(root)
    result: list[ModelConfig] = []
    owner_ids: set[str] = set()
    variant_ids: set[str] = set()

    for path in sorted(root.rglob("ci.yml")):
        data = _mapping(path)
        if data.get("kind") == "group":
            continue
        if data.get("schema") != 1:
            raise BuildConfigError(f"unsupported model schema: {path}")
        process = data.get("process", True)
        if type(process) is not bool:
            raise BuildConfigError(f"process must be boolean: {path}")
        if not process:
            continue

        owner_id = data.get("id")
        if not isinstance(owner_id, str) or not _ID.fullmatch(owner_id):
            raise BuildConfigError(f"invalid model id: {path}")
        if owner_id in owner_ids:
            raise BuildConfigError(f"duplicate model owner id {owner_id!r}: {path}")
        owner_ids.add(owner_id)

        if data.get("builder") != "forge":
            raise BuildConfigError(f"model builder must be forge: {path}")
        model_root = path.parent
        variants = _variants(
            owner_id=owner_id,
            model_root=model_root,
            data=data,
            path=path,
        )
        for variant in variants:
            if variant.id in variant_ids:
                raise BuildConfigError(
                    f"duplicate build variant id {variant.id!r}: {path}"
                )
            variant_ids.add(variant.id)

        artifacts = data.get("artifacts", [])
        if artifacts is None:
            artifacts = []
        if (
            not isinstance(artifacts, list)
            or any(not isinstance(item, str) or not item for item in artifacts)
            or len(set(artifacts)) != len(artifacts)
        ):
            raise BuildConfigError(f"artifacts must be a unique string list: {path}")
        unsupported = sorted(set(artifacts) - _SUPPORTED_ARTIFACTS)
        if unsupported:
            raise BuildConfigError(
                f"unsupported artifact(s) {', '.join(unsupported)}: {path}"
            )

        result.append(
            ModelConfig(
                id=owner_id,
                root=model_root,
                variants=variants,
                artifacts=tuple(artifacts),
                snapshots=_snapshots(data, path),
                snapshot_camera=_primary_snapshot_camera(data, path),
                priority=_resolved_priority(
                    model_root=model_root,
                    models_root=root,
                    groups=groups,
                ),
                dependencies=_dependencies(
                    data,
                    owner_id=owner_id,
                    path=path,
                ),
            )
        )

    _validate_dependencies(result)
    return tuple(sorted(result, key=lambda model: (model.priority, model.id)))


def active_variant_ids(models: tuple[ModelConfig, ...]) -> set[str]:
    return {
        variant.id
        for model in models
        for variant in model.variants
    }
