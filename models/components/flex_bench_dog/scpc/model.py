"""FlexBenchDog expressed directly as SolidCraft commands."""

from scpc import Script

script = Script()

for name, value in (
    ("hole_diameter", 20.0),
    ("interference", 0.20),
    ("rim_diameter", 22.0),
    ("slot_width", 1.5),
):
    script.add("parameters.add", name=name, expression=str(value), unit="mm")

# Small stop rim at the worktop datum.
script.add(
    "solid.cylinder",
    height=1.5,
    diameter="rim_diameter",
    base=[0, 0, 0],
    axis="Z",
    operation="new",
    body_name="FlexBenchDog",
)

# Working section to Z=20.
script.add(
    "solid.cylinder",
    height=18.5,
    diameter="hole_diameter",
    base=[0, 0, 1.5],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)

# Full-length shallow taper: Ø20.2 at the free end to Ø20.0 at the rim.
script.add(
    "solid.cone",
    height=20,
    diameter="hole_diameter + interference",
    top_diameter="hole_diameter",
    base=[0, 0, -20],
    axis="Z",
    operation="join",
    targets=["FlexBenchDog"],
)

# Larger lead-in chamfer on the free insert edge.
script.add(
    "solid.chamfer",
    body="FlexBenchDog",
    distance=1.0,
    edges=[[10.1, 0, -20]],
)

# Flex slot X.
script.add(
    "sketch.create",
    plane={"origin": [0, 0, -20], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]},
    name="Flex slot X",
)
script.add(
    "sketch.rectangle.two_point",
    p0=["-(hole_diameter + interference + 2) / 2", "-slot_width / 2"],
    p1=["(hole_diameter + interference + 2) / 2", "slot_width / 2"],
)
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance=16,
    direction="positive",
    operation="cut",
    targets=["FlexBenchDog"],
    name="Flex slot X",
)

# Flex slot Y.
script.add(
    "sketch.create",
    plane={"origin": [0, 0, -20], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]},
    name="Flex slot Y",
)
script.add(
    "sketch.rectangle.two_point",
    p0=["-slot_width / 2", "-(hole_diameter + interference + 2) / 2"],
    p1=["slot_width / 2", "(hole_diameter + interference + 2) / 2"],
)
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance=16,
    direction="positive",
    operation="cut",
    targets=["FlexBenchDog"],
    name="Flex slot Y",
)

# Light chamfer on the visible upper perimeter.
script.add(
    "solid.chamfer",
    body="FlexBenchDog",
    distance=0.6,
    edges=[[10, 0, 20]],
)

# Recessed isometric cube/box wireframe.
script.add(
    "sketch.create",
    plane={"origin": [0, 0, 20], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]},
    name="Top logo",
)
for p0, p1 in (
    ([0.0, 4.0], [3.5, 2.0]),
    ([3.5, 2.0], [3.5, -2.0]),
    ([3.5, -2.0], [0.0, -4.0]),
    ([0.0, -4.0], [-3.5, -2.0]),
    ([-3.5, -2.0], [-3.5, 2.0]),
    ([-3.5, 2.0], [0.0, 4.0]),
    ([0.0, 0.0], [0.0, 4.0]),
    ([0.0, 0.0], [3.5, -2.0]),
    ([0.0, 0.0], [-3.5, -2.0]),
):
    script.add(
        "sketch.slot.center_to_center",
        p0=p0,
        p1=p1,
        width=0.6,
    )
script.add("sketch.finish")
script.add(
    "solid.extrude",
    distance=0.6,
    direction="negative",
    operation="cut",
    targets=["FlexBenchDog"],
    name="Top logo",
)
