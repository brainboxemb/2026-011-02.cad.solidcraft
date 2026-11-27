"""Repository scan -> plan -> Forge compile -> SolidCraft batch."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import tempfile

from .config import candidate_solidcraft_pin, discover_models, load_project
from .forge import build_wheel, compile_plan, tested_solidcraft_version
from .native import run_native_batch
from .plan import resolve_plan, write_plan


def execute(
    *,
    repo: Path,
    namespace: str,
    selected_ids: tuple[str, ...],
    solidcraft_image: str | None = None,
    solidcraft_version: str | None = None,
) -> Path:
    repo = repo.resolve()
    project = load_project(repo)
    candidate = candidate_solidcraft_pin(
        solidcraft_image,
        solidcraft_version,
    )
    plan_project = (
        replace(project, solidcraft=candidate)
        if candidate is not None
        else project
    )
    models = discover_models(repo, project)
    plan = resolve_plan(
        repo=repo,
        project=plan_project,
        models=models,
        selected_ids=selected_ids,
        namespace=namespace,
    )

    output_root = repo / project.output_root / namespace
    plan_path = write_plan(output_root, plan)
    if not plan["models"]:
        return plan_path

    with tempfile.TemporaryDirectory(prefix="cad-model-forge-") as tmp:
        wheel = build_wheel(project.forge, Path(tmp))
        qualified = tested_solidcraft_version(wheel)
        if qualified != project.solidcraft.version:
            raise RuntimeError(
                f"Forge {project.forge.version} qualifies SolidCraft {qualified}, "
                f"but ci.yml pins {project.solidcraft.version}"
            )

        compile_plan(
            repo=repo,
            output_root=output_root,
            plan=plan,
            wheel=wheel,
        )
        # Forge compilation may discover generated artifacts such as native
        # drawing PDFs. Persist the enriched plan before native replay.
        write_plan(output_root, plan)
        run_native_batch(
            repo=repo,
            output_root=output_root,
            plan_path=plan_path,
            forge_wheel=wheel,
            image=plan_project.solidcraft.image,
            solidcraft_version=plan_project.solidcraft.version,
        )

    return plan_path
