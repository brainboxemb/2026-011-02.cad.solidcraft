"""Translate Git changes into module/model execution selections."""

from __future__ import annotations

from fnmatch import fnmatchcase

from .config import BuildSelection, full_selection
from .items import CadModel, PythonModule


def _matches(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatchcase(path, pattern) for pattern in patterns)


def changed_selection(
    *,
    branch: str,
    paths: tuple[str, ...],
    modules: tuple[PythonModule, ...],
    models: tuple[CadModel, ...],
) -> BuildSelection:
    if "ci.yml" in paths:
        return full_selection(branch)

    selected_modules: set[str] = set()
    selected_models: set[str] = set()

    for module in modules:
        if not any(_matches(path, module.watch) for path in paths):
            continue
        if module.impact == "full":
            return full_selection(branch)
        selected_modules.add(module.id)
        if module.impact == "models":
            selected_models.update(model.id for model in models)

    for model in models:
        if any(_matches(path, model.watch) for path in paths):
            selected_models.add(model.id)

    return BuildSelection(
        branch=branch,
        modules=tuple(sorted(selected_modules)),
        models=tuple(sorted(selected_models)),
        tasks=("test", "build"),
    )
