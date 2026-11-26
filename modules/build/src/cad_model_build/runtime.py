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


def _drawing_inspections(replay_results) -> dict[str, dict]:
    """Return the final native drawing inspection for each named drawing."""
    by_name: dict[str, dict] = {}
    if not isinstance(replay_results, list):
        return by_name
    for result in replay_results:
        if (
            isinstance(result, dict)
            and isinstance(result.get("name"), str)
            and isinstance(result.get("sheets"), list)
            and isinstance(result.get("properties"), dict)
        ):
            by_name[result["name"]] = result
    return by_name

def _export_drawings(
    *,
    document: dict,
    row: dict,
    variables: dict,
    saved: Path,
    output_root: Path,
    work_dir: Path,
    replay_results,
) -> tuple[Path, ...]:
    declarations = row.get("drawings", [])
    if not isinstance(declarations, list):
        raise RuntimeError(f"{row['id']}: drawings must be a list")

    source = document.get("artifacts", {}).get("drawings", [])
    if not isinstance(source, list):
        raise RuntimeError(f"{row['id']}: Forge drawing artifacts must be a list")
    by_variable = {
        item.get("drawing"): item
        for item in source
        if isinstance(item, dict)
    }
    inspections = _drawing_inspections(replay_results)

    produced: list[Path] = []
    seen: set[Path] = set()
    root = output_root.resolve()
    for index, item in enumerate(declarations, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(f"{row['id']}: invalid drawing declaration")
        required = {"name", "drawing", "path"}
        allowed = required | {"sheet", "orientation", "preview", "inspect"}
        if not required.issubset(item) or not set(item).issubset(allowed):
            raise RuntimeError(f"{row['id']}: invalid drawing declaration")

        variable = item["drawing"]
        declared = by_variable.get(variable)
        if not isinstance(declared, dict):
            raise RuntimeError(
                f"{row['id']}: drawing {variable!r} is not declared by Forge"
            )
        if variable not in variables:
            raise RuntimeError(
                f"{row['id']}: drawing variable {variable!r} was not replay-bound"
            )

        target = (output_root / item["path"]).resolve()
        targets = [target]
        preview = None
        inspect = None
        sheet_variable = item.get("sheet")
        if "preview" in item or "inspect" in item or sheet_variable is not None:
            if (
                not isinstance(item.get("preview"), str)
                or not isinstance(item.get("inspect"), str)
                or not isinstance(sheet_variable, str)
                or sheet_variable not in variables
            ):
                raise RuntimeError(
                    f"{row['id']}: incomplete drawing preview declaration"
                )
            preview = (output_root / item["preview"]).resolve()
            inspect = (output_root / item["inspect"]).resolve()
            targets.extend((preview, inspect))

        for artifact in targets:
            if root not in artifact.parents:
                raise RuntimeError(f"{row['id']}: drawing path escapes build scope")
            if artifact in seen:
                raise RuntimeError(
                    f"{row['id']}: duplicate drawing path {artifact}"
                )
            seen.add(artifact)
            artifact.parent.mkdir(parents=True, exist_ok=True)

        orientation_variable = item.get("orientation")
        if orientation_variable is not None:
            if (
                not isinstance(orientation_variable, str)
                or orientation_variable not in variables
                or variables[orientation_variable] != "landscape"
            ):
                raise RuntimeError(
                    f"{row['id']}: drawing sheet is not landscape"
                )

        commands = [
            {
                "command": "drawing.open",
                "params": {"drawing": variables[variable]},
            },
            {
                "command": "drawing.export",
                "params": {
                    "format": "pdf",
                    "path": str(target),
                },
            },
        ]
        if preview is not None:
            commands.append(
                {
                    "command": "drawing.export",
                    "params": {
                        "sheet": variables[sheet_variable],
                        "format": "png",
                        "path": str(preview),
                        "dpi": 144,
                    },
                }
            )
        commands.append({"command": "drawing.close", "params": {}})

        script = work_dir / f"drawing-export-{index}.json"
        checkpoint = work_dir / f"drawing-export-{index}.sc"
        script.write_text(
            json.dumps({"commands": commands}, indent=2) + "\n",
            encoding="utf-8",
        )
        subprocess.run(
            [
                "solidcraft-cli",
                "run",
                str(script),
                "--in",
                str(saved),
                "--save",
                str(checkpoint),
                "--quiet",
            ],
            check=True,
        )

        if not target.is_file() or target.stat().st_size == 0:
            raise RuntimeError(f"{row['id']}: SolidCraft produced no drawing PDF")
        if target.read_bytes()[:5] != b"%PDF-":
            raise RuntimeError(f"{row['id']}: drawing artifact is not a PDF")
        produced.append(target)

        if preview is not None and inspect is not None:
            if not preview.is_file() or preview.stat().st_size == 0:
                raise RuntimeError(
                    f"{row['id']}: SolidCraft produced no drawing preview PNG"
                )
            if preview.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                raise RuntimeError(
                    f"{row['id']}: drawing preview artifact is not a PNG"
                )
            inspection = inspections.get(item["name"])
            if inspection is None:
                raise RuntimeError(
                    f"{row['id']}: replay produced no drawing inspection"
                )
            inspect.write_text(
                json.dumps(inspection, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            produced.extend((preview, inspect))

    return tuple(produced)

def _export_stl(
    *,
    saved: Path,
    target: Path,
    artifact_options: dict,
) -> None:
    """SolidCraft adapter for generic STL artifact intent."""
    options = artifact_options.get("stl", {})
    if not isinstance(options, dict) or set(options) - {"quality"}:
        raise RuntimeError("invalid STL artifact options")

    command = [
        "solidcraft-cli",
        "run",
        "--in",
        str(saved),
        "--out",
        str(target),
    ]

    # No generic quality means adapter-owned default behavior.  For the current
    # SolidCraft adapter that is deliberately expressed by omitting --quality,
    # leaving the pinned runtime to use its native default.
    quality = options.get("quality")
    if quality is not None:
        if not isinstance(quality, str) or not quality:
            raise RuntimeError("invalid STL quality")
        command.extend(["--quality", quality])

    subprocess.run(command, check=True)
    if not target.is_file() or target.stat().st_size == 0:
        raise RuntimeError(f"SolidCraft produced no STL: {target}")


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
        work_dir = Path(tmp)
        results = work_dir / "replay-results.json"
        replay = run_document(
            document,
            save=saved,
            export=step,
            results_out=results,
            work_dir=work_dir,
        )
        replay_results = json.loads(results.read_text(encoding="utf-8"))
        drawings = _export_drawings(
            document=document,
            row=row,
            variables=replay.get("variables", {}),
            saved=saved,
            output_root=output_root,
            work_dir=work_dir,
            replay_results=replay_results,
        )

    _snapshot(
        saved,
        png,
        row.get("snapshot", {}).get("camera"),
    )

    stl_value = native.get("stl")
    if stl_value:
        _export_stl(
            saved=saved,
            target=output_root / stl_value,
            artifact_options=row.get("artifact_options", {}),
        )

    for extra in row.get("snapshots", []):
        _snapshot(
            saved,
            output_root / extra["path"],
            extra.get("camera"),
        )

    required = [saved, step, png, *drawings]
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
