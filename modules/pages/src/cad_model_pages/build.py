"""Build and verify one Hugo Pages scope from a source checkout."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess

from .history import build_manifest, write_manifest
from .verify import PagesVerificationError, verify


_HEXTRA = "github.com/imfing/hextra@v0.13.0"


def _stage_build_scope(source_root: Path, build_scope: Path) -> Path:
    """Stage one build scope at the mount path expected by the site config."""
    target = (source_root / "prepared-build" / "main").resolve()
    build_scope = build_scope.resolve()
    if build_scope == target:
        return target
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(build_scope, target)
    return target


def build(
    *,
    source_root: Path,
    build_scope: Path,
    destination: Path,
    base_url: str,
    source_ref: str,
    source_repository: str | None = None,
) -> None:
    source_root = source_root.resolve()
    build_scope = build_scope.resolve()
    build_namespace = build_scope.name
    destination = destination.resolve()

    site_root = source_root / "site"
    if not site_root.is_dir():
        raise PagesVerificationError(f"missing site root: {site_root}")

    staged_scope = _stage_build_scope(source_root, build_scope)
    write_manifest(source_root, build_manifest(source_root))

    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    env["HUGO_BASEURL"] = base_url
    env["HUGO_PARAMS_SOURCEREF"] = source_ref
    env["HUGO_PARAMS_BUILDSCOPE"] = build_namespace
    if source_repository:
        env["HUGO_PARAMS_CADSOURCEREPOSITORY"] = source_repository

    graph = subprocess.run(
        ["hugo", "mod", "graph"],
        cwd=site_root,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )
    if _HEXTRA not in graph.stdout:
        raise PagesVerificationError(
            f"site does not resolve accepted Hextra version {_HEXTRA}"
        )

    subprocess.run(
        [
            "hugo",
            "--minify",
            "--printPathWarnings",
            "--destination",
            str(destination),
        ],
        cwd=site_root,
        env=env,
        check=True,
    )

    verify(
        repo=source_root,
        site=destination,
        build_scope=staged_scope,
        source_repository=source_repository,
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--build-scope", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--source-repository")
    args = parser.parse_args(argv)

    build(
        source_root=args.source_root,
        build_scope=args.build_scope,
        destination=args.destination,
        base_url=args.base_url,
        source_ref=args.source_ref,
        source_repository=args.source_repository,
    )
    print(f"Built verified Pages scope: {args.destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
