"""Checks owned by the flex-bench-dog model."""
from model_check import (
    body_size,
    commands,
    count,
    measurements,
    require,
    size_close,
)


def check_native(root, slug):
    rows = commands(root, slug)
    require(count(rows, "solid.cylinder") == 4,
            f"{slug}: expected rim, working body, insert and tip flare")
    require(count(rows, "sketch.create") == 3,
            f"{slug}: expected two flex-slot sketches and one logo sketch")
    require(count(rows, "solid.extrude") == 3,
            f"{slug}: expected two slot cuts and one logo extrusion")
    require(count(rows, "solid.fillet") == 0,
            f"{slug}: expected chamfers rather than fillets")
    require(count(rows, "solid.chamfer") == 2,
            f"{slug}: expected top and bottom chamfers")
    require(count(rows, "solid.box") == 0,
            f"{slug}: should use native Sketch features, not Box CSG")

    data = measurements(root, slug)
    require(data["body_count"] == 1, f"{slug}: expected one body")
    body = data["bodies"][0]
    require(body["closed"] is True, f"{slug}: body must be closed")
    require(
        size_close(body, (24.0, 24.0, 40.0)),
        f"{slug}: unexpected bounds {body_size(body)}",
    )
