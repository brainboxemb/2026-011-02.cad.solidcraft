#!/usr/bin/env python3
"""Validate native SolidCraft evidence for project CAD models.

This mirrors Forge qualification/native_validation.py: the workflow builds
native evidence, while this file owns model-specific semantic checks.
"""
from __future__ import annotations

import argparse
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


def validate_hub75_panel(root: Path):
    rows = commands(root, "hub75-panel")
    require(count(rows, "component.create") == 0, "hub75-panel: unexpected component.create")
    require(count(rows, "occurrence.copy") == 0, "hub75-panel: unexpected occurrence.copy")
    require(count(rows, "occurrence.move") == 0, "hub75-panel: unexpected occurrence.move")
    require(count(rows, "solid.loft") == 1, "hub75-panel: expected one loft")
    require(
        count(
            rows,
            "sketch.create",
            lambda p: p.get("name") == "Rear electronics bays",
        ) == 1,
        "hub75-panel: expected one Rear electronics bays sketch",
    )
    require(
        count(rows, "sketch.rectangle.two_point") == 7,
        "hub75-panel: expected seven rectangles",
    )
    require(count(rows, "solid.hole") == 6, "hub75-panel: expected six holes")
    require(
        count(
            rows,
            "solid.extrude",
            lambda p: (
                p.get("operation") == "cut"
                and p.get("name") == "Rear electronics bays"
                and p.get("direction") == "negative"
            ),
        ) == 1,
        "hub75-panel: expected one rear-bay cut",
    )

    data = measurements(root, "hub75-panel")
    require(data["body_count"] == 1, "hub75-panel: expected one body")
    require(
        size_close(data["bodies"][0], (159.70, 319.71, 14.50)),
        f"hub75-panel: unexpected bounds {body_size(data['bodies'][0])}",
    )


def validate_guide_rail(root: Path):
    data = measurements(root, "guide-rail")
    require(data["body_count"] == 1, "guide-rail: expected one body")
    require(
        size_close(data["bodies"][0], (184.20, 1400.0, 10.50)),
        f"guide-rail: unexpected bounds {body_size(data['bodies'][0])}",
    )


def validate_hub75_screen(root: Path):
    rows = commands(root, "hub75-screen")
    require(count(rows, "component.create") == 1, "hub75-screen: expected one component.create")
    require(count(rows, "occurrence.copy") == 4, "hub75-screen: expected four copies")
    require(count(rows, "occurrence.move") == 5, "hub75-screen: expected five moves")
    require(count(rows, "solid.loft") == 1, "hub75-screen: expected one loft")
    require(
        count(
            rows,
            "sketch.create",
            lambda p: p.get("name") == "Rear electronics bays",
        ) == 1,
        "hub75-screen: expected one rear electronics sketch",
    )

    doc = document(root / "hub75-screen" / "model.sc")
    require(len(doc["components"]) == 1, "hub75-screen: expected one component definition")
    require(len(doc["occurrences"]) == 5, "hub75-screen: expected five occurrences")
    require(
        [row["transform"][3][0] for row in doc["occurrences"]]
        == [0, -320, -160, 160, 320],
        "hub75-screen: unexpected X occurrence positions",
    )
    require(
        all(close(row["transform"][3][2], 160, 1e-6) for row in doc["occurrences"]),
        "hub75-screen: occurrence Z positions must be 160",
    )
    require(close(doc["occurrences"][0]["transform"][1][2], 1, 1e-6),
            "hub75-screen: first occurrence orientation changed")
    require(close(doc["occurrences"][2]["transform"][1][2], -1, 1e-6),
            "hub75-screen: central occurrence Y/Z orientation changed")
    require(close(doc["occurrences"][2]["transform"][0][0], -1, 1e-6),
            "hub75-screen: central occurrence X orientation changed")
    require(close(doc["occurrences"][2]["transform"][2][1], -1, 1e-6),
            "hub75-screen: central occurrence Z/Y orientation changed")

    data = measurements(root, "hub75-screen")
    require(data["body_count"] == 5, "hub75-screen: expected five bodies")
    require(
        all(
            close(body_size(body)[2], 319.71)
            and close(body_size(body)[1], 14.50)
            for body in data["bodies"]
        ),
        "hub75-screen: panel height/depth changed",
    )
    require(
        close(min(body["bbox"]["min"][0] for body in data["bodies"]), -399.85)
        and close(max(body["bbox"]["max"][0] for body in data["bodies"]), 399.85),
        "hub75-screen: overall X bounds changed",
    )


