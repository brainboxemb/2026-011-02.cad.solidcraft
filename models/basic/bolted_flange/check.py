"""Checks owned by the bolted-flange model."""
import math

from model_check import (
    body_size,
    close,
    commands,
    count,
    measurements,
    require,
    size_close,
)


def check_native(root, slug):
    rows = commands(root, slug)
    require(count(rows, "solid.cylinder") == 2,
            f"{slug}: expected flange and hub cylinders")
    require(count(rows, "sketch.create") == 1,
            f"{slug}: expected one seed bolt-hole sketch")
    require(count(rows, "sketch.circle.center") == 1,
            f"{slug}: expected one seed bolt-hole circle")
    require(count(rows, "solid.extrude") == 1,
            f"{slug}: expected one seed through-cut")
    require(count(rows, "solid.pattern.circular") == 1,
            f"{slug}: expected one native circular bolt pattern")
    require(count(rows, "solid.hole") == 1,
            f"{slug}: only the central bore should use solid.hole")

    data = measurements(root, slug)
    require(data["body_count"] == 1, f"{slug}: expected one joined/cut body")
    body = data["bodies"][0]
    require(body["name"] == "Flange", f"{slug}: body name changed")
    require(body["closed"] is True, f"{slug}: body must be closed")
    require(
        size_close(body, (100.0, 100.0, 26.0)),
        f"{slug}: unexpected bounds {body_size(body)}",
    )

    expected_volume = (
        math.pi * 50.0**2 * 10.0
        + math.pi * 22.0**2 * 16.0
        - math.pi * 12.0**2 * 26.0
        - 6.0 * math.pi * 4.5**2 * 10.0
    )
    require(
        close(body["volume_mm3"], expected_volume, 1e-3),
        f"{slug}: native volume changed",
    )
