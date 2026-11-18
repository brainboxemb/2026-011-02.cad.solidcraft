"""Prepare verified per-model native candidates for tool.cad.ci packaging.

This module owns the CAD-specific input fingerprint and the temporary native
candidate produced inside the immutable CAD container. Durable build storage,
promotion, previews and Git publication are owned by tool.cad.ci.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import zipfile

from model_catalog import MODELS, model_build_path, verification_input_paths


ROOT = Path(__file__).resolve().parents[2]
VERIFICATION_FILE = "verification.json"


def input_fingerprint(slug: str, root: Path = ROOT) -> str:
    """Hash only source/geometry inputs that define one native CAD result."""

    if slug not in MODELS:
        raise ValueError(f"unknown model: {slug}")

    digest = hashlib.sha256()
    files: set[Path] = set()
    for watched in verification_input_paths(slug):
        candidate = root / watched
        if watched.endswith("/"):
            if candidate.is_dir():
                files.update(
                    path
                    for path in candidate.rglob("*")
                    if path.is_file()
                    and "__pycache__" not in path.parts
                    and not path.name.endswith((".pyc", ".pyo"))
                )
        elif candidate.is_file():
            files.add(candidate)

    if not files:
        raise FileNotFoundError(f"{slug}: no declared input files found")

    # Include paths as well as bytes so renames and file moves change identity.
    for path in sorted(files):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def native_file_format(model_sc: Path) -> str | None:
    """Return the SolidCraft document format from a native .sc ZIP."""

    if not model_sc.is_file() or not zipfile.is_zipfile(model_sc):
        return None
    with zipfile.ZipFile(model_sc) as archive:
        document = json.loads(archive.read("document.json"))
    value = document.get("format")
    return value if isinstance(value, str) else None


def _copy_tree_if_present(source: Path | None, destination: Path) -> None:
    """Copy an optional generated-command directory into the candidate."""

    if source is None or not source.is_dir():
        return
    shutil.copytree(source, destination)


def prepare_candidate(
    *,
    models,
    native_root: Path,
    generated_root: Path | None,
    out: Path,
    metadata: dict,
) -> None:
    """Write verified per-model native output for the later package step.

    This is a temporary handoff inside one workflow run. The model-root package
    step reads it, combines it with generated commands and lets tool.cad.ci
    record the durable item state.
    """

    models = tuple(models)
    unknown = [slug for slug in models if slug not in MODELS]
    if unknown:
        raise ValueError(f"unknown model(s): {', '.join(unknown)}")

    missing = [
        slug
        for slug in models
        if not (native_root / slug).is_dir()
    ]
    if missing:
        raise FileNotFoundError(
            "missing native output for selected model(s): "
            + ", ".join(missing)
        )

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    for slug in models:
        target = out / model_build_path(slug)
        target.mkdir(parents=True)
        shutil.copytree(native_root / slug, target / "native")
        _copy_tree_if_present(
            generated_root / slug if generated_root is not None else None,
            target / "generated",
        )

        row = dict(metadata)
        row["model"] = slug
        row["verified"] = True
        row["input_fingerprint"] = input_fingerprint(slug)
        file_format = native_file_format(native_root / slug / "model.sc")
        if file_format:
            row["native_file_format"] = file_format
        (target / VERIFICATION_FILE).write_text(
            json.dumps(row, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    (out / "selection.json").write_text(
        json.dumps({"models": list(models)}, indent=2) + "\n",
        encoding="utf-8",
    )