def validate_corner_bracket(root: Path):
    rows = commands(root, "corner-bracket")
    require(count(rows, "solid.hole") == 0, "corner-bracket: holes must stay absent")
    require(count(rows, "solid.fillet") == 1, "corner-bracket: expected one fillet")
    require(count(rows, "solid.chamfer") == 3, "corner-bracket: expected three chamfers")

    data = measurements(root, "corner-bracket")
    require(data["body_count"] == 1, "corner-bracket: expected one body")
    body = data["bodies"][0]
    require(body["name"] == "CornerBracket", "corner-bracket: body name changed")
    require(body["closed"] is True, "corner-bracket: body must be closed")


def validate_sample_plate(root: Path):
    doc = document(root / "sample-plate" / "model.sc")
    features = doc["features"]
    require(
        [row["name"] for row in features if row["type"] == "sketch"]
        == ["Base", "Holes", "Bore"],
        "sample-plate: sketch history changed",
    )
    require(sum(row["type"] == "cylinder" for row in features) == 1,
            "sample-plate: expected one cylinder feature")
    require(sum(row["type"] == "hole" for row in features) == 0,
            "sample-plate: unexpected native hole feature")


def validate_plastic_enclosure(root: Path):
    doc = document(root / "plastic-enclosure" / "model.sc")
    require(
        [row["type"] for row in doc["features"]]
        == ["box", "shell", "lip", "snap_fit", "boss", "boss", "rest"],
        "plastic-enclosure: feature history changed",
    )


def validate_plastic_enclosure_pi(root: Path):
    rows = commands(root, "plastic-enclosure-pi")
    require(
        [
            row["params"]["name"]
            for row in rows
            if row["command"] == "sketch.create"
        ]
        == ["Pi ports", "USB and Ethernet", "Floor vents", "Pi 4 engraving"],
        "plastic-enclosure-pi: sketch history changed",
    )
    require(count(rows, "plastic.boss") == 4,
            "plastic-enclosure-pi: expected four bosses")

    data = measurements(root, "plastic-enclosure-pi")
    require(data["body_count"] == 1, "plastic-enclosure-pi: expected one body")
    body = data["bodies"][0]
    require(body["name"] == "PlasticEnclosurePi",
            "plastic-enclosure-pi: body name changed")
    require(body["closed"] is True, "plastic-enclosure-pi: body must be closed")
    require(body["material"] == "PETG", "plastic-enclosure-pi: PETG material missing")
    require(len(data["sketches"]) == 4, "plastic-enclosure-pi: expected four sketches")


