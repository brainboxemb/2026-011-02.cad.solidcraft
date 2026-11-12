"""Minimal assembly with one corner parent and one custom child anchor.

This isolates the remaining difference from the HUB75 corner-bracket joints:
the parent uses a standard corner Anchor while the child uses a named
AnchorFrame that Forge materializes as one native joint.origin.
"""

from scpf import AnchorFrame


class Base:
    def build(self):
        return Box(80, 40, 80)


class Child:
    def anchors(self):
        return {
            "mount": AnchorFrame(
                origin=(0, 0, 0),
                z=(0, 1, 0),
                x=(1, 0, 0),
            ),
        }

    def build(self):
        return Box(30, 20, 20)


class SingleCustomAnchorJoint:
    def build(self):
        base = Base()
        child = Child().attach(
            base,
            parent=Anchor.FRONT_TOP_RIGHT,
            child="mount",
        )
        return base + child


SingleCustomAnchorJoint()
