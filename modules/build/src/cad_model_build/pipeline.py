"""Repository scan -> plan -> Forge compile -> SolidCraft batch."""

from __future__ import annotations

from pathlib import Path
import re
import tempfile

from .config import BuildConfigError, discover_models, load_project
from .forge import build_wheel, compile_plan, tested_solidcraft_version
from .native import run_native_batch
from .plan import resolve_plan, write_plan


_COMMIT_SHA = re.compile(r"^[0-9a-f]{40}$")


def execute(
    *,
    repo: Path,
    namespace: str,
    selected_ids: tuple[str, ...],
    forge_ref: str | None = None,
) -> Path:
    repo = repo.resolve()
    if (
        forge_ref is not None
        and not _COMMIT_SHA.fullmatch(forge_ref)
    ):
        raise BuildConfigError(
            "Forge qualification ref must be an exact 40-character "
            "lowercase commit SHA"
        )
    project = load_project(repo)
    models = discover_models(repo, project)
    plan = resolve_plan(
        repo=repo,
        project=project,
        models=models,
        selected_ids=selected_ids,
        namespace=namespace,
        forge_ref=forge_ref,
    )

    output_root = repo / project.output_root / namespace
    plan_path = write_plan(output_root, plan)
    if not plan["models"]:
        return plan_path

    with tempfile.TemporaryDirectory(prefix="cad-model-forge-") as tmp:
        wheel = build_wheel(
            project.forge,
            Path(tmp),
            qualification_ref=forge_ref,
        )
        qualified = tested_solidcraft_version(wheel)
        if qualified != project.solidcraft.version:
            raise RuntimeError(
                f"Forge {forge_ref or project.forge.version} qualifies "
                f"SolidCraft {qualified}, "
                f"but ci.yml pins {project.solidcraft.version}"
            )

        compile_plan(
            repo=repo,
            output_root=output_root,
            plan=plan,
            wheel=wheel,
        )
        # Forge compilation can discover generated artifacts (for example
        # native drawing PDFs). Persist the enriched plan before the runtime
        # consumes and Pages later publishes it.
        write_plan(output_root, plan)
        run_native_batch(
            repo=repo,
            output_root=output_root,
            plan_path=plan_path,
            forge_wheel=wheel,
            image=project.solidcraft.image,
            solidcraft_version=project.solidcraft.version,
        )

    return plan_path
