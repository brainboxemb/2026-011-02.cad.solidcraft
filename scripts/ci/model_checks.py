"""Discover and run checks owned by each CAD model directory."""
from __future__ import annotations

import importlib.util
from pathlib import Path

from model_catalog import MODELS

ROOT = Path(__file__).resolve().parents[2]


def model_root(slug):
    source = Path(MODELS[slug]["source"])
    parts = source.parts
    try:
        index = parts.index("scpf")
    except ValueError as exc:
        raise ValueError(f"{slug}: source path has no scpf directory") from exc
    return ROOT.joinpath(*parts[:index])


def check_path(slug):
    return model_root(slug) / "check.py"


def load_check(slug):
    path = check_path(slug)
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(
        f"cad_model_check_{slug.replace('-', '_')}",
        path,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"{slug}: cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def command_check(slug, command_file):
    module = load_check(slug)
    if module is not None and hasattr(module, "check_commands"):
        module.check_commands(Path(command_file), slug)


def native_check(slug, native_root):
    module = load_check(slug)
    if module is not None and hasattr(module, "check_native"):
        module.check_native(Path(native_root), slug)


def mutations(slug):
    module = load_check(slug)
    if module is None:
        return ()
    value = getattr(module, "MUTATIONS", ())
    if isinstance(value, dict):
        return tuple(value.get(slug, ()))
    return tuple(value)


def snapshot_camera(slug):
    module = load_check(slug)
    if module is None:
        return None
    value = getattr(module, "SNAPSHOT_CAMERA", None)
    if isinstance(value, dict) and slug in value and isinstance(value[slug], dict):
        return value[slug]
    if isinstance(value, dict) and "target" in value:
        return value
    return None


def extra_snapshots(slug):
    module = load_check(slug)
    if module is None:
        return ()
    value = getattr(module, "EXTRA_SNAPSHOTS", ())
    if isinstance(value, dict):
        return tuple(value.get(slug, ()))
    return tuple(value)
