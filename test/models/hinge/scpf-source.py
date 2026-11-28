"""Basic two-leaf hinge reconstructed from the supplied SolidCraft source.

The source owns two identical components (Leaf A / Leaf B) joined by a native
revolute relationship. Each source leaf contains a 40 x 30 x 3 mm box and a
separate Ø8 x 40 mm cylinder. They overlap physically, so Forge joins those
primitive bodies inside one reusable leaf definition while preserving the
important source ownership boundary: two independent leaf occurrences and one
native driveable hinge joint.
"""

from scpf import (
    Anchor,
    AnchorFrame,
    Axis,
    Box,
    Cylinder,
    component,
)


@component(include="*")
class HingeLeaf:
    length = 40.0
    width = 30.0
    thickness = 3.0

    knuckle_diameter = 8.0
    knuckle_length = 40.0
    knuckle_y = 33.0
    knuckle_z = 4.0

    def anchors(self):
        return {
            "hinge_axis": AnchorFrame(
                origin=(0.0, 33.0, 4.0),
                z=(1.0, 0.0, 0.0),
                x=(0.0, 0.0, -1.0),
            ),
        }

    def build(self):
        plate = Box(
            self.length,
            self.width,
            self.thickness,
            anchor=Anchor.BOTTOM,
        ).at(
            self.length / 2,
            self.width / 2,
            0.0,
            anchor=Anchor.BOTTOM,
        )

        knuckle = Cylinder(
            d=self.knuckle_diameter,
            h=self.knuckle_length,
            axis=Axis.X,
            anchor=Anchor.LEFT,
        ).at(
            0.0,
            self.knuckle_y,
            self.knuckle_z,
            anchor=Anchor.LEFT,
        )

        return plate + knuckle


class Hinge:
    _initial_angle = 60.0
    _minimum_angle = 0.0
    _maximum_angle = 180.0

    def build(self):
        leaf_a = HingeLeaf(name="LeafA")
        leaf_b = HingeLeaf(name="LeafB").attach(
            leaf_a,
            parent="hinge_axis",
            child="hinge_axis",
            kind="revolute",
            value=self._initial_angle,
            limits=(self._minimum_angle, self._maximum_angle),
            name="Hinge",
        )
        return leaf_a + leaf_b


Hinge()
