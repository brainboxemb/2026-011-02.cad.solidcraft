#!/usr/bin/env python3
"""Run the cheap compile/compare proof for one model-root CI item.

A physical model folder can own more than one catalog slug. GuideRail owns both
Festool and Makita variants, and Simple MFT owns both the worktop and assembly.
The mapping is derived from model_catalog.py so ci.yml is not a second catalog.

This is migration proof code. Native SolidCraft verification and durable
publication remain on the existing CAD pipeline until the later cutover.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from model_catalog import COMMAND_SOURCES, MODELS, model_build_path, source_path
from model_checks import command_check


ROOT = Path(__file__).resolve().parents[2]


def catalog_root(slug: str) -> Path:
    """Return the repository model root that owns one catalog slug.

    CAD model roots have one fixed shape: models/<section>/<folder>. Files
    below that root may add implementation or variant directories such as
    detailed/scpf or scpf/assemblies, but those are not separate CI items.
    """

    source = Path(MODELS[slug]["source"])
    parts = source.parts
    if len(parts) < 4 or parts[0] != "models":
        raise ValueError(
            f"{slug}: source is not below models/<section>/<folder>: {source}"
        )
    return Path(*parts[:3])


def item_members(item_root: Path) -> tuple[str, ...]:
    """Return all catalog slugs owned by one physical model folder."""

    relative = item_root.resolve().relative_to(ROOT.resolve())
    return tuple(
        slug for slug in MODELS
        if catalog_root(slug) == relative
    )


def item_id_for_slug(slug: str) -> str:
    """Return the stable item ID for the folder that owns one catalog slug."""

    root = catalog_root(slug)
    for candidate in MODELS:
        if catalog_root(candidate) == root:
            return candidate
    raise ValueError(f"{slug}: no model-root item found")


def item_dependencies(item_id: str) -> tuple[str, ...]:
    """Return unique folder-level dependencies from all variants in the item."""

    if item_id not in MODELS:
        raise ValueError(f"unknown model item: {item_id}")

    root = catalog_root(item_id)
    members = tuple(
        slug for slug in MODELS
        if catalog_root(slug) == root
    )
    result: list[str] = []
    for slug in members:
        for dependency in MODELS[slug].get("dependencies", ()):
            dependency_item = item_id_for_slug(dependency)
            if dependency_item != item_id and dependency_item not in result:
                result.append(dependency_item)
    return tuple(result)


def output_root() -> Path:
    """Return the item output directory supplied by tool.cad.ci."""

    value = os.environ.get("CAD_CI_OUTPUT")
    if not value:
        raise RuntimeError("CAD_CI_OUTPUT is required")
    return Path(value)


def current_item_root() -> Path:
    """Return the model folder supplied by tool.cad.ci."""

    value = os.environ.get("CAD_CI_ITEM_PATH")
    if not value:
        raise RuntimeError("CAD_CI_ITEM_PATH is required")
    return Path(value)


def generated_path(slug: str, language: str) -> Path:
    """Return the new command JSON path for one catalog variant."""

    return (
        output_root()
        / "generated"
        / slug
        / language
        / "solidcraft.json"
    )


def _sha256(path: Path) -> str:
    """Hash one file for the inspectable proof summaries."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> object:
    """Read JSON used for semantic reference comparison."""

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"missing generated/reference file: {path}") from exc


def _write_check(name: str, data: dict) -> None:
    """Write one proof file only after the complete item step passed."""

    target = output_root() / "checks" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _compile(module: str, source: Path, target: Path) -> None:
    """Compile one source through the pinned library in the CAD image."""

    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            sys.executable,
            "-m",
            module,
            str(source),
            "--out",
            str(target),
        ],
        cwd=ROOT,
        check=True,
    )


def compile_item() -> None:
    """Compile all SCPF and applicable SCPC variants in this model root."""

    members = item_members(current_item_root())
    if not members:
        raise RuntimeError(
            f"no catalog model belongs to {current_item_root()}"
        )

    rows: dict[str, dict] = {}
    for slug in members:
        scpf_target = generated_path(slug, "scpf")
        _compile("scpf", source_path(ROOT, slug), scpf_target)
        command_check(slug, scpf_target)

        row = {"scpf_sha256": _sha256(scpf_target)}
        reference = source_path(ROOT, slug).parent / "reference.json"
        if reference.is_file():
            if _read_json(scpf_target) != _read_json(reference):
                raise RuntimeError(
                    f"{slug}: generated SCPF commands differ from {reference}"
                )
            row["reference"] = str(reference.relative_to(ROOT))
            row["reference_sha256"] = _sha256(reference)

        if slug in COMMAND_SOURCES:
            scpc_target = generated_path(slug, "scpc")
            _compile(
                "scpc",
                source_path(ROOT, slug, "scpc"),
                scpc_target,
            )
            row["scpc_sha256"] = _sha256(scpc_target)

        rows[slug] = row

    _write_check(
        "compile.json",
        {"schema": 1, "status": "pass", "models": rows},
    )


def _existing_commands(slug: str, language: str) -> tuple[Path, str]:
    """Find old-pipeline output, preferring output from the current run.

    A shared item can contain an unchanged sibling variant that the old
    selector did not rebuild. Its accepted stable command JSON is then the
    correct comparison source.
    """

    current = (
        ROOT / "output" / "models" / slug / language / "solidcraft.json"
    )
    if current.is_file():
        return current, "current-run"

    stable = (
        ROOT
        / "generated-build"
        / "main"
        / model_build_path(slug)
        / "generated"
        / language
        / "solidcraft.json"
    )
    if stable.is_file():
        return stable, "stable-build"

    raise RuntimeError(
        f"{slug}: no current or stable {language} command JSON is available"
    )


def compare_current() -> None:
    """Require all new command documents to equal current/stable CAD output."""

    rows: dict[str, dict] = {}
    for slug in item_members(current_item_root()):
        row: dict[str, object] = {}
        languages = ["scpf"]
        if slug in COMMAND_SOURCES:
            languages.append("scpc")

        for language in languages:
            generated = generated_path(slug, language)
            existing, source = _existing_commands(slug, language)
            if generated.read_bytes() != existing.read_bytes():
                raise RuntimeError(
                    f"{slug}: tool.cad.ci {language} commands differ from "
                    f"{source} output"
                )
            row[language] = {
                "status": "pass",
                "source": source,
                "sha256": _sha256(generated),
            }
        rows[slug] = row

    _write_check(
        "current-pipeline.json",
        {"schema": 1, "status": "pass", "models": rows},
    )


def main() -> int:
    """Run one shared model-root migration step."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("compile", "compare-current"))
    args = parser.parse_args()

    if args.command == "compile":
        compile_item()
    else:
        compare_current()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
