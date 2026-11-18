"""Native snapshot settings owned by the detailed HUB75 panel model."""

SNAPSHOT_CAMERA = {
    "target": [0, 0, 7.25],
    "yaw": -0.40,
    "pitch": 0.65,
    "distance": 460,
    "fov": 0,
}

EXTRA_SNAPSHOTS = (
    {
        "name": "front.png",
        "camera": {
            "target": [0, 0, 7.25],
            "yaw": 0,
            "pitch": -1.55,
            "distance": 460,
            "fov": 0,
        },
    },
    {
        "name": "rear.png",
        "camera": {
            "target": [0, 0, 7.25],
            "yaw": 0,
            "pitch": 1.55,
            "distance": 460,
            "fov": 0,
        },
    },
)
