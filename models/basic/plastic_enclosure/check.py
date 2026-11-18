"""Checks owned by the plastic-enclosure model."""
from model_check import document, require


def check_native(root, slug):
    doc = document(root / slug / "model.sc")
    require(
        [row["type"] for row in doc["features"]]
        == ["box", "shell", "lip", "snap_fit", "boss", "boss", "rest"],
        f"{slug}: feature history changed",
    )
