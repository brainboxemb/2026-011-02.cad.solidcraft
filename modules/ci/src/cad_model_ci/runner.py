"""Execute selected internal module tests and the CAD model batch."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

from .config import BuildSelection, ProjectConfig
from .items import CadModel, PythonModule


def _run(command: list[str], *, env: dict[str, str] | None = None) -> None:
    subprocess.run(command, check=True, env=env)


def _source_env(module_root: Path) -> dict[str, str]:
    env = dict(os.environ)
    source = str((module_root / "src").resolve())
    previous = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = source + (os.pathsep + previous if previous else "")
    return env


def test_module(module: PythonModule) -> None:
    _run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(module.root / "tests"),
            "-v",
        ],
        env=_source_env(module.root),
    )


def build_models(
    *,
    repo: Path,
    build_module_root: Path,
    namespace: str,
    models: tuple[CadModel, ...],
    forge_ref: str | None = None,
) -> None:
    if not models:
        return

    command = [
        sys.executable,
        "-m",
        "cad_model_build",
        "--repo",
        str(repo),
        "--namespace",
        namespace,
    ]
    if forge_ref is not None:
        command.extend(["--forge-ref", forge_ref])

    for model in models:
        command.extend(["--model", model.id])

    _run(command, env=_source_env(build_module_root))


def execute(
    *,
    repo: Path,
    project: ProjectConfig,
    selection: BuildSelection,
    namespace: str,
    modules: tuple[PythonModule, ...],
    models: tuple[CadModel, ...],
) -> None:
    if "test" in selection.tasks:
        for module in modules:
            test_module(module)

    if "build" in selection.tasks:
        build_models(
            repo=repo,
            build_module_root=repo / project.modules_root / "build",
            namespace=namespace,
            models=models,
            forge_ref=selection.forge_ref,
        )
