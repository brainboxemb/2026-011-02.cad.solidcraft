"""Native validation for the Simple MFT assembly."""
from pathlib import Path

from .common import close, measurements, require, size_close


def _one_body_with_size(data, expected):
    matches = [
        body for body in data["bodies"]
        if size_close(body, expected)
    ]
    require(
        len(matches) == 1,
        f"simple-mft-assembly: expected one body sized {expected}, "
        f"found {len(matches)}",
    )
    return matches[0]


def _bounds_close(body, minimum, maximum):
    return all(
        close(actual, expected)
        for actual, expected in zip(body["bbox"]["min"], minimum)
    ) and all(
        close(actual, expected)
        for actual, expected in zip(body["bbox"]["max"], maximum)
    )


def validate_simple_mft_assembly(root: Path):
    data = measurements(root, "simple-mft-assembly")
    require(
        data["body_count"] == 2,
        f"simple-mft-assembly: expected two bodies, found {data['body_count']}",
    )

    worktop = _one_body_with_size(data, (805.0, 555.0, 18.0))
    rail = _one_body_with_size(data, (184.20, 1080.0, 10.50))

    require(
        _bounds_close(
            worktop,
            (-402.5, -277.5, 0.0),
            (402.5, 277.5, 18.0),
        ),
        f"simple-mft-assembly: unexpected worktop bounds {worktop['bbox']}",
    )
    require(
        _bounds_close(
            rail,
            (-92.1, -540.0, 18.0),
            (92.1, 540.0, 28.5),
        ),
        f"simple-mft-assembly: unexpected guide rail bounds {rail['bbox']}",
    )
