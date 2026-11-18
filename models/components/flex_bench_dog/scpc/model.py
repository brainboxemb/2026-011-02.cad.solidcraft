"""FlexBenchDog expressed directly as SolidCraft commands."""

from scpc import Script

script = Script()

for name, value in (
    ("hole_diameter", 20.0),
    ("interference", 0.20),
    ("rim_diameter", 24.0),
    ("slot_width", 1.5),
):
    script.add("parameters.add", name=name, expression=str(value), unit="mm")

script.add(
    "solid.cylinder",
    height=20,
    diameter="hole_diameter",
    base=[0, 0, 0],
    axis="Z",
    operation="new",
    body_name="FlexBenchDog",
)
script.add(
    "solid.cylinder",
    height=3,
    diameter="rim_diameter",
    base=[0, 0, 20],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)
script.add(
    "solid.cylinder",
    height=18,
    diameter="hole_diameter + interference",
    base=[0, 0, 23],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)
script.add(
    "solid.box",
    length="hole_diameter + interference + 2",
    width="slot_width",
    height=14,
    corner=[
        "-(hole_diameter + interference + 2) / 2",
        "-slot_width / 2",
        27,
    ],
    operation="cut",
    targets=["FlexBenchDog"],
)
script.add(
    "solid.box",
    length="slot_width",
    width="hole_diameter + interference + 2",
    height=14,
    corner=[
        "-slot_width / 2",
        "-(hole_diameter + interference + 2) / 2",
        27,
    ],
    operation="cut",
    targets=["FlexBenchDog"],
)
