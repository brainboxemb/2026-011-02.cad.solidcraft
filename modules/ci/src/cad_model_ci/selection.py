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
            selected_models.update(
                model.id for model in models if model.process
            )

    for model in models:
        if not model.process:
            continue
        if any(_matches(path, model.watch) for path in paths):
            selected_models.add(model.id)

    return BuildSelection(
        branch=branch,
        modules=tuple(sorted(selected_modules)),
        models=tuple(sorted(selected_models)),
        tasks=("test", "build"),
    )


def expand_model_dependents(
    selection: BuildSelection,
    models: tuple[CadModel, ...],
) -> BuildSelection:
    """Close an explicit model selection over downstream dependents."""
    if selection.models is None:
        return selection

    selected = set(selection.models)
    changed = True
    while changed:
        changed = False
        for model in models:
            if model.id in selected or not model.process:
                continue
            if any(dependency in selected for dependency in model.dependencies):
                selected.add(model.id)
                changed = True

    ordered = tuple(model.id for model in models if model.id in selected)
    return BuildSelection(
        branch=selection.branch,
        modules=selection.modules,
        models=ordered,
        tasks=selection.tasks,
        forge_ref=selection.forge_ref,
        output_scope=selection.output_scope,
    )
