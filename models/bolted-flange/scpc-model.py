"""Simple bolted flange expressed directly as SCPC commands."""

from math import cos, radians, sin

from scpc import Script


BOLTS = 6
PCD = 70.0

script = Script()

script.add(
    "solid.cylinder",
    height=10,
    diameter=100,
    base=[0, 0, 0],
    axis="Z",
    operation="new",
    body_name="Flange",
)
script.add(
    "solid.cylinder",
    height=16,
    diameter=44,
    base=[0, 0, 10],
    axis="Z",
    operation="join",
    targets=["Flange"],
)
script.add(
    "solid.hole",
    position=[0, 0, 26],
    diameter=24,
    depth=26,
    direction=[0, 0, -1],
    targets=["Flange"],
)

radius = PCD / 2
for index in range(BOLTS):
    angle = radians(index * 360 / BOLTS)
    script.add(
        "solid.hole",
        position=[
            radius * cos(angle),
            radius * sin(angle),
            10,
        ],
        diameter=9,
        depth=10,
        direction=[0, 0, -1],
        targets=["Flange"],
    )
