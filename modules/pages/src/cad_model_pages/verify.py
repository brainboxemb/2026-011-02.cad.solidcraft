"""Verify generated model Pages against one build scope."""

from __future__ import annotations

import argparse
from pathlib import Path
import json

import yaml


class PagesVerificationError(RuntimeError):
    """Generated Pages do not match the accepted build scope."""


def _require_file(path: Path) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise PagesVerificationError(f"missing generated Pages file: {path}")


def _load_json(path: Path) -> dict:
    _require_file(path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PagesVerificationError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PagesVerificationError(f"expected JSON object: {path}")
    return value


def _load_yaml(path: Path) -> dict:
    _require_file(path)
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise PagesVerificationError(f"expected YAML mapping: {path}")
    return value


def _metadata_for_variant(model: dict, variant_id: str, path: Path) -> dict:
    variants = model.get("variants")
    if variants is None:
        return model
    if not isinstance(variants, dict):
        raise PagesVerificationError(f"model variants must be a mapping: {path}")
    value = variants.get(variant_id)
    if not isinstance(value, dict):
        raise PagesVerificationError(
            f"{path}: no presentation metadata for build variant {variant_id!r}"
        )
    return value


def verify(*, repo: Path, site: Path, build_scope: Path) -> None:
    repo = repo.resolve()
    site = site.resolve()
    build_scope = build_scope.resolve()

    plan = _load_json(build_scope / "build-plan.json")
    rows = plan.get("models")
    if not isinstance(rows, list) or not rows:
        raise PagesVerificationError("build plan contains no models")

    solidcraft = plan.get("solidcraft")
    if not isinstance(solidcraft, dict) or not isinstance(
        solidcraft.get("version"), str
    ):
        raise PagesVerificationError("build plan lacks SolidCraft version")
    solidcraft_version = solidcraft["version"]

    _require_file(site / "index.html")
    _require_file(site / "models" / "index.html")

    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise PagesVerificationError("build-plan model row must be an object")

        variant_id = row.get("id")
        model_root = row.get("root")
        if (
            not isinstance(variant_id, str)
            or not variant_id
            or not isinstance(model_root, str)
            or not model_root
        ):
            raise PagesVerificationError("build-plan row requires id and root")
        if variant_id in seen:
            raise PagesVerificationError(f"duplicate build-plan model id: {variant_id}")
        seen.add(variant_id)

        model_path = repo / model_root / "model.yml"
        metadata = _metadata_for_variant(
            _load_yaml(model_path),
            variant_id,
            model_path,
        )
        title = metadata.get("title")
        parameters = metadata.get("parameters")
        if not isinstance(title, str) or not title:
            raise PagesVerificationError(f"{model_path}: missing model title")
        if not isinstance(parameters, str) or not parameters:
            raise PagesVerificationError(f"{model_path}: missing model parameters")

        page_root = site / "models" / variant_id
        page_path = page_root / "index.html"
        _require_file(page_path)
        html = page_path.read_text(encoding="utf-8")
        for expected in (
            title,
            parameters,
            f"Built in SolidCraft {solidcraft_version}",
        ):
            if expected not in html:
                raise PagesVerificationError(
                    f"{page_path}: expected rendered text {expected!r}"
                )

        for name in (
            "model.png",
            "model.sc",
            "model.step",
            "solidcraft.json",
            "scpf-source.py",
            "model.yml",
            "ci.yml",
        ):
            _require_file(page_root / name)

        native = row.get("native")
        if not isinstance(native, dict):
            raise PagesVerificationError(f"{variant_id}: missing native artifact map")
        if native.get("stl"):
            _require_file(page_root / "model.stl")

        snapshots = row.get("snapshots", [])
        if not isinstance(snapshots, list):
            raise PagesVerificationError(f"{variant_id}: snapshots must be a list")
        for snapshot in snapshots:
            if not isinstance(snapshot, dict) or not isinstance(
                snapshot.get("name"), str
            ):
                raise PagesVerificationError(
                    f"{variant_id}: invalid snapshot declaration"
                )
            _require_file(page_root / snapshot["name"])

        command_doc = _load_json(page_root / "solidcraft.json")
        commands = command_doc.get("commands")
        if not isinstance(commands, list) or not commands:
            raise PagesVerificationError(
                f"{variant_id}: generated command JSON contains no commands"
            )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--build-scope", type=Path, required=True)
    args = parser.parse_args(argv)

    verify(repo=args.repo, site=args.site, build_scope=args.build_scope)
    print("Generated Pages match build plan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
