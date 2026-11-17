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

    thickness_data = measurements(
        root,
        "simple-mft-assembly",
        "worktop-thickness-24",
    )
    thick_worktop = _one_body_with_size(
        thickness_data,
        (805.0, 555.0, 24.0),
    )
    thick_rail = _one_body_with_size(
        thickness_data,
        (184.20, 1080.0, 10.50),
    )
    require(
        _bounds_close(
            thick_worktop,
            (-402.5, -277.5, 0.0),
            (402.5, 277.5, 24.0),
        ),
        "simple-mft-assembly: worktop thickness mutation changed its datum",
    )
    require(
        _bounds_close(
            thick_rail,
            (-92.1, -540.0, 24.0),
            (92.1, 540.0, 34.5),
        ),
        "simple-mft-assembly: rail did not follow worktop_thickness",
    )

    length_data = measurements(
        root,
        "simple-mft-assembly",
        "guide-rail-length-1400",
    )
    long_worktop = _one_body_with_size(
        length_data,
        (805.0, 555.0, 18.0),
    )
    long_rail = _one_body_with_size(
        length_data,
        (184.20, 1400.0, 10.50),
    )
    require(
        _bounds_close(
            long_worktop,
            (-402.5, -277.5, 0.0),
            (402.5, 277.5, 18.0),
        ),
        "simple-mft-assembly: guide rail length mutation changed worktop",
    )
    require(
        _bounds_close(
            long_rail,
            (-92.1, -700.0, 18.0),
            (92.1, 700.0, 28.5),
        ),
        "simple-mft-assembly: guide_rail_length did not resize rail symmetrically",
    )
