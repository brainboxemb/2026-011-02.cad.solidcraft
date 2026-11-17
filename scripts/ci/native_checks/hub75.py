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


