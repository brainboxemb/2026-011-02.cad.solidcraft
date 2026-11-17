"""Compare native SolidCraft results for two *independent* Python scripts.

Unit tests compare the independent command plans at the appropriate level:
exact lowering where representation is identical, and the same parameter /
feature contract where Forge keeps algebraically equivalent expressions.
Native SolidCraft evaluates both models here; BRep measurements and editable
feature histories are the geometry proof. No custom geometry or transforms.
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
    # If the CLI returns feature timelines, they must match in identity and
    # naming. Vent Plate has one documented SCPF 0.6.1 representation
    # difference: an explicit Sketch and its extrusion share one name, so the
    # SCPF source calls both "Vent" while the original command model calls the
    # sketch "Slot" and its cut "Vent".
    left_timeline = a.get("timeline") or []
    right_timeline = b.get("timeline") or []

    def timeline_rows(items):
        rows = []
        for item in items:
            feature_type = item.get("type")
            name = item.get("name")
            if slug == "vent-plate" and name == "Slot":
                name = "Vent"
            if slug == "bolted-flange":
                # Forge gives the first standalone Sketch extrusion the native
                # default name Extrude1, while the source command document
                # explicitly calls it Disc. Forge also shares one name between
                # the Bolt Sketch and BoltHole extrusion.
                if feature_type == "ExtrudeFeature" and name == "Disc":
                    name = "Extrude1"
                if feature_type == "Sketch" and name == "Bolt":
                    name = "BoltHole"
            rows.append((feature_type, name, item.get("error")))
        return rows

    assert timeline_rows(left_timeline) == timeline_rows(right_timeline), slug
    print(f"{slug}: SCPC/SCPF native BRep + feature history match")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: compare-scpc.py <native-root> <slug>")
    check(Path(sys.argv[1]), sys.argv[2])
