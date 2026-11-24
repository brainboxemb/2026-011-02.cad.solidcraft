"""Execute one resolved CAD build plan inside the SolidCraft runtime."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


_VERSION = re.compile(r"(?<!\d)(\d+\.\d+\.\d+)(?!\d)")


def _solidcraft_version() -> str:
    result = subprocess.run(
        ["solidcraft-cli", "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    match = _VERSION.search((result.stdout or "") + " " + (result.stderr or ""))
    if match is None:
        raise RuntimeError("cannot determine SolidCraft runtime version")
    return match.group(1)


def _camera_args(camera: dict | None) -> list[str]:
    if camera is None:
        return []
    return ["--camera", json.dumps(camera, separators=(",", ":"))]


def _snapshot(saved: Path, target: Path, camera: dict | None) -> None:
    command = [
        "solidcraft-cli",
        "snapshot",
        str(saved),
        "--out",
        str(target),
        "--no-grid",
        "--no-axes",
        *_camera_args(camera),
    ]
    subprocess.run(command, check=True)
    if not target.is_file() or target.stat().st_size == 0:
        raise RuntimeError(f"SolidCraft produced no snapshot: {target}")


def _build_one(output_root: Path, row: dict) -> None:
    from scpf.headless import run_document

    commands_path = output_root / row["commands"]
    document = json.loads(commands_path.read_text(encoding="utf-8"))
    native = row["native"]

    saved = output_root / native["sc"]
    step = output_root / native["step"]
    png = output_root / native["png"]
    saved.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"scpf-{row['id']}-") as tmp:
        run_document(
            document,
            save=saved,
            export=step,
            work_dir=Path(tmp),
        )

    _snapshot(
        saved,
        png,
        row.get("snapshot", {}).get("camera"),
    )

    stl_value = native.get("stl")
    if stl_value:
        stl = output_root / stl_value
        subprocess.run(
            [
                "solidcraft-cli",
                "run",
                "--in",
                str(saved),
                "--out",
                str(stl),
                "--quality",
                "fine",
            ],
            check=True,
        )
        if not stl.is_file() or stl.stat().st_size == 0:
            raise RuntimeError(f"SolidCraft produced no STL: {stl}")

    for extra in row.get("snapshots", []):
        _snapshot(
            saved,
            output_root / extra["path"],
            extra.get("camera"),
        )

    required = [saved, step, png]
    missing = [
        path for path in required
        if not path.is_file() or path.stat().st_size == 0
    ]
    if missing:
        raise RuntimeError(
            f"{row['id']}: missing native artifact(s): "
            + ", ".join(str(path) for path in missing)
        )


def run(plan_path: Path) -> None:
    expected = os.environ.get("EXPECTED_SOLIDCRAFT_VERSION", "").strip()
    actual = _solidcraft_version()
    if not expected:
        raise RuntimeError("EXPECTED_SOLIDCRAFT_VERSION is required")
    if actual != expected:
        raise RuntimeError(
            f"SolidCraft runtime version {actual} differs from expected {expected}"
        )

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("solidcraft", {}).get("version") != expected:
        raise RuntimeError("build plan SolidCraft version differs from runtime contract")

    output_root = plan_path.parent
    for row in plan.get("models", []):
        _build_one(output_root, row)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args(argv)
    run(args.plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
