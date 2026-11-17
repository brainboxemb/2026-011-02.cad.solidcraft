"""Native validation for MFT worktop assemblies."""
from pathlib import Path

from .common import body_size, close, measurements, require


def _body_with_size(data, expected):
    matches = [
        body for body in data["bodies"]
        if all(
            close(actual, target)
            for actual, target in zip(body_size(body), expected)
        )
    ]
    require(
        len(matches) == 1,
        f"expected one body sized {expected}, found {len(matches)}",
    )
    return matches[0]


def validate_simple_mft_assembly(root: Path):
    data = measurements(root, "simple-mft-assembly")
    require(
        data["body_count"] == 2,
        f"simple-mft-assembly: expected two bodies, found {data['body_count']}",
    )

    worktop = _body_with_size(data, (805.0, 555.0, 18.0))
    rail = _body_with_size(data, (184.20, 1080.0, 10.50))

    require(
        all(
            close(actual, expected)
            for actual, expected in zip(
                worktop["bbox"]["min"],
                (-402.5, -277.5, 0.0),
            )
        )
        and all(
            close(actual, expected)
            for actual, expected in zip(
                worktop["bbox"]["max"],
                (402.5, 277.5, 18.0),
            )
        ),
        f"simple-mft-assembly: unexpected worktop bounds {worktop['bbox']}",
    )

    require(
        all(
            close(actual, expected)
            for actual, expected in zip(
                rail["bbox"]["min"],
                (-92.1, -540.0, 18.0),
            )
        )
        and all(
            close(actual, expected)
            for actual, expected in zip(
                rail["bbox"]["max"],
                (92.1, 540.0, 28.5),
            )
        ),
        f"simple-mft-assembly: unexpected guide rail bounds {rail['bbox']}",
    )