def validate_wood_frame_commands(root: Path):
    rows = commands(root, "hub75-wood-frame")

    require(count(rows, "solid.hole") == 0,
            "hub75-wood-frame: CornerBracket holes must stay absent")
    require(
        count(
            rows,
            "component.create",
            lambda p: p.get("name") == "CornerBracket",
        ) == 1,
        "hub75-wood-frame: expected one CornerBracket definition",
    )
    require(
        count(
            rows,
            "occurrence.copy",
            lambda p: p.get("component") == "CornerBracket",
        ) == 7,
        "hub75-wood-frame: expected seven CornerBracket copies",
    )
    require(
        count(
            rows,
            "occurrence.move",
            lambda p: str(p.get("occurrence", "")).startswith("$cornerbracket"),
        ) == 8,
        "hub75-wood-frame: expected eight CornerBracket placements",
    )
    require(
        count(
            rows,
            "joint.create",
            lambda p: str(p.get("name", "")).startswith("Attach CornerBracket:"),
        ) == 0,
        "hub75-wood-frame: CornerBracket placement must not create joints",
    )
    require(
        count(
            rows,
            "joint.origin",
            lambda p: str(p.get("name", "")).startswith("CornerBracket:"),
        ) == 0,
        "hub75-wood-frame: CornerBracket placement must not create origins",
    )
    require(count(rows, "solid.fillet") == 3,
            "hub75-wood-frame: expected three fillet operations")

    require(
        count(
            rows,
            "component.create",
            lambda p: p.get("name") == "HUB75Panels" and p.get("activate") is False,
        ) == 1,
        "hub75-wood-frame: HUB75Panels group changed",
    )
    require(
        count(
            rows,
            "component.create",
            lambda p: (
                p.get("name") == "Hub75PanelBasic"
                and p.get("parent") == "HUB75Panels"
            ),
        ) == 1,
        "hub75-wood-frame: Hub75PanelBasic definition changed",
    )
    require(
        count(
            rows,
            "occurrence.copy",
            lambda p: p.get("component") == "Hub75PanelBasic",
        ) == 4,
        "hub75-wood-frame: expected four panel copies",
    )
    panel_moves = [
        row["params"] for row in rows
        if row["command"] == "occurrence.move"
        and str(row["params"].get("occurrence", "")).startswith("$hub75panelbasic")
    ]
    require(len(panel_moves) == 5,
            "hub75-wood-frame: expected five panel placements")
    require(
        all(
            "panel_recess_depth" in str(p["translate"][1])
            and "opening_height" in str(p["translate"][2])
            for p in panel_moves
        ),
        "hub75-wood-frame: panel placement lost symbolic dependencies",
    )
    require(
        count(
            rows,
            "joint.create",
            lambda p: str(p.get("name", "")).startswith("Place Hub75PanelBasic"),
        ) == 0,
        "hub75-wood-frame: panel placement must not create joints",
    )

    require(
        count(
            rows,
            "occurrence.copy",
            lambda p: str(p.get("component", "")).startswith("GlassStrip"),
        ) == 2,
        "hub75-wood-frame: expected two GlassStrip copies",
    )
    board_moves = [
        row["params"] for row in rows
        if row["command"] == "occurrence.move"
        and row["params"].get("occurrence") in {"$left", "$right", "$roof", "$rear"}
    ]
    require(len(board_moves) == 4,
            "hub75-wood-frame: expected four board placements")
    require(
        count(
            rows,
            "joint.create",
            lambda p: str(p.get("name", "")).startswith("Place Board"),
        ) == 0,
        "hub75-wood-frame: board placement must not create joints",
    )
    require(
        count(
            rows,
            "joint.create",
            lambda p: str(p.get("name", "")).startswith("Place GlassStrip"),
        ) == 0,
        "hub75-wood-frame: GlassStrip placement must not create joints",
    )
    glass_moves = [
        row["params"] for row in rows
        if row["command"] == "occurrence.move"
        and str(row["params"].get("occurrence", "")).startswith("$glassstrip")
    ]
    require(len(glass_moves) == 4,
            "hub75-wood-frame: expected four GlassStrip placements")
    require(
        all("matrix" not in p and "to" not in p for p in [
            row["params"] for row in rows if row["command"] == "occurrence.move"
        ]),
        "hub75-wood-frame: occurrence.move must not use matrix/to",
    )
    require(
        count(
            rows,
            "component.create",
            lambda p: str(p.get("name", "")).startswith("GlassStrip"),
        ) == 2,
        "hub75-wood-frame: expected two GlassStrip definitions",
    )
    require(
        all(p.get("translate") != [0, 0, 0] for p in glass_moves),
        "hub75-wood-frame: GlassStrip placement must be explicit",
    )
    require(
        count(
            rows,
            "material.create",
            lambda p: (
                p.get("name") == "PINE glazing vertical"
                and p.get("color") == "#A9793E"
            ),
        ) == 1,
        "hub75-wood-frame: vertical glazing material changed",
    )
    require(
        count(
            rows,
            "material.create",
            lambda p: (
                p.get("name") == "PINE glazing horizontal"
                and p.get("color") == "#E3BF80"
            ),
        ) == 1,
        "hub75-wood-frame: horizontal glazing material changed",
    )

    require(
        any(
            row["command"] == "solid.extrude"
            and close(row["params"].get("distance"), 14.50)
            for row in rows
            if isinstance(row["params"].get("distance"), (int, float))
        ),
        "hub75-wood-frame: basic panel 14.50 mm extrusion missing",
    )
    require(
        any(
            row["command"] == "sketch.create"
            and row["params"].get("plane") == "XZ"
            for row in rows
        ),
        "hub75-wood-frame: Hub75PanelBasic XZ sketch missing",
    )


