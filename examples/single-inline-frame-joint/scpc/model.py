"""One native SolidCraft joint with an inline child frame.

This is deliberately written with SCPC so the joint.create command can be
tested directly, without Forge first materializing a named joint.origin.
"""
from scpc import Script


script = Script()

script.add("component.create", name="Base", grounded=True)
script.add(
    "solid.box",
    length=80,
    width=40,
    height=80,
    center=[0, 0, 0],
    operation="new",
    body_name="Base",
)
script.add("component.activate", component="root")

script.add("component.create", name="Child", grounded=False)
script.add(
    "solid.box",
    length=30,
    width=20,
    height=20,
    center=[0, 0, 0],
    operation="new",
    body_name="Child",
)
script.add("component.activate", component="root")

# Seed the child at the same corner used by the diagnostic SCPF examples.
script.add(
    "occurrence.move",
    occurrence="Child:1",
    translate=[40, -20, 80],
)

# Parent: the same persistent edge/on/corner reference as
# Anchor.FRONT_TOP_RIGHT.
#
# Child: the same frame as AnchorFrame(origin=(0,0,0), z=(0,1,0), x=(1,0,0)),
# but supplied directly to joint.create at its current world position.
# There is intentionally NO joint.origin command in this script.
script.add(
    "joint.create",
    type="rigid",
    name="Inline custom frame",
    a={
        "occurrence": "Base:1",
        "edge": [40, -20, 40],
        "on": [0, -20, 40],
        "corner": [40, -20, 80],
    },
    b={
        "occurrence": "Child:1",
        "point": [40, -20, 80],
        "z": [0, 1, 0],
        "x": [1, 0, 0],
    },
)
