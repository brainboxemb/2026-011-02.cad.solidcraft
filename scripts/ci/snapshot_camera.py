"""Stable orthographic overview framing for native SolidCraft CAD snapshots.

Angles are in radians and target/distance are in mm. Orthographic fov=0
maps distance d to a visible vertical half-height of 0.4*d. The official
SolidCraft v0.30.1 CLI accepts this JSON with `snapshot --camera`.

Only large, reliably dimensioned models need an explicit override.
Simple examples keep SolidCraft's default ISO framing.
The planned multiple-views gallery is a different feature (CAD issue #20).
"""
import json
import sys

CAMERAS = {
    # Wooden box: ±437 mm across X, Z=-15..377, depth -25..99 plus
    # external brackets. Camera sees from slightly above, front-right.
    "hub75-wood-frame": {
        "target": [0, 28, 181],
        "yaw": -0.40,
        "pitch": 0.25,
        "distance": 1020,
        "fov": 0,
    },
    # The detailed panel array now stands in the XZ plane like the wooden box.
    "hub75-screen": {
        "target": [0, 0, 160],
        "yaw": -0.24,
        "pitch": 0.20,
        "distance": 920,
        "fov": 0,
    },
    "hub75-panel": {
        "target": [80, 0, 8],
        "yaw": -0.33,
        "pitch": 1.05,
        "distance": 565,
        "fov": 0,
    },
}


def validate_camera(camera):
    assert len(camera["target"]) == 3
    assert all(isinstance(value, (int, float)) for value in camera["target"])
    assert isinstance(camera["distance"], (int, float))
    assert camera["distance"] > 0
    assert -1.57 < camera["pitch"] < 1.57
    assert camera.get("fov", 0) == 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: snapshot_camera.py MODEL_SLUG")
    camera = CAMERAS.get(sys.argv[1])
    if camera is not None:
        validate_camera(camera)
        print(json.dumps(camera, separators=(",", ":")))