def validate_wood_frame_baseline(root: Path):
    data = measurements(root, "hub75-wood-frame")
    require(data["body_count"] == 23, "hub75-wood-frame: expected 23 bodies")

    glass = bodies_named(data, "GlassStrip")
    require(
        all_bodies(
            glass,
            lambda b: close(b["bbox"]["min"][1], 0)
            and close(b["bbox"]["max"][1], 12),
        ),
        "hub75-wood-frame: glazing baseline Y bounds changed",
    )
    roof = bodies_named(data, "Board_3")
    require(
        all_bodies(
            roof,
            lambda b: (
                close(b["bbox"]["min"][1], -10)
                and close(b["bbox"]["max"][1], 110)
                and close(b["bbox"]["min"][2], 374)
                and close(b["bbox"]["max"][2], 386)
            ),
        ),
        "hub75-wood-frame: roof baseline bounds changed",
    )
    rear = bodies_named(data, "Board_4")
    require(
        all_bodies(
            rear,
            lambda b: close(b["bbox"]["min"][1], 100)
            and close(b["bbox"]["max"][1], 109),
        ),
        "hub75-wood-frame: rear board baseline bounds changed",
    )
    window = bodies_named(data, "Window")
    require(
        all_bodies(
            window,
            lambda b: (
                close(b["bbox"]["min"][1], 12)
                and close(b["bbox"]["max"][1], 16)
                and close(b["bbox"]["min"][2], 13)
                and close(b["bbox"]["max"][2], 373)
            ),
        ),
        "hub75-wood-frame: window baseline bounds changed",
    )
    panels = bodies_named(data, "Hub75PanelBasic")
    require(
        all_bodies(
            panels,
            lambda b: (
                close(b["bbox"]["min"][1], 25)
                and close(b["bbox"]["max"][1], 39.5)
                and close(b["bbox"]["min"][2], 33.145)
                and close(b["bbox"]["max"][2], 352.855)
            ),
        ),
        "hub75-wood-frame: panel baseline bounds changed",
    )

    brackets = bodies_named(data, "CornerBracket")
    require(len(brackets) == 8,
            "hub75-wood-frame: expected eight CornerBracket bodies")
    rear_brackets = [b for b in brackets if b["bbox"]["min"][1] > 50]
    require(len(rear_brackets) == 4,
            "hub75-wood-frame: expected four rear brackets")
    require(
        all(
            close(b["bbox"]["min"][1], 76)
            and close(b["bbox"]["max"][1], 100)
            for b in rear_brackets
        ),
        "hub75-wood-frame: rear brackets must end at sidewall rear face",
    )


