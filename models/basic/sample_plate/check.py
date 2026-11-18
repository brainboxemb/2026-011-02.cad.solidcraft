"""Checks owned by the sample-plate model."""
from model_check import document, require


def check_native(root, slug):
    doc = document(root / slug / "model.sc")
    features = doc["features"]
    require(
        [row["name"] for row in features if row["type"] == "sketch"]
        == ["Base", "Holes", "Bore"],
        f"{slug}: sketch history changed",
    )
    require(
        sum(row["type"] == "cylinder" for row in features) == 1,
        f"{slug}: expected one cylinder feature",
    )
    require(
        sum(row["type"] == "hole" for row in features) == 0,
        f"{slug}: unexpected native hole feature",
    )
