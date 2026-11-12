"""Minimal assembly with exactly one corner-referenced rigid joint.

This differs from examples/single-joint only in the parent reference:
Anchor.FRONT_TOP_RIGHT forces Forge to describe the parent reference through
SolidCraft's native edge/on/corner selector. The child still uses a plain face
anchor, so any additional selection lines can be attributed to the corner
reference.
"""


class Base:
    def build(self):
        return Box(80, 40, 80)


class Child:
    def build(self):
        return Box(30, 20, 20)


class SingleCornerJoint:
    def build(self):
        base = Base()
        child = Child().attach(
            base,
            parent=Anchor.FRONT_TOP_RIGHT,
            child=Anchor.LEFT,
        )
        return base + child


SingleCornerJoint()