def validate_wood_frame_height(root: Path):
    data = measurements(root, "hub75-wood-frame", "height-400")
    roof = bodies_named(data, "Board_3")
    require(all_bodies(roof, lambda b: close(b["bbox"]["min"][2], 412)
                       and close(b["bbox"]["max"][2], 424)),
            "height mutation: roof did not follow opening_height")

    rear = bodies_named(data, "Board_4")
    require(all_bodies(rear, lambda b: close(b["bbox"]["min"][2], 0)
                       and close(b["bbox"]["max"][2], 412)),
            "height mutation: rear board did not follow opening_height")

    glass = bodies_named(data, "GlassStrip")
    tall = [
        b for b in glass
        if close(body_size(b)[2], 400)
    ]
    require(len(tall) == 2,
            "height mutation: expected two 400 mm vertical retainers")
    require(sum(close(b["bbox"]["min"][2], 12)
                and close(b["bbox"]["max"][2], 24) for b in glass) == 1,
            "height mutation: bottom horizontal retainer changed")
    require(sum(close(b["bbox"]["min"][2], 400)
                and close(b["bbox"]["max"][2], 412) for b in glass) == 1,
            "height mutation: top horizontal retainer did not move")

    window = bodies_named(data, "Window")
    require(all_bodies(window, lambda b: close(b["bbox"]["min"][2], 32)
                       and close(b["bbox"]["max"][2], 392)),
            "height mutation: window did not stay centred")

    panels = bodies_named(data, "Hub75PanelBasic")
    require(all_bodies(panels, lambda b: close(b["bbox"]["min"][2], 52.145)
                       and close(b["bbox"]["max"][2], 371.855)),
            "height mutation: panels did not stay centred")

    brackets = bodies_named(data, "CornerBracket")
    require(
        sum(close(b["bbox"]["min"][2], 364)
            and close(b["bbox"]["max"][2], 436) for b in brackets) == 4,
        "height mutation: top brackets changed",
    )
    require(
        sum(close(b["bbox"]["min"][2], -12)
            and close(b["bbox"]["max"][2], 60) for b in brackets) == 4,
        "height mutation: bottom brackets changed",
    )


def validate_wood_frame_width(root: Path):
    data = measurements(root, "hub75-wood-frame", "width-1000")
    left = [b for b in data["bodies"] if b["name"] == "Board"]
    right = [
        b for b in data["bodies"]
        if "WoodBoxFrame:1/Board:2" in b["name"]
    ]
    require(all_bodies(left, lambda b: close(b["bbox"]["min"][0], -512)
                       and close(b["bbox"]["max"][0], -500)),
            "width mutation: left side board changed")
    require(all_bodies(right, lambda b: close(b["bbox"]["min"][0], 500)
                       and close(b["bbox"]["max"][0], 512)),
            "width mutation: right side board changed")

    for prefix in ("Board_2", "Board_3", "Board_4"):
        rows = bodies_named(data, prefix)
        require(all_bodies(rows, lambda b: close(b["bbox"]["min"][0], -512)
                           and close(b["bbox"]["max"][0], 512)),
                f"width mutation: {prefix} did not span outside width")

    window = bodies_named(data, "Window")
    require(all_bodies(window, lambda b: close(b["bbox"]["min"][0], -420)
                       and close(b["bbox"]["max"][0], 420)),
            "width mutation: window changed width/centering")

    panels = bodies_named(data, "Hub75PanelBasic")
    require(close(min(b["bbox"]["min"][0] for b in panels), -399.85)
            and close(max(b["bbox"]["max"][0] for b in panels), 399.85),
            "width mutation: panel set moved")

    glass = bodies_named(data, "GlassStrip")
    require(sum(close(body_size(b)[0], 1000) for b in glass) == 2,
            "width mutation: horizontal retainers did not span 1000 mm")

    brackets = bodies_named(data, "CornerBracket")
    require(
        sum(b["bbox"]["max"][0] < 0 and close(b["bbox"]["min"][0], -524)
            for b in brackets) == 4,
        "width mutation: left brackets changed",
    )
    require(
        sum(b["bbox"]["min"][0] > 0 and close(b["bbox"]["max"][0], 524)
            for b in brackets) == 4,
        "width mutation: right brackets changed",
    )


