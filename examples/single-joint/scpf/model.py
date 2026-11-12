"""Minimal SolidCraft Forge assembly with exactly one rigid joint.

This example intentionally avoids custom AnchorFrame objects, corner/edge
anchors, copies, groups and extra placement logic. It exists to inspect the
native visualization and behavior of one ordinary face-to-face joint.
"""


class Base:
    def build(self):
        return Box(80, 40, 20)


class Child:
    def build(self):
        return Box(30, 20, 20)


class SingleJoint:
    def build(self):
        base = Base()
        child = Child().attach(
            base,
            parent=Anchor.RIGHT,
            child=Anchor.LEFT,
        )
        return base + child


SingleJoint()
