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


def _catalog(repo: Path) -> tuple[list[dict], list[dict]]:
    path = repo / "site/data/cad/catalog.yml"
    catalog = _load_yaml(path)
    sections = catalog.get("sections")
    groups = catalog.get("groups")
    if not isinstance(sections, list) or not sections:
        raise PagesVerificationError(f"{path}: sections must be a non-empty list")
    if not isinstance(groups, list):
        raise PagesVerificationError(f"{path}: groups must be a list")

    def validate(rows: list[dict], kind: str) -> None:
        seen: set[str] = set()
        for row in rows:
            if not isinstance(row, dict):
                raise PagesVerificationError(f"{path}: {kind} row must be a mapping")
            key = row.get("id")
            title = row.get("title")
            if not isinstance(key, str) or not key:
                raise PagesVerificationError(f"{path}: {kind} row requires id")
            if key in seen:
                raise PagesVerificationError(f"{path}: duplicate {kind} id {key!r}")
            seen.add(key)
            if not isinstance(title, str) or not title:
                raise PagesVerificationError(f"{path}: {kind} {key!r} requires title")

    validate(sections, "section")
    validate(groups, "group")
    return sections, groups


def _source_metadata_by_id(repo: Path) -> dict[str, tuple[Path, dict]]:
    """Resolve current source metadata by public model id, independent of path moves."""
    found: dict[str, tuple[Path, dict]] = {}
    for ci_path in sorted((repo / "models").rglob("ci.yml")):
        ci = _load_yaml(ci_path)
        if ci.get("kind") == "group":
            continue
        model_path = ci_path.with_name("model.yml")
        if not model_path.is_file():
            continue
        root_metadata = _load_yaml(model_path)

        variants = ci.get("variants")
        if variants is not None:
            if not isinstance(variants, list):
                raise PagesVerificationError(f"{ci_path}: variants must be a list")
            ids = [row.get("id") for row in variants if isinstance(row, dict)]
        else:
            ids = [ci.get("id")]

        for variant_id in ids:
            if not isinstance(variant_id, str) or not variant_id:
                raise PagesVerificationError(f"{ci_path}: model id is missing")
            if variant_id in found:
                raise PagesVerificationError(
                    f"duplicate source model id {variant_id!r}: "
                    f"{found[variant_id][0]} and {model_path}"
                )
            found[variant_id] = (model_path, root_metadata)
    return found


