"""Native validation for standalone and assembled HUB75 models."""
from pathlib import Path

from .common import (
    close,
    commands,
    count,
    document,
    measurements,
    require,
    size_close,
    body_size,
)

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


