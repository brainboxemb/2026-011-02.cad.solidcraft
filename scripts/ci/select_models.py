"""Select CAD models for targeted CI and publication.

Model selection and tool-version selection are deliberately separate:
changing dependencies.repos or a SolidCraft workflow version does not imply a
full catalog rebuild. Use --mode all when a deliberate full regression is
wanted.
"""
from __future__ import annotations

from argparse import ArgumentParser
import json
from pathlib import Path

from model_catalog import MODELS, model_input_paths, model_slugs


PIPELINE_SMOKE_MODEL = "plate"
PIPELINE_SMOKE_PATHS = (
    ".github/workflows/cad.yml",
    "scripts/ci/build_plan.py",
    "scripts/ci/cad_ci.py",
    "scripts/ci/model_catalog.py",
    "scripts/ci/model_check.py",
    "scripts/ci/model_checks.py",
    "scripts/ci/native_ci.py",
    "scripts/ci/native_validation.py",
    "scripts/ci/output_store.py",
    "scripts/ci/pipeline_ci.py",
    "scripts/ci/publish_ci.py",
    "scripts/ci/run_native_mutations.py",
    "scripts/ci/compare-scpc.py",
)


SITE_ONLY_PATHS = (
    "scripts/ci/build-results.py",
    "scripts/ci/test-results.py",
    "scripts/ci/model_catalog.py",
    "scripts/ci/output_store.py",
    ".github/workflows/publish-cad.yml",
    ".github/workflows/cleanup-cad-preview.yml",
    "site/",
)


def _matches(path: str, watched: str) -> bool:
    raw_watched = str(watched).replace("\\", "/")
    is_prefix = raw_watched.endswith("/")
    path = Path(path).as_posix().lstrip("./")
    watched = Path(raw_watched).as_posix().lstrip("./")
    if is_prefix:
        return path == watched or path.startswith(watched + "/")
    return path == watched


def affected_models(changed_paths, *, kind="scpf"):
    """Return catalog models affected by changed repository paths."""
    eligible = set(model_slugs(kind))
    selected = []

    for slug in MODELS:
        if slug not in eligible:
            continue
        watched = model_input_paths(slug)
        if any(
            _matches(path, candidate)
            for path in changed_paths
            for candidate in watched
        ):
            selected.append(slug)

    return tuple(selected)


def validate_models(slugs, *, kind="scpf"):
    """Validate catalog slugs and keep only models supporting this build kind."""
    eligible = set(model_slugs(kind))
    unknown = [slug for slug in slugs if slug not in MODELS]
    if unknown:
        raise ValueError(f"unknown model(s): {', '.join(unknown)}")
    return tuple(
        slug for slug in dict.fromkeys(slugs)
        if slug in eligible
    )


def select_models(
    *,
    mode="changed",
    kind="scpf",
    changed_paths=(),
    models=(),
):
    if mode == "all":
        return tuple(model_slugs(kind))
    if mode == "models":
        if not models:
            raise ValueError("models mode requires at least one model slug")
        return validate_models(models, kind=kind)
    if mode == "changed":
        return affected_models(changed_paths, kind=kind)
    raise ValueError(f"unknown selection mode: {mode}")


def needs_site_refresh(changed_paths, selected=()):
    """Whether catalog/site output should be regenerated.

    A site refresh is cheap and separate from native geometry selection.
    """
    if selected:
        return True
    return any(
        _matches(path, watched)
        for path in changed_paths
        for watched in SITE_ONLY_PATHS
    )


def needs_pipeline_smoke(changed_paths):
    """Whether CI infrastructure changes need one real end-to-end model."""
    return any(
        _matches(path, watched)
        for path in changed_paths
        for watched in PIPELINE_SMOKE_PATHS
    )


def read_paths(path):
    if path is None:
        return ()
    return tuple(
        line.strip()
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    )


def parse_models(value):
    if not value:
        return ()
    return tuple(
        item.strip()
        for item in value.replace(",", " ").split()
        if item.strip()
    )


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("changed", "models", "all"),
        default="changed",
    )
    parser.add_argument(
        "--kind",
        choices=("scpf", "scpc", "native", "native-snapshot-required"),
        default="scpf",
    )
    parser.add_argument("--paths-file")
    parser.add_argument("--models", default="")
    parser.add_argument(
        "--format",
        choices=("list", "json"),
        default="list",
    )
    args = parser.parse_args()

    changed_paths = read_paths(args.paths_file)
    selected = select_models(
        mode=args.mode,
        kind=args.kind,
        changed_paths=changed_paths,
        models=parse_models(args.models),
    )

    if args.format == "json":
        print(json.dumps({
            "mode": args.mode,
            "kind": args.kind,
            "models": list(selected),
            "site_refresh": needs_site_refresh(changed_paths, selected),
        }))
    else:
        print(" ".join(selected))


if __name__ == "__main__":
    main()
