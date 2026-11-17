"""Vent Plate from the official SolidCraft example, expressed as native commands.

This intentionally mirrors the source feature history:
Box1 -> Fillet1 -> Slot -> Vent -> RectangularPattern1.

The SCPF version is added only when Forge can emit the same native rectangular
feature pattern (brainboxemb/lib.py.solidcraft.forge#215).
"""
from scpc import Script


script = Script()

script.add("parameters.add", name="cols", expression="6", unit="")
script.add("parameters.add", name="rows", expression="3", unit="")
script.add(
    "parameters.add",
    name="pitch",
    expression="16",
    unit="mm",
    comment="slot spacing",
)

script.add(
    "solid.box",
    length=120,
    width=80,
    height=4,
    corner=[0, 0, 0],
    body_name="Plate",
)

script.add(
    "solid.fillet",
    body="Plate",
    radius=8,
    edges=[
        [0, 0, 2],
        [120, 0, 2],
        [120, 80, 2],
        [0, 80, 2],
    ],
)

script.add("sketch.create", plane="XY", name="Slot")
script.add(
    "sketch.rectangle.two_point",
    p0=[18, 12],
    p1=[24, 26],
)
script.add("sketch.finish")

script.add(
    "solid.extrude",
    distance=4,
    direction="positive",
    operation="cut",
    targets=["Plate"],
    name="Vent",
)

script.add(
    "solid.pattern.rectangular",
    features=["Vent"],
    dir1=[1, 0, 0],
    count1="cols",
    spacing1="pitch",
    dir2=[0, 1, 0],
    count2="rows",
    spacing2=22,
    name="RectangularPattern1",
)