def validate_wood_frame_other_mutations(root: Path):
    data = measurements(root, "hub75-wood-frame", "panel-recess-35")
    require(timeline_ok(data), "panel recess mutation: native timeline error")
    panels = bodies_named(data, "Hub75PanelBasic")
    require(all_bodies(panels, lambda b: close(b["bbox"]["min"][1], 35)
                       and close(b["bbox"]["max"][1], 49.5)),
            "panel recess mutation: panels did not move to 35 mm")

    data = measurements(root, "hub75-wood-frame", "glazing-depth-16")
    require(timeline_ok(data), "glazing depth mutation: native timeline error")
    glass = bodies_named(data, "GlassStrip")
    require(all_bodies(glass, lambda b: close(b["bbox"]["min"][1], 0)
                       and close(b["bbox"]["max"][1], 16)),
            "glazing depth mutation: retainers did not deepen")
    window = bodies_named(data, "Window")
    require(all_bodies(window, lambda b: close(b["bbox"]["min"][1], 16)
                       and close(b["bbox"]["max"][1], 20)),
            "glazing depth mutation: window did not follow retainers")

    data = measurements(root, "hub75-wood-frame", "bracket-params")
    require(timeline_ok(data), "bracket parameter mutation: native timeline error")
    brackets = bodies_named(data, "CornerBracket")
    require(
        sum(close(b["bbox"]["min"][1], 0) and close(b["bbox"]["max"][1], 30)
            for b in brackets) == 4,
        "bracket parameter mutation: front brackets did not become 30 mm",
    )
    require(
        sum(close(b["bbox"]["min"][1], 70) and close(b["bbox"]["max"][1], 100)
            for b in brackets) == 4,
        "bracket parameter mutation: rear brackets did not become 30 mm",
    )

    data = measurements(root, "hub75-wood-frame", "depth-120")
    front_names = lambda b: (
        b["name"] == "Board"
        or "WoodBoxFrame:1/Board:2" in b["name"]
        or b["name"].startswith("Board_2")
    )
    fronts = [b for b in data["bodies"] if front_names(b)]
    require(all_bodies(fronts, lambda b: close(b["bbox"]["min"][1], 0)
                       and close(b["bbox"]["max"][1], 120)),
            "depth mutation: side/bottom boards did not grow to 120")
    rear = bodies_named(data, "Board_4")
    require(all_bodies(rear, lambda b: close(b["bbox"]["min"][1], 120)
                       and close(b["bbox"]["max"][1], 129)),
            "depth mutation: rear board did not move")
    roof = bodies_named(data, "Board_3")
    require(all_bodies(roof, lambda b: close(b["bbox"]["min"][1], -10)
                       and close(b["bbox"]["max"][1], 130)),
            "depth mutation: roof did not preserve overhangs")
    brackets = bodies_named(data, "CornerBracket")
    rear_brackets = [b for b in brackets if b["bbox"]["min"][1] > 50]
    require(len(rear_brackets) == 4
            and all(close(b["bbox"]["min"][1], 96)
                    and close(b["bbox"]["max"][1], 120)
                    for b in rear_brackets),
            "depth mutation: rear brackets did not follow sidewall rear face")


def validate_hub75_wood_frame(root: Path):
    validate_wood_frame_commands(root)
    validate_wood_frame_baseline(root)
    validate_wood_frame_height(root)
    validate_wood_frame_width(root)
    validate_wood_frame_other_mutations(root)


VALIDATORS = {
    "hub75-panel": validate_hub75_panel,
    "guide-rail": validate_guide_rail,
    "hub75-screen": validate_hub75_screen,
    "corner-bracket": validate_corner_bracket,
    "sample-plate": validate_sample_plate,
    "plastic-enclosure": validate_plastic_enclosure,
    "plastic-enclosure-pi": validate_plastic_enclosure_pi,
    "hub75-wood-frame": validate_hub75_wood_frame,
}


def validate(root: Path):
    for slug, validator in VALIDATORS.items():
        validator(root)
        print(f"{slug}: native validation PASS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("native_root", type=Path)
    args = parser.parse_args()
    validate(args.native_root)


if __name__ == "__main__":
    main()
