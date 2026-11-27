"""Discover independently owned Python modules and CAD model owners."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import yaml

from .config import ConfigError, ProjectConfig


_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
_IMPACTS = {"self", "models", "full"}
_DEFAULT_MODEL_PRIORITY = 1000


@dataclass(frozen=True)
class PythonModule:
    id: str
    root: Path
    impact: str = "self"
    watch: tuple[str, ...] = ()


@dataclass(frozen=True)
class CadModel:
    id: str
    root: Path
    builder: str
    source: Path | None = None
    watch: tuple[str, ...] = ()
    priority: int = _DEFAULT_MODEL_PRIORITY
    dependencies: tuple[str, ...] = ()
    process: bool = True


def _load(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema") != 1:
        raise ConfigError(f"invalid item config: {path}")
    return value


def _id(data: dict[str, Any], path: Path) -> str:
    value = data.get("id")
    if not isinstance(value, str) or not _ID.fullmatch(value):
        raise ConfigError(f"invalid item id: {path}")
    return value


def _impact(data: dict[str, Any], path: Path) -> str:
    value = data.get("impact", "self")
    if value not in _IMPACTS:
        raise ConfigError(f"impact must be one of {sorted(_IMPACTS)}: {path}")
    return value


def _watch(
    data: dict[str, Any],
    *,
    default: str,
    path: Path,
) -> tuple[str, ...]:
    extra = data.get("watch", [])
    if not isinstance(extra, list) or not all(
        isinstance(value, str) and value for value in extra
    ):
        raise ConfigError(f"watch must be a string list: {path}")
    return (default, *extra)


def _dependencies(
    data: dict[str, Any],
    *,
    model_id: str,
    path: Path,
) -> tuple[str, ...]:
    raw = data.get("dependencies", [])
    if not isinstance(raw, list):
        raise ConfigError(f"dependencies must be a list: {path}")
    if not all(isinstance(item, str) and _ID.fullmatch(item) for item in raw):
        raise ConfigError(f"dependencies contains an invalid id: {path}")
    if len(set(raw)) != len(raw):
        raise ConfigError(f"dependencies must be unique: {path}")
    if model_id in raw:
        raise ConfigError(f"model cannot depend on itself: {path}")
    return tuple(raw)


def _validate_dependencies(models: list[CadModel]) -> None:
    by_id = {model.id: model for model in models}
    for model in models:
        unknown = [item for item in model.dependencies if item not in by_id]
        if unknown:
            raise ConfigError(
                f"unknown model dependency {unknown[0]!r}: {model.root / 'ci.yml'}"
            )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(model_id: str, trail: tuple[str, ...]) -> None:
        if model_id in visited:
            return
        if model_id in visiting:
            cycle = " -> ".join((*trail, model_id))
            raise ConfigError(f"cyclic model dependency: {cycle}")
        visiting.add(model_id)
        model = by_id[model_id]
        for dependency in model.dependencies:
            visit(dependency, (*trail, model_id))
        visiting.remove(model_id)
        visited.add(model_id)

    for model in models:
        visit(model.id, ())


def _source_path(value: object, *, field: str, path: Path) -> Path:
    if not isinstance(value, str) or not value:
        raise ConfigError(f"{field} must be a string: {path}")
    result = Path(value)
    if result.is_absolute() or ".." in result.parts:
        raise ConfigError(f"{field} must remain inside model root: {path}")
    return result


def _validate_model_sources(child: Path, data: dict[str, Any], path: Path) -> Path | None:
    has_source = "source" in data
    has_variants = "variants" in data
    if has_source == has_variants:
        raise ConfigError(f"exactly one of source or variants is required: {path}")

    if has_source:
        source = _source_path(data.get("source"), field="model source", path=path)
        if not (child / source).is_file():
            raise ConfigError(f"model source does not exist: {child / source}")
        return source

    variants = data.get("variants")
    if not isinstance(variants, list) or not variants:
        raise ConfigError(f"variants must be a non-empty list: {path}")
    for index, item in enumerate(variants):
        if not isinstance(item, dict) or set(item) != {"id", "source"}:
            raise ConfigError(
                f"variants[{index}] must contain only id and source: {path}"
            )
        variant_id = item.get("id")
        if not isinstance(variant_id, str) or not _ID.fullmatch(variant_id):
            raise ConfigError(f"invalid variant id: {path}")
        source = _source_path(
            item.get("source"),
            field=f"variants[{index}].source",
            path=path,
        )
        if not (child / source).is_file():
            raise ConfigError(f"variant source does not exist: {child / source}")
    return None


def discover_modules(repo: Path, project: ProjectConfig) -> tuple[PythonModule, ...]:
    root = repo / project.modules_root
    result: list[PythonModule] = []
    for child in sorted(root.iterdir(), key=lambda value: value.name):
        path = child / "ci.yml"
        if not child.is_dir() or not path.is_file():
            continue
        data = _load(path)
        if data.get("kind") != "python":
            raise ConfigError(f"module kind must be python: {path}")
        relative = child.relative_to(repo).as_posix()
        result.append(
            PythonModule(
                id=_id(data, path),
                root=child,
                impact=_impact(data, path),
                watch=_watch(data, default=f"{relative}/**", path=path),
            )
        )
    return tuple(result)


def _group_priorities(root: Path) -> dict[Path, int]:
    groups: dict[Path, int] = {}
    for path in sorted(root.rglob("ci.yml")):
        data = _load(path)
        if data.get("kind") != "group":
            continue
        if set(data) != {"schema", "kind", "priority"}:
            raise ConfigError(
                f"group config may contain only schema, kind and priority: {path}"
            )
        priority = data.get("priority")
        if type(priority) is not int or priority < 0:
            raise ConfigError(f"group priority must be a non-negative integer: {path}")
        groups[path.parent] = priority
    return groups


def _resolved_group(
    *,
    model_root: Path,
    models_root: Path,
    groups: dict[Path, int],
) -> tuple[int, Path | None]:
    current = model_root.parent
    while True:
        if current in groups:
            return groups[current], current / "ci.yml"
        if current == models_root:
            break
        if models_root not in current.parents:
            break
        current = current.parent
    if models_root in groups:
        return groups[models_root], models_root / "ci.yml"
    return _DEFAULT_MODEL_PRIORITY, None


def discover_models(repo: Path, project: ProjectConfig) -> tuple[CadModel, ...]:
    root = repo / project.models_root
    groups = _group_priorities(root)
    result: list[CadModel] = []
    seen: set[str] = set()

    for path in sorted(root.rglob("ci.yml")):
        child = path.parent
        data = _load(path)
        if data.get("kind") == "group":
            continue
        process = data.get("process", True)
        if type(process) is not bool:
            raise ConfigError(f"model process must be boolean: {path}")
        model_id = _id(data, path)
        if model_id in seen:
            raise ConfigError(f"duplicate model id {model_id!r}: {path}")
        seen.add(model_id)

        builder = data.get("builder")
        if builder != "forge":
            raise ConfigError(f"unsupported model builder {builder!r}: {path}")
        source = _validate_model_sources(child, data, path)

        relative = child.relative_to(repo).as_posix()
        priority, group_config = _resolved_group(
            model_root=child,
            models_root=root,
            groups=groups,
        )
        watch = list(_watch(data, default=f"{relative}/**", path=path))
        if group_config is not None:
            watch.append(group_config.relative_to(repo).as_posix())

        result.append(
            CadModel(
                id=model_id,
                root=child,
                builder=builder,
                source=source,
                watch=tuple(watch),
                priority=priority,
                dependencies=_dependencies(
                    data,
                    model_id=model_id,
                    path=path,
                ),
                process=process,
            )
        )

    _validate_dependencies(result)
    return tuple(sorted(result, key=lambda model: (model.priority, model.id)))


def select(items, selected_ids: tuple[str, ...] | None):
    if selected_ids is None:
        return tuple(
            item for item in items
            if getattr(item, "process", True)
        )
    by_id = {item.id: item for item in items}
    missing = [item_id for item_id in selected_ids if item_id not in by_id]
    if missing:
        raise ConfigError(f"unknown item(s): {', '.join(missing)}")
    return tuple(by_id[item_id] for item_id in selected_ids)
