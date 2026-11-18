#!/usr/bin/env python3
"""Run selected native SolidCraft CAD verification from one build-plan JSON."""

from __future__ import annotations

import argparse
from importlib.metadata import version
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from model_catalog import MODELS, source_path
from model_checks import command_check, extra_snapshots, native_check, snapshot_camera
from output_store import prepare_candidate
from scpf.version import TESTED_SOLIDCRAFT_VERSION


ROOT = Path(__file__).resolve().parents[2]


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=ROOT, check=check)


def load_plan(path: Path) -> dict:
    plan = json.loads(path.read_text(encoding="utf-8"))
    if plan.get("schema") != 1:
        raise ValueError("unsupported CAD build-plan schema")
    return plan


def camera_json(value: dict | None) -> str | None:
    if not value:
        return None
    return json.dumps(value, separators=(",", ":"))


def compile_native(slug: str, native_root: Path) -> Path:
    model_root = native_root / slug
    model_root.mkdir(parents=True, exist_ok=True)
    commands = model_root / "commands.json"
    run([
        sys.executable,
        "-m",
        "scpf",
        str(source_path(ROOT, slug)),
        "--out",
        str(commands),
    ])
    command_check(slug, commands)

    run([
        sys.executable,
        "-m",
        "scpf.headless",
        str(commands),
        "--save",
        str(model_root / "model.sc"),
        "--out",
        str(model_root / "model.step"),
        "--results",
        str(model_root / "results.json"),
        "--replay-log",
        str(model_root / "replay-log.json"),
    ])
    run([
        "solidcraft-cli",
        "eval",
        str(model_root / "model.sc"),
        "--json-out",
        str(model_root / "measurements.json"),
    ])

    measurements = json.loads(
        (model_root / "measurements.json").read_text(encoding="utf-8")
    )
    errors = [
        item.get("error")
        for item in measurements.get("timeline", ())
        if item.get("error") is not None
    ]
    if errors:
        raise RuntimeError(f"{slug}: native timeline contains errors: {errors!r}")
    if not (model_root / "model.step").is_file() or not (model_root / "model.step").stat().st_size:
        raise RuntimeError(f"{slug}: native STEP export is empty")
    return model_root


def snapshot(slug: str, model_root: Path) -> None:
    target = model_root / "model.png"
    command = [
        "solidcraft-cli",
        "snapshot",
        str(model_root / "model.sc"),
        "--out",
        str(target),
        "--no-grid",
        "--no-axes",
    ]
    camera = camera_json(snapshot_camera(slug))
    if camera:
        command += ["--camera", camera]

    required = bool(MODELS[slug].get("native_snapshot_required"))
    completed = run(command, check=False)
    if completed.returncode:
        target.unlink(missing_ok=True)
        if required:
            raise RuntimeError(f"{slug}: required native snapshot failed")
    elif not target.is_file() or not target.stat().st_size:
        if required:
            raise RuntimeError(f"{slug}: required native snapshot is empty")

    for spec in extra_snapshots(slug):
        name = spec["name"]
        extra = model_root / name
        command = [
            "solidcraft-cli",
            "snapshot",
            str(model_root / "model.sc"),
            "--out",
            str(extra),
            "--no-grid",
            "--no-axes",
        ]
        extra_camera = camera_json(spec.get("camera"))
        if extra_camera:
            command += ["--camera", extra_camera]
        run(command)
        if not extra.is_file() or not extra.stat().st_size:
            raise RuntimeError(f"{slug}: extra snapshot is empty: {name}")


def run_native_checks(models: tuple[str, ...], native_root: Path) -> None:
    if not models:
        return
    run([
        sys.executable,
        "scripts/ci/run_native_mutations.py",
        str(native_root),
        "--models",
        *models,
    ])
    run([
        sys.executable,
        "scripts/ci/native_validation.py",
        str(native_root),
        "--models",
        *models,
    ])
    for slug in models:
        native_check(slug, native_root)


def compare_scpc(slug: str, native_root: Path) -> None:
    model_root = native_root / slug
    scpf_root = model_root / "scpf"
    scpc_root = model_root / "scpc"
    scpf_root.mkdir(parents=True, exist_ok=True)
    scpc_root.mkdir(parents=True, exist_ok=True)

    shutil.copy2(
        model_root / "measurements.json",
        scpf_root / "measurements.json",
    )
    commands = scpc_root / "commands.json"
    run([
        sys.executable,
        "-m",
        "scpc",
        str(source_path(ROOT, slug, "scpc")),
        "--out",
        str(commands),
    ])
    run([
        "solidcraft-cli",
        "run",
        str(commands),
        "--param-check",
        "strict",
        "--results",
        "--json-out",
        str(scpc_root / "results.json"),
        "--save",
        str(scpc_root / "model.sc"),
        "--out",
        str(scpc_root / "model.step"),
    ])
    run([
        "solidcraft-cli",
        "eval",
        str(scpc_root / "model.sc"),
        "--json-out",
        str(scpc_root / "measurements.json"),
    ])

    measurements = json.loads(
        (scpc_root / "measurements.json").read_text(encoding="utf-8")
    )
    if any(item.get("error") is not None for item in measurements.get("timeline", ())):
        raise RuntimeError(f"{slug}: SCPC native timeline contains errors")

    run([
        sys.executable,
        "scripts/ci/compare-scpc.py",
        str(native_root),
        slug,
    ])


