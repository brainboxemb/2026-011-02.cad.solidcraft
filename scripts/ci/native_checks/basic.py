"""Native validation for small standalone/component CAD models."""
from pathlib import Path

from .common import (
    commands,
    count,
    document,
    measurements,
    require,
    size_close,
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


