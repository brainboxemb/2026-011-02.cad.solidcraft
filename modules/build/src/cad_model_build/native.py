"""Launch the released SolidCraft runtime once for a complete batch."""

from __future__ import annotations

from pathlib import Path
import subprocess


def run_native_batch(
    *,
    repo: Path,
    output_root: Path,
    plan_path: Path,
    forge_wheel: Path,
    image: str,
    solidcraft_version: str,
) -> None:
    subprocess.run(["docker", "pull", image], cwd=repo, check=True)

    container_plan = "/output/" + plan_path.relative_to(output_root).as_posix()
    pythonpath = (
        f"/forge/{forge_wheel.name}:"
        "/workspace/modules/build/src"
    )
    command = [
        "docker",
        "run",
        "--rm",
        "--pull=never",
        "-e",
        f"PYTHONPATH={pythonpath}",
        "-e",
        f"EXPECTED_SOLIDCRAFT_VERSION={solidcraft_version}",
        "-e",
        "SOLIDCRAFT_GPU=cpu",
        "-v",
        f"{repo.resolve()}:/workspace:ro",
        "-v",
        f"{output_root.resolve()}:/output",
        "-v",
        f"{forge_wheel.parent.resolve()}:/forge:ro",
        "-w",
        "/workspace",
        image,
        "python",
        "-m",
        "cad_model_build.runtime",
        "--plan",
        container_plan,
    ]
    subprocess.run(command, cwd=repo, check=True)
