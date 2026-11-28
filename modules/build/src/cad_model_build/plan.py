"""Resolve selected model ids into one deterministic build plan."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess

from .config import BuildConfigError, ModelConfig, ProjectConfig


def source_sha(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _selected_in_build_order(
    models: tuple[ModelConfig, ...],
    selected_ids: tuple[str, ...],
) -> tuple[ModelConfig, ...]:
    by_id = {model.id: model for model in models}
    missing = [model_id for model_id in selected_ids if model_id not in by_id]
    if missing:
        raise BuildConfigError(f"unknown selected model(s): {', '.join(missing)}")

    selected = {model_id for model_id in selected_ids}
    remaining = {model_id: by_id[model_id] for model_id in selected}
    ordered: list[ModelConfig] = []

    while remaining:
        ready = [
            model
            for model in remaining.values()
            if not any(
                dependency in remaining
                for dependency in model.dependencies
                if dependency in selected
            )
        ]
        if not ready:
            raise BuildConfigError("selected model dependency graph contains a cycle")
        model = min(ready, key=lambda item: (item.priority, item.id))
        ordered.append(model)
        del remaining[model.id]

    return tuple(ordered)


def resolve_plan(
    *,
    repo: Path,
    project: ProjectConfig,
    models: tuple[ModelConfig, ...],
    selected_ids: tuple[str, ...],
    namespace: str,
    source_ref: str | None = None,
    forge_ref: str | None = None,
) -> dict:
    allowed = {
        project.stable_branch,
        project.development_branch,
        project.experimental_branch,
        "test",
    }
    if namespace not in allowed:
        raise BuildConfigError(
            f"output namespace must be one of {', '.join(sorted(allowed))}"
        )
    if len(set(selected_ids)) != len(selected_ids):
        raise BuildConfigError("selected model ids must be unique")

    built_source_sha = source_sha(repo)
    rows = []
    selected = _selected_in_build_order(models, selected_ids)
    for model in selected:
        relative_root = model.root.relative_to(repo).as_posix()
        for variant in sorted(model.variants, key=lambda item: item.id):
            target = f"models/{variant.id}"
            rows.append(
                {
                    "id": variant.id,
                    "owner": model.id,
                    "priority": model.priority,
                    "dependencies": list(model.dependencies),
                    "built_source_sha": built_source_sha,
                    "root": relative_root,
                    "source": (model.root / variant.source).relative_to(repo).as_posix(),
                    "commands": f"{target}/solidcraft.json",
                    "snapshot": {
                        "camera": model.snapshot_camera,
                    },
                    "native": {
                        "sc": f"{target}/model.sc",
                        "step": f"{target}/model.step",
                        "png": f"{target}/model.png",
                        "stl": f"{target}/model.stl"
                        if "stl" in model.artifacts
                        else None,
                    },
                    "drawings": [],
                    "snapshots": [
                        {
                            "name": item.name,
                            "path": f"{target}/{item.name}",
                            "camera": item.camera,
                            **(
                                {"exploded_view": item.exploded_view}
                                if item.exploded_view is not None
                                else {}
                            ),
                        }
                        for item in model.snapshots
                    ],
                    "artifacts": list(model.artifacts),
                    "artifact_options": (
                        {
                            "stl": {
                                "quality": model.stl_quality,
                            },
                        }
                        if model.stl_quality is not None
                        else {}
                    ),
                }
            )

    return {
        "schema": 1,
        "namespace": namespace,
        "source_ref": source_ref or namespace,
        "source_sha": built_source_sha,
        "forge": {
            "repository": project.forge.repository,
            "version": project.forge.version,
            **(
                {"qualification_ref": forge_ref}
                if forge_ref is not None
                else {}
            ),
        },
        "solidcraft": {
            "image": project.solidcraft.image,
            "version": project.solidcraft.version,
        },
        "models": rows,
    }


def write_plan(output_root: Path, plan: dict) -> Path:
    output_root.mkdir(parents=True, exist_ok=True)
    path = output_root / "build-plan.json"
    path.write_text(
        json.dumps(plan, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path