def verify(
    *,
    repo: Path,
    site: Path,
    build_scope: Path,
    source_repository: str | None = None,
) -> None:
    repo = repo.resolve()
    site = site.resolve()
    build_scope = build_scope.resolve()

    plan = _load_json(build_scope / "build-plan.json")
    rows = plan.get("models")
    if not isinstance(rows, list) or not rows:
        raise PagesVerificationError("build plan contains no models")

    namespace = plan.get("namespace")
    if namespace not in {"main", "dev", "exp", "test"}:
        raise PagesVerificationError("build plan has invalid namespace")
    repository = source_repository or _repository_name(repo)
    blob_base = f"https://github.com/{repository}/blob/build/{namespace}/"
    raw_base = f"https://raw.githubusercontent.com/{repository}/build/{namespace}/"

    solidcraft = plan.get("solidcraft")
    if not isinstance(solidcraft, dict) or not isinstance(
        solidcraft.get("version"), str
    ):
        raise PagesVerificationError("build plan lacks SolidCraft version")
    solidcraft_version = solidcraft["version"]

    sections, groups = _catalog(repo)
    section_by_id = {row["id"]: row for row in sections}
    group_by_id = {row["id"]: row for row in groups}
    source_by_id = _source_metadata_by_id(repo)
    source_ids_by_path: dict[Path, list[str]] = {}
    for source_id, (source_path, _metadata) in source_by_id.items():
        source_ids_by_path.setdefault(source_path, []).append(source_id)

    _require_file(site / "index.html")
    _require_file(site / "models" / "index.html")
    category_html: dict[str, str] = {}
    for section in sections:
        category = section["id"]
        path = site / "models" / category / "index.html"
        _require_file(path)
        html = path.read_text(encoding="utf-8")
        if "cad-model-grid" not in html or "cad-model-detail" in html:
            raise PagesVerificationError(
                f"{path}: expected a category grid, not a model detail"
            )
        category_html[category] = html

    home_html = (site / "index.html").read_text(encoding="utf-8")
    if "Recently updated models" not in home_html:
        raise PagesVerificationError("home page lacks recently-updated catalog")

    catalog_html = (site / "models" / "index.html").read_text(encoding="utf-8")
    for section in sections:
        heading = section["title"]
        if heading not in catalog_html:
            raise PagesVerificationError(
                f"model catalog lacks section heading {heading!r}"
            )

    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise PagesVerificationError("build-plan model row must be an object")

        variant_id = row.get("id")
        if not isinstance(variant_id, str) or not variant_id:
            raise PagesVerificationError("build-plan row requires id")
        if variant_id in seen:
            raise PagesVerificationError(f"duplicate build-plan model id: {variant_id}")
        seen.add(variant_id)

        source = source_by_id.get(variant_id)
        if source is None:
            raise PagesVerificationError(
                f"durable build model {variant_id!r} has no current source owner"
            )
        model_path, root_metadata = source

        category = root_metadata.get("section")
        if category not in section_by_id or category not in category_html:
            raise PagesVerificationError(
                f"{model_path}: unsupported section {category!r}"
            )
        group = root_metadata.get("group")
        if group is not None and group not in group_by_id:
            raise PagesVerificationError(
                f"{model_path}: unsupported group {group!r}"
            )
        owner_variant_ids = source_ids_by_path.get(model_path, [])
        has_owner_page = len(owner_variant_ids) > 1
        owner_href = None
        owner_page_path = None
        if has_owner_page:
            try:
                owner_rel = model_path.parent.relative_to(repo / "models")
            except ValueError as exc:
                raise PagesVerificationError(
                    f"{model_path}: model owner is outside models/"
                ) from exc
            owner_href = f"/models/owners/{owner_rel.as_posix()}/"
            owner_page_path = site / "models" / "owners" / owner_rel / "index.html"
            expected_catalog_href = owner_href
        else:
            expected_catalog_href = f"/models/{variant_id}/"

        if expected_catalog_href not in category_html[category]:
            raise PagesVerificationError(
                f"{category}: missing model-owner link for {variant_id}"
            )

        if group is not None:
            group_html = category_html[category]
            group_markers = (
                f'data-cad-group="{group}"',
                f"data-cad-group={group}",
            )
            if not any(marker in group_html for marker in group_markers):
                raise PagesVerificationError(
                    f"{category}: missing structural group {group!r}"
                )
            group_title = group_by_id[group]["title"]
            if group_title not in group_html:
                raise PagesVerificationError(
                    f"{category}: missing group heading {group_title!r}"
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
        if has_owner_page:
            assert owner_href is not None
            assert owner_page_path is not None
            _require_file(owner_page_path)
            owner_html = owner_page_path.read_text(encoding="utf-8")
            if f"/models/{variant_id}/" not in owner_html:
                raise PagesVerificationError(
                    f"{owner_page_path}: missing variant link for {variant_id}"
                )
            if owner_href not in html:
                raise PagesVerificationError(
                    f"{page_path}: missing physical-owner back link"
                )

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

        drawings = row.get("drawings", [])
        if not isinstance(drawings, list):
            raise PagesVerificationError(
                f"{variant_id}: drawings must be a list"
            )
        for drawing in drawings:
            if (
                not isinstance(drawing, dict)
                or not isinstance(drawing.get("name"), str)
                or not drawing["name"]
                or not isinstance(drawing.get("drawing"), str)
                or not drawing["drawing"].startswith("$")
                or not isinstance(drawing.get("path"), str)
                or not drawing["path"].endswith(".pdf")
            ):
                raise PagesVerificationError(
                    f"{variant_id}: invalid drawing artifact declaration"
                )
            artifact = drawing["path"]
            pdf = build_scope / artifact
            _require_file(pdf)
            if pdf.read_bytes()[:5] != b"%PDF-":
                raise PagesVerificationError(
                    f"{variant_id}: drawing artifact is not a PDF: {artifact}"
                )
            if f"{blob_base}{artifact}" not in html:
                raise PagesVerificationError(
                    f"{variant_id}: page does not link drawing PDF"
                )
            if f"{raw_base}{artifact}" not in html:
                raise PagesVerificationError(
                    f"{variant_id}: page does not expose drawing PDF"
                )

            preview = drawing.get("preview")
            inspection = drawing.get("inspect")
            if preview is not None or inspection is not None:
                if (
                    not isinstance(preview, str)
                    or not preview.endswith(".png")
                    or not isinstance(inspection, str)
                    or not inspection.endswith(".json")
                ):
                    raise PagesVerificationError(
                        f"{variant_id}: invalid drawing preview declaration"
                    )
                preview_file = build_scope / preview
                inspect_file = build_scope / inspection
                _require_file(preview_file)
                _require_file(inspect_file)
                if preview_file.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                    raise PagesVerificationError(
                        f"{variant_id}: drawing preview is not a PNG"
                    )
                _load_json(inspect_file)
                if f"{raw_base}{preview}" not in html:
                    raise PagesVerificationError(
                        f"{variant_id}: page does not expose drawing preview"
                    )
                if "cad-drawing-frame" in html:
                    raise PagesVerificationError(
                        f"{variant_id}: page still auto-loads drawing PDF"
                    )

            duplicate = page_root / "drawings" / Path(artifact).name
            if duplicate.exists():
                raise PagesVerificationError(
                    f"{variant_id}: drawing PDF duplicated in Pages: {duplicate}"
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
    parser.add_argument("--source-repository")
    args = parser.parse_args(argv)

    verify(
        repo=args.repo,
        site=args.site,
        build_scope=args.build_scope,
        source_repository=args.source_repository,
    )
    print("Generated Pages link durable build artifacts without copying them")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
