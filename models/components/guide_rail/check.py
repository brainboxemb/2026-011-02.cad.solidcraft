"""Checks owned by the guide-rail model family."""
from model_check import body_size, measurements, require, size_close


EXPECTED = {
    "guide-rail": (184.20, 600.0, 10.50),
    "guide-rail-makita": (182.50, 600.0, 10.28),
}


def check_native(root, slug):
    expected = EXPECTED[slug]
    data = measurements(root, slug)
    require(data["body_count"] == 1, f"{slug}: expected one body")
    require(
        size_close(data["bodies"][0], expected),
        f"{slug}: unexpected bounds {body_size(data['bodies'][0])}",
    )
