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


