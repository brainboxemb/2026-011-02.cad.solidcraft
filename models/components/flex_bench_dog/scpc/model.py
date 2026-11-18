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

# Rim at the worktop datum.
script.add(
    "solid.cylinder",
    height=3,
    diameter="rim_diameter",
    base=[0, 0, 0],
    axis="Z",
    operation="new",
    body_name="FlexBenchDog",
)

# Working section: top of rim to 20 mm above the worktop.
script.add(
    "solid.cylinder",
    height=17,
    diameter="hole_diameter",
    base=[0, 0, 3],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)
script.add(
    "solid.fillet",
    body="FlexBenchDog",
    radius=1.0,
    edges=[[10, 0, 3]],
)
script.add(
    "solid.chamfer",
    body="FlexBenchDog",
    distance=0.6,
    edges=[[10, 0, 20]],
)

# Straight insert and a slightly oversized free tip.
script.add(
    "solid.cylinder",
    height=18,
    diameter="hole_diameter",
    base=[0, 0, -18],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)
script.add(
    "solid.cylinder",
    height=2,
    diameter="hole_diameter + interference",
    base=[0, 0, -18],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)

# Crossing slots split the lower 14 mm into four flexible legs.
script.add(
    "solid.box",
    length="hole_diameter + interference + 2",
    width="slot_width",
    height=14,
    corner=[
        "-(hole_diameter + interference + 2) / 2",
        "-slot_width / 2",
        -18,
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
        -18,
    ],
    operation="cut",
    targets=["FlexBenchDog"],
)

# Raised box-outline logo.
script.add(
    "solid.box",
    length=8,
    width=8,
    height=0.6,
    corner=[-4, -4, 20],
    operation="join",
    targets=["FlexBenchDog"],
)
script.add(
    "solid.box",
    length=5,
    width=5,
    height=0.6,
    corner=[-2.5, -2.5, 20],
    operation="cut",
    targets=["FlexBenchDog"],
)
