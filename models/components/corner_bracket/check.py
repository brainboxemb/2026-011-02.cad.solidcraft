"""Checks owned by the corner-bracket model."""
from model_check import commands, count, measurements, require


def check_native(root, slug):
    rows = commands(root, slug)
    require(count(rows, "solid.hole") == 0, f"{slug}: holes must stay absent")
    require(count(rows, "solid.fillet") == 1, f"{slug}: expected one fillet")
    require(count(rows, "solid.chamfer") == 3, f"{slug}: expected three chamfers")

    data = measurements(root, slug)
    require(data["body_count"] == 1, f"{slug}: expected one body")
    body = data["bodies"][0]
    require(body["name"] == "CornerBracket", f"{slug}: body name changed")
    require(body["closed"] is True, f"{slug}: body must be closed")
