"""Derive model last-modified timestamps from repository Git history.

This is presentation input only. It does not define model identity, category,
build participation or build success.
"""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import subprocess


class ModelHistoryError(RuntimeError):
    """Model history cannot be derived safely."""


def physical_model_roots(repo: Path) -> tuple[str, ...]:
    repo = repo.resolve()
    models_root = repo / "models"
    roots: list[str] = []

    for model_path in sorted(models_root.rglob("model.yml")):
        root = model_path.parent
        if not (root / "ci.yml").is_file():
            raise ModelHistoryError(f"model root has no ci.yml: {root}")
        roots.append(root.relative_to(models_root).as_posix())

    if not roots:
        raise ModelHistoryError("no physical CAD model roots found")
    return tuple(roots)


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def git_head(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD")


def git_lastmod(repo: Path, model_root: str) -> str:
    value = _git(
        repo,
        "log",
        "-1",
        "--format=%aI",
        "--",
        f"models/{model_root}",
    )
    if not value:
        raise ModelHistoryError(f"no Git history found for models/{model_root}")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ModelHistoryError(f"Git timestamp lacks timezone: {value}")
    return value


def build_manifest(
    repo: Path,
    *,
    source_commit: str | None = None,
    lastmod_resolver=git_lastmod,
) -> dict:
    repo = repo.resolve()
    source = source_commit or git_head(repo)
    roots = {
        model_root: lastmod_resolver(repo, model_root)
        for model_root in physical_model_roots(repo)
    }
    return {
        "schema": 1,
        "source_commit": source,
        "roots": roots,
    }


def write_manifest(repo: Path, manifest: dict) -> Path:
    target = repo / "site/data/cad/model_history.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return target
