"""Retained active Free-state profiles from HUB75 – losse Ø10 proefklem.sc.

Coordinates are native SolidCraft sketch coordinates as authored in the source;
they are not reinterpreted through the physical XZ helper used by the frame
coupler owner.
"""

FREE = {
    "tube_d": 10.0,
    "clamp_interference": 0.4,
    "clamp_bore": 9.6,
    "clamp_wall": 2.0,
    "clamp_width": 12.0,
    "dove_run": 16.0,
    "slot_stop": 1.0,
}

RING_LOOP = {
    "start": [4.8083261120685235, 4.8083261120685235],
    "segments": [
        {
            "kind": "arc",
            "end": [4.8083261120685235, -4.8083261120685235],
            "center": [0.0, 0.0],
            "clockwise": False,
        },
        {
            "kind": "arc",
            "end": [3.394112549695428, -3.394112549695428],
            "center": [4.1012193308819755, -4.1012193308819755],
            "clockwise": False,
        },
        {
            "kind": "arc",
            "end": [3.394112549695428, 3.394112549695428],
            "center": [0.0, 0.0],
            "clockwise": True,
        },
        {
            "kind": "arc",
            "end": [4.8083261120685235, 4.8083261120685235],
            "center": [4.1012193308819755, 4.1012193308819755],
            "clockwise": False,
        },
    ],
}

BACK_LOOP = {
    "start": [-8.85, -5.7],
    "segments": [
        {
            "kind": "arc",
            "end": [-8.55, -6.0],
            "center": [-8.55, -5.7],
            "clockwise": False,
        },
        {"kind": "line", "end": [-5.95, -6.0]},
        {
            "kind": "arc",
            "end": [-5.65, -5.7],
            "center": [-5.95, -5.7],
            "clockwise": False,
        },
        {"kind": "line", "end": [-5.65, 5.7]},
        {
            "kind": "arc",
            "end": [-5.95, 6.0],
            "center": [-5.95, 5.7],
            "clockwise": False,
        },
        {"kind": "line", "end": [-8.55, 6.0]},
        {
            "kind": "arc",
            "end": [-8.85, 5.7],
            "center": [-8.55, 5.7],
            "clockwise": False,
        },
        {"kind": "line", "end": [-8.85, -5.7]},
    ],
}

SLOT_LOOP = {
    "start": [-9.05, -2.75],
    "segments": [
        {
            "kind": "arc",
            "end": [-8.9, -2.9],
            "center": [-8.9, -2.75],
            "clockwise": False,
        },
        {"kind": "line", "end": [-8.412132034355963, -2.9]},
        {
            "kind": "arc",
            "end": [-8.306066017177981, -2.943933982822018],
            "center": [-8.412132034355963, -3.05],
            "clockwise": True,
        },
        {"kind": "line", "end": [-7.643933982822017, -3.606066017177982]},
        {
            "kind": "arc",
            "end": [-7.537867965644035, -3.65],
            "center": [-7.537867965644035, -3.5],
            "clockwise": False,
        },
        {"kind": "line", "end": [-7.25, -3.65]},
        {
            "kind": "arc",
            "end": [-7.1, -3.5],
            "center": [-7.25, -3.5],
            "clockwise": False,
        },
        {"kind": "line", "end": [-7.1, 3.5]},
        {
            "kind": "arc",
            "end": [-7.25, 3.65],
            "center": [-7.25, 3.5],
            "clockwise": False,
        },
        {"kind": "line", "end": [-7.537867965644035, 3.65]},
        {
            "kind": "arc",
            "end": [-7.643933982822017, 3.606066017177982],
            "center": [-7.537867965644035, 3.5],
            "clockwise": False,
        },
        {"kind": "line", "end": [-8.306066017177981, 2.943933982822018]},
        {
            "kind": "arc",
            "end": [-8.412132034355963, 2.9],
            "center": [-8.412132034355963, 3.05],
            "clockwise": True,
        },
        {"kind": "line", "end": [-8.9, 2.9]},
        {
            "kind": "arc",
            "end": [-9.05, 2.75],
            "center": [-8.9, 2.75],
            "clockwise": False,
        },
        {"kind": "line", "end": [-9.05, -2.75]},
    ],
}
