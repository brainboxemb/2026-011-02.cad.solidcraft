"""Official SolidCraft bolted-flange sample expressed as SCPC commands.

This intentionally preserves the source command history and names:
Disc -> Hub -> Bore -> Bolt/BoltHole -> CircularPattern.
"""
from scpc import Script


script = Script()

script.add(
    "parameters.change",
    name="bolts",
    expression="6",
    unit="",
    comment="number of bolt holes",
)
script.add(
    "parameters.change",
    name="pcd",
    expression="70 mm",
    comment="bolt circle diameter",
)

script.add("sketch.create", plane="XY", name="Disc")
script.add("sketch.circle.center", center=[0, 0], diameter=100)
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance=10,
    body_name="Flange",
    name="Disc",
)

script.add(
    "sketch.create",
    plane={"face": [0, 0, 10]},
    name="Hub",
)
script.add("sketch.circle.center", center=[0, 0], diameter=44)
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance=16,
    operation="join",
    name="Hub",
)

script.add("sketch.create", plane="XY", name="Bore")
script.add("sketch.circle.center", center=[0, 0], diameter=24)
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance=26,
    operation="cut",
    name="Bore",
)

script.add("sketch.create", plane="XY", name="Bolt")
script.add(
    "sketch.circle.center",
    center=[35, 0],
    diameter=9,
)
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance=10,
    operation="cut",
    name="BoltHole",
)

script.add(
    "solid.pattern.circular",
    features=["BoltHole"],
    axis="Z",
    count="bolts",
)
