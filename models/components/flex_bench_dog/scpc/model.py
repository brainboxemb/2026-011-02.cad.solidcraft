"""FlexBenchDog expressed directly as SolidCraft commands."""

from scpc import Script

script = Script()

for name, value in (
    ("hole_diameter", 20.0),
    ("interference", 0.20),
    ("working_height", 35.0),
    ("rim_diameter", 24.0),
    ("rim_thickness", 3.0),
    ("insertion_length", 38.0),
    ("slot_width", 1.5),
    ("slot_length", 30.0),
):
    script.add("parameters.add", name=name, expression=str(value), unit="mm")

script.add(
    "solid.cylinder",
    height="working_height",
    diameter="hole_diameter",
    base=[0, 0, 0],
    axis="Z",
    operation="new",
    body_name="FlexBenchDog",
)
script.add(
    "solid.cylinder",
    height="rim_thickness",
    diameter="rim_diameter",
    base=[0, 0, "working_height"],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)
script.add(
    "solid.cylinder",
    height="insertion_length",
    diameter="hole_diameter + interference",
    base=[0, 0, "working_height + rim_thickness"],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)
script.add(
    "solid.box",
    length="hole_diameter + interference + 2",
    width="slot_width",
    height="slot_length",
    corner=[
        "-(hole_diameter + interference + 2) / 2",
        "-slot_width / 2",
        "working_height + rim_thickness + insertion_length - slot_length",
    ],
    operation="cut",
    targets=["FlexBenchDog"],
)
script.add(
    "solid.box",
    length="slot_width",
    width="hole_diameter + interference + 2",
    height="slot_length",
    corner=[
        "-slot_width / 2",
        "-(hole_diameter + interference + 2) / 2",
        "working_height + rim_thickness + insertion_length - slot_length",
    ],
    operation="cut",
    targets=["FlexBenchDog"],
)
