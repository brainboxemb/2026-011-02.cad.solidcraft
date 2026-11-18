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

# Flex slot X.
script.add(
    "sketch.create",
    plane={"origin": [0, 0, -18], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]},
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
    distance=14,
    direction="positive",
    operation="cut",
    targets=["FlexBenchDog"],
    name="Flex slot X",
)

# Flex slot Y.
script.add(
    "sketch.create",
    plane={"origin": [0, 0, -18], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]},
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
    distance=14,
    direction="positive",
    operation="cut",
    targets=["FlexBenchDog"],
    name="Flex slot Y",
)

# Visible top finish.
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

# Recessed square box logo.
script.add(
    "sketch.create",
    plane={"origin": [0, 0, 20], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]},
    name="Top logo",
)
script.add(
    "sketch.rectangle.two_point",
    p0=[-4, -4],
    p1=[4, 4],
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
