"""Verify generated model Pages against one durable build scope."""

from __future__ import annotations

import argparse
from pathlib import Path
import json
import tomllib

import yaml


class PagesVerificationError(RuntimeError):
    """Generated Pages do not match the accepted build scope."""


def _require_file(path: Path) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise PagesVerificationError(f"missing file: {path}")


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


def _repository_name(repo: Path) -> str:
    config_path = repo / "site/config/_default/hugo.toml"
    _require_file(config_path)
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    value = config.get("params", {}).get("cadSourceRepository")
    if not isinstance(value, str) or not value:
        raise PagesVerificationError(
            f"{config_path}: missing params.cadSourceRepository"
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

    namespace = plan.get("namespace")
    if namespace not in {"main", "dev"}:
        raise PagesVerificationError("build plan has invalid namespace")
    repository = _repository_name(repo)
    blob_base = f"https://github.com/{repository}/blob/build/{namespace}/"
    raw_base = f"https://raw.githubusercontent.com/{repository}/build/{namespace}/"

    solidcraft = plan.get("solidcraft")
    if not isinstance(solidcraft, dict) or not isinstance(
        solidcraft.get("version"), str
    ):
        raise PagesVerificationError("build plan lacks SolidCraft version")
    solidcraft_version = solidcraft["version"]

    _require_file(site / "index.html")
    _require_file(site / "models" / "index.html")
    category_html = {}
    for category in ("basic", "components", "advanced"):
        path = site / "models" / category / "index.html"
        _require_file(path)
        html = path.read_text(encoding="utf-8")
        if (
            "cad-category-page" not in html
            or "cad-model-grid" not in html
            or "cad-model-detail" in html
        ):
            raise PagesVerificationError(
                f"{path}: expected a category grid, not a model detail"
            )
        category_html[category] = html

    home_html = (site / "index.html").read_text(encoding="utf-8")
    if "Recently updated models" not in home_html:
        raise PagesVerificationError("home page lacks recently-updated catalog")

    catalog_html = (site / "models" / "index.html").read_text(encoding="utf-8")
    for heading in ("Basic Models", "Components", "Advanced Models"):
        if heading not in catalog_html:
            raise PagesVerificationError(
                f"model catalog lacks category heading {heading!r}"
            )

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
        root_metadata = _load_yaml(model_path)
        category = root_metadata.get("section")
        if category not in category_html:
            raise PagesVerificationError(
                f"{model_path}: unsupported category {category!r}"
            )
        if f"/models/{variant_id}/" not in category_html[category]:
            raise PagesVerificationError(
                f"{category}: missing model link for {variant_id}"
            )

        metadata = _metadata_for_variant(root_metadata, variant_id, model_path)
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
            f"<code>{namespace}</code>",
        ):
            if expected not in html:
                raise PagesVerificationError(
                    f"{page_path}: expected rendered text {expected!r}"
                )

        for source_name in ("scpf-source.py", "model.yml", "ci.yml"):
            _require_file(page_root / source_name)

        commands = row.get("commands")
        if not isinstance(commands, str) or not commands:
            raise PagesVerificationError(f"{variant_id}: missing command path")
        command_path = build_scope / commands
        command_doc = _load_json(command_path)
        if not isinstance(command_doc.get("commands"), list) or not command_doc["commands"]:
            raise PagesVerificationError(
                f"{variant_id}: generated command JSON contains no commands"
            )
        if f"{blob_base}{commands}" not in html:
            raise PagesVerificationError(
                f"{variant_id}: page does not link durable command JSON"
            )

        native = row.get("native")
        if not isinstance(native, dict):
            raise PagesVerificationError(
                f"{variant_id}: missing native artifact map"
            )
        for key in ("png", "sc", "step"):
            artifact = native.get(key)
            if not isinstance(artifact, str) or not artifact:
                raise PagesVerificationError(
                    f"{variant_id}: missing native {key} path"
                )
            _require_file(build_scope / artifact)
            if key == "png":
                if f"{raw_base}{artifact}" not in html:
                    raise PagesVerificationError(
                        f"{variant_id}: preview does not use durable build image"
                    )
            elif f"{blob_base}{artifact}" not in html:
                raise PagesVerificationError(
                    f"{variant_id}: page does not link native {key}"
                )

        stl = native.get("stl")
        if stl:
            _require_file(build_scope / stl)
            if f"{blob_base}{stl}" not in html:
                raise PagesVerificationError(
                    f"{variant_id}: STL does not link GitHub build viewer"
                )

        generated_names = {
            "model.png",
            "model.sc",
            "model.step",
            "model.stl",
            "solidcraft.json",
        }
        snapshots = row.get("snapshots", [])
        if not isinstance(snapshots, list):
            raise PagesVerificationError(
                f"{variant_id}: snapshots must be a list"
            )
        for snapshot in snapshots:
            if (
                not isinstance(snapshot, dict)
                or not isinstance(snapshot.get("name"), str)
                or not isinstance(snapshot.get("path"), str)
            ):
                raise PagesVerificationError(
                    f"{variant_id}: invalid snapshot declaration"
                )
            _require_file(build_scope / snapshot["path"])
            generated_names.add(snapshot["name"])

        for name in generated_names:
            duplicate = page_root / name
            if duplicate.exists():
                raise PagesVerificationError(
                    f"{variant_id}: generated artifact duplicated in Pages: {duplicate}"
                )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--build-scope", type=Path, required=True)
    args = parser.parse_args(argv)

    verify(repo=args.repo, site=args.site, build_scope=args.build_scope)
    print("Generated Pages link durable build artifacts without copying them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
