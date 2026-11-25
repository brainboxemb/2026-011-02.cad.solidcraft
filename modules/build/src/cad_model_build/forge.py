"""Prepare one released Forge version and compile all planned models."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

from .config import ForgePin


def install_url(repository: str, version: str) -> str:
    return f"git+https://github.com/{repository}.git@{version}#subdirectory=cadlib"


def build_wheel(pin: ForgePin, wheel_dir: Path) -> Path:
    wheel_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--disable-pip-version-check",
            "--no-deps",
            "--wheel-dir",
            str(wheel_dir),
            install_url(pin.repository, pin.version),
        ],
        check=True,
    )
    wheels = tuple(wheel_dir.glob("scpf-*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"expected one Forge wheel, found {len(wheels)}")
    return wheels[0]


def _pythonpath(wheel: Path) -> str:
    previous = os.environ.get("PYTHONPATH", "")
    return str(wheel) + (os.pathsep + previous if previous else "")


def tested_solidcraft_version(wheel: Path) -> str:
    env = dict(os.environ)
    env["PYTHONPATH"] = _pythonpath(wheel)
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from scpf.version import TESTED_SOLIDCRAFT_VERSION; "
                "print(TESTED_SOLIDCRAFT_VERSION)"
            ),
        ],
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    value = result.stdout.strip()
    if not value:
        raise RuntimeError("Forge reported no tested SolidCraft version")
    return value


def _drawing_artifacts(document: dict, commands_path: str) -> list[dict]:
    artifacts = document.get("artifacts", {})
    if artifacts is None:
        return []
    if not isinstance(artifacts, dict):
        raise RuntimeError("Forge artifacts must be an object")
    drawings = artifacts.get("drawings", [])
    if not isinstance(drawings, list):
        raise RuntimeError("Forge drawing artifacts must be a list")

    base = Path(commands_path).parent
    projected = []
    seen: set[str] = set()
    for index, item in enumerate(drawings):
        if not isinstance(item, dict) or set(item) != {"name", "drawing", "pdf"}:
            raise RuntimeError(f"invalid Forge drawing artifact at index {index}")
        name = item["name"]
        variable = item["drawing"]
        relative = Path(item["pdf"])
        if (
            not isinstance(name, str)
            or not name.strip()
            or not isinstance(variable, str)
            or not variable.startswith("$")
            or relative.is_absolute()
            or ".." in relative.parts
            or relative.suffix.lower() != ".pdf"
            or not relative.parts
            or relative.parts[0] != "drawings"
        ):
            raise RuntimeError(f"invalid Forge drawing artifact at index {index}")
        path = (base / relative).as_posix()
        if path in seen:
            raise RuntimeError(f"duplicate Forge drawing artifact: {path}")
        seen.add(path)
        projected.append(
            {
                "name": name.strip(),
                "drawing": variable,
                "path": path,
            }
        )
    return projected


def compile_plan(*, repo: Path, output_root: Path, plan: dict, wheel: Path) -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = _pythonpath(wheel)

    for row in plan["models"]:
        source = repo / row["source"]
        target = output_root / row["commands"]
        target.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "scpf",
                str(source),
                "--out",
                str(target),
            ],
            cwd=repo,
            env=env,
            check=True,
        )
        if not target.is_file() or target.stat().st_size == 0:
            raise RuntimeError(f"Forge produced no output: {target}")
        document = json.loads(target.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            raise RuntimeError(f"Forge produced invalid command document: {target}")
        row["drawings"] = _drawing_artifacts(document, row["commands"])
