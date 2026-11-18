"""Checks owned by the plastic-enclosure-pi model."""
from model_check import commands, count, measurements, require


def check_native(root, slug):
    rows = commands(root, slug)
    require(
        [
            row["params"]["name"]
            for row in rows
            if row["command"] == "sketch.create"
        ]
        == ["Pi ports", "USB and Ethernet", "Floor vents", "Pi 4 engraving"],
        f"{slug}: sketch history changed",
    )
    require(count(rows, "plastic.boss") == 4,
            f"{slug}: expected four bosses")

    data = measurements(root, slug)
    require(data["body_count"] == 1, f"{slug}: expected one body")
    body = data["bodies"][0]
    require(body["name"] == "PlasticEnclosurePi", f"{slug}: body name changed")
    require(body["closed"] is True, f"{slug}: body must be closed")
    require(body["material"] == "PETG", f"{slug}: PETG material missing")
    require(len(data["sketches"]) == 4, f"{slug}: expected four sketches")
