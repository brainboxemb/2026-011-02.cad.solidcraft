"""Compare native SolidCraft results for two *independent* Python scripts.

Command JSON equivalence is checked in unit tests. Native SolidCraft
evaluates both models and this script compares BRep measurements and
editable feature histories. No custom geometry or transformations.
"""
import json
from math import isclose
from pathlib import Path
import sys


def check(root, slug):
    def load(language):
        path = root / slug / language / "measurements.json"
        return json.loads(path.read_text(encoding="utf-8"))

    a = load("scpf")
    b = load("scpc")
    assert a["body_count"] == b["body_count"] > 0, slug
    assert len(a["bodies"]) == len(b["bodies"]), slug
    for left, right in zip(a["bodies"], b["bodies"]):
        assert left["name"] == right["name"], slug
        for field in ("volume_mm3",):
            if field in left and field in right:
                assert isclose(left[field], right[field], rel_tol=1e-8,
                               abs_tol=1e-6), (slug, field, left, right)
        for key in ("min", "max"):
            for x, y in zip(left["bbox"][key], right["bbox"][key]):
                assert isclose(x, y, rel_tol=1e-8, abs_tol=1e-6), (slug, key, x, y)
    # If the CLI returns feature timelines, they must match in identity
    # and naming. Distinct run metadata can differ.
    left_timeline = a.get("timeline") or []
    right_timeline = b.get("timeline") or []
    assert [(x.get("type"), x.get("name"), x.get("error"))
            for x in left_timeline] == [
            (x.get("type"), x.get("name"), x.get("error"))
            for x in right_timeline], slug
    print(f"{slug}: SCPC/SCPF native BRep + feature history match")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: compare-scpc.py <native-root> <slug>")
    check(Path(sys.argv[1]), sys.argv[2])
