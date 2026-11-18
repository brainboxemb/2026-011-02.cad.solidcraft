"""Generic helpers for model-owned CAD checks."""
from __future__ import annotations

import json
from pathlib import Path
import zipfile

TOL = 1e-3


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def document(path: Path):
    with zipfile.ZipFile(path) as archive:
        return json.loads(archive.read("document.json"))


def close(actual, expected, tol=TOL):
    return abs(float(actual) - float(expected)) <= tol


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def commands(root: Path, slug: str):
    return load(root / slug / "commands.json")["commands"]


def measurements(root: Path, slug: str, suffix: str = ""):
    name = "measurements.json" if not suffix else f"measurements-{suffix}.json"
    return load(root / slug / name)


def count(rows, command, predicate=None):
    selected = [row for row in rows if row["command"] == command]
    if predicate is not None:
        selected = [row for row in selected if predicate(row["params"])]
    return len(selected)


def bodies_named(data, prefix):
    return [
        body for body in data["bodies"]
        if body["name"].startswith(prefix)
    ]


def body_size(body):
    return tuple(
        float(hi) - float(lo)
        for lo, hi in zip(body["bbox"]["min"], body["bbox"]["max"])
    )


def size_close(body, expected):
    return all(
        close(actual, target)
        for actual, target in zip(body_size(body), expected)
    )


def all_bodies(rows, predicate):
    return bool(rows) and all(predicate(body) for body in rows)


def timeline_ok(data):
    return all(row.get("error") is None for row in data.get("timeline", []))
