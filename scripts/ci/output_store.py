"""Prepare and promote verified per-model CAD build output.

This module contains no GitHub-specific code. Workflows check out the
build branch and call these functions/CLI against that working tree.
"""
from __future__ import annotations

from argparse import ArgumentParser
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import zipfile

from model_catalog import MODELS, model_build_path, verification_input_paths, model_slugs

ROOT = Path(__file__).resolve().parents[2]


VERIFICATION_FILE = "verification.json"


def parse_models(value):
    return tuple(
        item.strip()
        for item in value.replace(",", " ").split()
        if item.strip()
    )


def safe_preview_key(value):
    """Return a stable filesystem key for a PR/branch preview."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = value.strip(".-")
    if not value:
        raise ValueError("preview key must contain a usable character")
    return value


def input_fingerprint(slug, root=ROOT):
    """Hash only geometry/source inputs that define one native CAD result."""
    if slug not in MODELS:
        raise ValueError(f"unknown model: {slug}")
    digest = hashlib.sha256()
    files = set()
    for watched in verification_input_paths(slug):
        candidate = root / watched
        if watched.endswith("/"):
            if candidate.is_dir():
                files.update(
                    path for path in candidate.rglob("*")
                    if path.is_file()
                    and "__pycache__" not in path.parts
                    and not path.name.endswith((".pyc", ".pyo"))
                )
        elif candidate.is_file():
            files.add(candidate)

    if not files:
        raise FileNotFoundError(f"{slug}: no declared input files found")

    for path in sorted(files):
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def verification_metadata(
    *,
    slug,
    source_commit,
    scpf_commit,
    scpf_release,
    scpc_commit,
    solidcraft_version,
    workflow_run,
    toolchain_image,
    native_file_format=None,
):
    if slug not in MODELS:
        raise ValueError(f"unknown model: {slug}")
    data = {
        "schema": 1,
        "model": slug,
        "source_commit": source_commit,
        "scpf_commit": scpf_commit,
        "scpf_release": scpf_release,
        "scpc_commit": scpc_commit,
        "solidcraft_version": solidcraft_version,
        "workflow_run": str(workflow_run),
        "toolchain_image": toolchain_image,
        "verified": True,
    }
    if native_file_format:
        data["native_file_format"] = native_file_format
    return data


def native_file_format(model_sc):
    """Read the SolidCraft document format from a native .sc ZIP."""
    if not model_sc.is_file() or not zipfile.is_zipfile(model_sc):
        return None
    with zipfile.ZipFile(model_sc) as archive:
        document = json.loads(archive.read("document.json"))
    value = document.get("format")
    return value if isinstance(value, str) else None


def _copy_tree_if_present(source, destination):
    if source is None or not source.is_dir():
        return
    shutil.copytree(source, destination)


def prepare_candidate(
    *,
    models,
    native_root,
    generated_root,
    out,
    metadata,
):
    """Create one self-contained candidate output for selected models."""
    models = tuple(models)
    unknown = [slug for slug in models if slug not in MODELS]
    if unknown:
        raise ValueError(f"unknown model(s): {', '.join(unknown)}")

    missing = [
        slug for slug in models
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


def migrate_legacy_store_layout(*, store):
    """Copy a complete legacy stable/models tree into build/main source paths."""
    legacy = store / "stable" / "models"
    expected = tuple(model_slugs("native"))
    if not legacy.is_dir():
        return ()

    missing = [
        slug
        for slug in expected
        if not (legacy / slug / VERIFICATION_FILE).is_file()
    ]
    if missing:
        raise ValueError(
            "legacy build store is incomplete; missing: " + ", ".join(missing)
        )

    with tempfile.TemporaryDirectory() as tmp:
        candidate = Path(tmp) / "candidate"
        candidate.mkdir(parents=True)
        for slug in expected:
            source = legacy / slug
            row = json.loads(
                (source / VERIFICATION_FILE).read_text(encoding="utf-8")
            )
            if row.get("model") != slug or row.get("verified") is not True:
                raise ValueError(f"{slug}: invalid legacy verification")
            target = candidate / model_build_path(slug)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, target)

        promote_candidate(
            candidate=candidate,
            store=store,
            models=expected,
            channel="stable",
        )
    return expected


def migrate_legacy_pages(*, pages, store, source_root=ROOT):
    """Bootstrap stable model-output from one complete legacy Pages build."""
    provenance_file = pages / "provenance.json"
    if not provenance_file.is_file():
        raise FileNotFoundError("legacy Pages provenance.json is missing")
    legacy = json.loads(provenance_file.read_text(encoding="utf-8"))

    expected = tuple(model_slugs("native"))
    verified = tuple(legacy.get("native_verified_models", ()))
    if set(verified) != set(expected) or len(verified) != len(expected):
        raise ValueError(
            "legacy Pages is not a complete native catalog; "
            f"expected {len(expected)} models, got {len(verified)}"
        )

    required = (
        "source_commit",
        "scpf_commit",
        "scpf_release",
        "scpc_commit",
        "solidcraft_version",
        "workflow_run",
        "native_file_format",
    )
    missing = [key for key in required if not legacy.get(key)]
    if missing:
        raise ValueError(
            "legacy Pages lacks verification fields: " + ", ".join(missing)
        )

    with tempfile.TemporaryDirectory() as tmp:
        candidate = Path(tmp) / "candidate"
        candidate.mkdir(parents=True)

        for slug in expected:
            published = pages / "models" / slug
            if not published.is_dir():
                raise FileNotFoundError(
                    f"legacy Pages model directory is missing: {slug}"
                )
            native_file = published / "model.sc"
            if not native_file.is_file() or not zipfile.is_zipfile(native_file):
                raise ValueError(
                    f"legacy Pages model has no valid native .sc: {slug}"
                )
            actual_format = native_file_format(native_file)
            if actual_format != legacy["native_file_format"]:
                raise ValueError(
                    f"{slug}: legacy native format {actual_format!r} does not "
                    f"match {legacy['native_file_format']!r}"
                )
            command_file = published / "solidcraft.json"
            if not command_file.is_file():
                raise FileNotFoundError(
                    f"legacy Pages command JSON is missing: {slug}"
                )

            target = candidate / model_build_path(slug)
            native = target / "native"
            generated = target / "generated" / "scpf"
            native.mkdir(parents=True)
            generated.mkdir(parents=True)

            for filename in ("model.sc", "native.png", "front.png", "rear.png"):
                source = published / filename
                if source.is_file():
                    target_name = "model.png" if filename == "native.png" else filename
                    shutil.copy2(source, native / target_name)
            shutil.copy2(command_file, generated / "solidcraft.json")

            scpc = published / "scpc-commands.json"
            if scpc.is_file():
                target_scpc = target / "generated" / "scpc"
                target_scpc.mkdir(parents=True)
                shutil.copy2(scpc, target_scpc / "solidcraft.json")

            verification = {
                "schema": 1,
                "model": slug,
                "source_commit": legacy["source_commit"],
                "scpf_commit": legacy["scpf_commit"],
                "scpf_release": legacy["scpf_release"],
                "scpc_commit": legacy["scpc_commit"],
                "solidcraft_version": legacy["solidcraft_version"],
                "workflow_run": str(legacy["workflow_run"]),
                "native_file_format": actual_format,
                "input_fingerprint": input_fingerprint(slug, source_root),
                "verified": True,
                "legacy_migrated": True,
            }
            (target / VERIFICATION_FILE).write_text(
                json.dumps(verification, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

        promote_candidate(
            candidate=candidate,
            store=store,
            models=expected,
            channel="stable",
        )
    return expected


def _validate_candidate(candidate, models):
    missing = []
    for slug in models:
        model = candidate / model_build_path(slug)
        verification = model / VERIFICATION_FILE
        if not model.is_dir() or not verification.is_file():
            missing.append(slug)
            continue
        row = json.loads(verification.read_text(encoding="utf-8"))
        if row.get("model") != slug or row.get("verified") is not True:
            raise ValueError(f"{slug}: invalid candidate verification")
    if missing:
        raise FileNotFoundError(
            "candidate is incomplete for model(s): " + ", ".join(missing)
        )


def destination_root(store, *, channel, preview_key=None):
    if channel == "stable":
        return store / "main"
    if channel == "preview":
        if preview_key is None:
            raise ValueError("preview channel requires preview_key")
        key = safe_preview_key(preview_key)
        if key.startswith("pr-") and key[3:].isdigit():
            return store / "pr" / key[3:]
        return store / "preview" / key
    raise ValueError(f"unknown output channel: {channel}")


def promote_candidate(
    *,
    candidate,
    store,
    models,
    channel,
    preview_key=None,
):
    """Promote selected candidate models without touching other model output.

    Candidate completeness is validated before the first destination changes.
    Each selected model is copied to a sibling temporary directory and then
    renamed into place, so incomplete copy operations cannot expose a partial
    model directory.
    """
    models = tuple(models)
    _validate_candidate(candidate, models)

    root = destination_root(
        store,
        channel=channel,
        preview_key=preview_key,
    )
    staged = []
    try:
        for slug in models:
            source = candidate / model_build_path(slug)
            target = root / model_build_path(slug)
            target.parent.mkdir(parents=True, exist_ok=True)
            temp = Path(
                tempfile.mkdtemp(
                    prefix=f".{target.name}-",
                    dir=target.parent,
                )
            )
            shutil.rmtree(temp)
            shutil.copytree(source, temp)
            staged.append((slug, target, temp))

        for slug, target, temp in staged:
            backup = target.parent / f".{target.name}.previous"
            if backup.exists():
                shutil.rmtree(backup)
            if target.exists():
                target.rename(backup)
            try:
                temp.rename(target)
            except Exception:
                if backup.exists() and not target.exists():
                    backup.rename(target)
                raise
            if backup.exists():
                shutil.rmtree(backup)
    finally:
        for _, _, temp in staged:
            if temp.exists():
                shutil.rmtree(temp)


def normalize_native_snapshots(store, *, channel="stable", preview_key=None):
    """Normalize legacy primary screenshots to native/model.png."""
    root = destination_root(
        store,
        channel=channel,
        preview_key=preview_key,
    )
    if not root.is_dir():
        return ()

    normalized = []
    for verification in tuple(root.rglob(VERIFICATION_FILE)):
        model_root = verification.parent
        try:
            row = json.loads(verification.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        slug = row.get("model")
        if not isinstance(slug, str) or slug not in MODELS:
            continue

        native = model_root / "native"
        legacy = native / "native.png"
        canonical = native / "model.png"
        if legacy.is_file():
            canonical.parent.mkdir(parents=True, exist_ok=True)
            if not canonical.exists():
                legacy.rename(canonical)
            else:
                legacy.unlink()
            normalized.append(slug)
    return tuple(sorted(set(normalized)))


def prune_removed_models(store, *, channel="stable", preview_key=None):
    """Remove stored build items whose verification names a retired model."""
    root = destination_root(
        store,
        channel=channel,
        preview_key=preview_key,
    )
    if not root.is_dir():
        return ()
    removed = []
    for verification in tuple(root.rglob(VERIFICATION_FILE)):
        model_root = verification.parent
        try:
            row = json.loads(verification.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        slug = row.get("model")
        if isinstance(slug, str) and slug not in MODELS:
            shutil.rmtree(model_root)
            removed.append(slug)
    return tuple(sorted(set(removed)))


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare")
    prepare.add_argument("--models", required=True)
    prepare.add_argument("--native", type=Path, required=True)
    prepare.add_argument("--generated", type=Path)
    prepare.add_argument("--out", type=Path, required=True)
    prepare.add_argument("--source-commit", required=True)
    prepare.add_argument("--scpf-commit", required=True)
    prepare.add_argument("--scpf-release", required=True)
    prepare.add_argument("--scpc-commit", required=True)
    prepare.add_argument("--solidcraft-version", required=True)
    prepare.add_argument("--workflow-run", required=True)
    prepare.add_argument("--toolchain-image", required=True)
    prepare.add_argument("--native-file-format")

    promote = sub.add_parser("promote")
    promote.add_argument("--models", required=True)
    promote.add_argument("--candidate", type=Path, required=True)
    promote.add_argument("--store", type=Path, required=True)
    promote.add_argument("--channel", choices=("stable", "preview"), required=True)
    promote.add_argument("--preview-key")

    migrate = sub.add_parser("migrate-pages")
    migrate.add_argument("--pages", type=Path, required=True)
    migrate.add_argument("--store", type=Path, required=True)

    migrate_store = sub.add_parser("migrate-store")
    migrate_store.add_argument("--store", type=Path, required=True)

    prune = sub.add_parser("prune")
    prune.add_argument("--store", type=Path, required=True)
    prune.add_argument("--channel", choices=("stable", "preview"), default="stable")
    prune.add_argument("--preview-key")

    args = parser.parse_args()

    if args.command == "prepare":
        models = parse_models(args.models)
        metadata = {
            "schema": 1,
            "source_commit": args.source_commit,
            "scpf_commit": args.scpf_commit,
            "scpf_release": args.scpf_release,
            "scpc_commit": args.scpc_commit,
            "solidcraft_version": args.solidcraft_version,
            "workflow_run": str(args.workflow_run),
            "toolchain_image": args.toolchain_image,
            "verified": True,
        }
        if args.native_file_format:
            metadata["native_file_format"] = args.native_file_format
        prepare_candidate(
            models=models,
            native_root=args.native,
            generated_root=args.generated,
            out=args.out,
            metadata=metadata,
        )
    elif args.command == "migrate-pages":
        migrated = migrate_legacy_pages(
            pages=args.pages,
            store=args.store,
        )
        print(" ".join(migrated))
    elif args.command == "migrate-store":
        migrated = migrate_legacy_store_layout(store=args.store)
        print(" ".join(migrated))
    elif args.command == "promote":
        promote_candidate(
            candidate=args.candidate,
            store=args.store,
            models=parse_models(args.models),
            channel=args.channel,
            preview_key=args.preview_key,
        )
    else:
        removed = prune_removed_models(
            args.store,
            channel=args.channel,
            preview_key=args.preview_key,
        )
        print(" ".join(removed))


if __name__ == "__main__":
    main()