def toolchain_metadata(*, image_reference: str, workflow_run: str) -> dict:
    solidcraft = os.environ.get("SOLIDCRAFT_VERSION", "")
    scpf_commit = os.environ.get("SCPF_COMMIT", "")
    scpc_commit = os.environ.get("SCPC_COMMIT", "")
    if not solidcraft or not scpf_commit or not scpc_commit:
        raise RuntimeError("CAD image is missing pinned toolchain metadata")
    if TESTED_SOLIDCRAFT_VERSION != solidcraft:
        raise RuntimeError(
            "Forge/SolidCraft qualification mismatch: "
            f"Forge expects {TESTED_SOLIDCRAFT_VERSION}, image uses {solidcraft}"
        )
    return {
        "schema": 1,
        "scpf_commit": scpf_commit,
        "scpf_release": version("scpf"),
        "scpc_commit": scpc_commit,
        "solidcraft_version": solidcraft,
        "workflow_run": str(workflow_run),
        "toolchain_image": image_reference,
        "verified": True,
    }


def copy_generated_commands(
    *,
    native_models: tuple[str, ...],
    scpc_models: tuple[str, ...],
    native_root: Path,
    generated_root: Path,
) -> None:
    for slug in native_models:
        target = generated_root / slug / "scpf" / "solidcraft.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(native_root / slug / "commands.json", target)
    for slug in scpc_models:
        target = generated_root / slug / "scpc" / "solidcraft.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(native_root / slug / "scpc" / "commands.json", target)


def build_site(
    *,
    plan: dict,
    output_root: Path,
    stable_store: Path,
    previous_site: Path,
    source_sha: str,
) -> None:
    if not plan["publishable"]:
        return
    run([
        sys.executable,
        "scripts/ci/build-results.py",
        "--generated",
        str(output_root / "models"),
        "--native",
        str(output_root / "native"),
        "--stable-store",
        str(stable_store),
        "--previous-site",
        str(previous_site),
        "--public-base",
        plan["public_base"],
        "--commit",
        source_sha,
        "--out",
        str(output_root / "site"),
    ])
    run([
        sys.executable,
        "scripts/ci/test-results.py",
        str(output_root / "site"),
        source_sha,
        plan["public_base"],
    ])
    for slug in plan["snapshot_models"]:
        image = output_root / "site" / "models" / slug / "native.png"
        if not image.is_file() or not image.stat().st_size:
            raise RuntimeError(f"{slug}: published native snapshot is missing")


def execute(
    *,
    plan_path: Path,
    output_root: Path,
    stable_store: Path,
    previous_site: Path,
    source_sha: str,
    workflow_run: str,
    image_reference: str,
) -> dict:
    plan = load_plan(plan_path)
    native_models = tuple(plan["native_models"])
    scpc_models = tuple(
        slug for slug in plan["scpc_models"]
        if slug in native_models
    )
    native_root = output_root / "native"
    generated_root = output_root / "models"

    metadata = toolchain_metadata(
        image_reference=image_reference,
        workflow_run=workflow_run,
    )
    (native_root).mkdir(parents=True, exist_ok=True)
    (native_root / "verification.json").write_text(
        json.dumps(
            {
                **metadata,
                "source_commit": source_sha,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    for slug in native_models:
        model_root = compile_native(slug, native_root)
        snapshot(slug, model_root)

    run_native_checks(native_models, native_root)

    for slug in scpc_models:
        compare_scpc(slug, native_root)

    copy_generated_commands(
        native_models=native_models,
        scpc_models=scpc_models,
        native_root=native_root,
        generated_root=generated_root,
    )

    if native_models:
        prepare_candidate(
            models=native_models,
            native_root=native_root,
            generated_root=generated_root,
            out=output_root / "candidate",
            metadata={
                **metadata,
                "source_commit": source_sha,
            },
        )

    build_site(
        plan=plan,
        output_root=output_root,
        stable_store=stable_store,
        previous_site=previous_site,
        source_sha=source_sha,
    )

    if plan["publishable"]:
        (output_root / "publish.json").write_text(
            json.dumps(
                {
                    "channel": plan["channel"],
                    "preview_key": plan["preview_key"],
                    "public_base": plan["public_base"],
                    "models": list(native_models),
                    "source_commit": source_sha,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--stable-store", type=Path, required=True)
    parser.add_argument("--previous-site", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--workflow-run", required=True)
    parser.add_argument("--image-reference", required=True)
    args = parser.parse_args()
    execute(
        plan_path=args.plan,
        output_root=args.out,
        stable_store=args.stable_store,
        previous_site=args.previous_site,
        source_sha=args.source_sha,
        workflow_run=args.workflow_run,
        image_reference=args.image_reference,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
