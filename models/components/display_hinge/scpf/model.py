"""Provisional 180-degree external hinge for the wooden HUB75 display.

Coordinate contract:
- Y is the hinge/pin axis;
- X runs across the two leaves;
- the hinge axis is at X=0, Z=0;
- both mounting leaves sit below the hinge axis;
- the default model is shown fully open at 180 degrees.

This first component is intentionally a conventional pin hinge. It establishes
the reusable mounting/pin interface without pretending to be the later
concealed multi-link/spider mechanism explored in the HUB75 hinge notes.
Dimensions remain provisional until fitted to the physical enclosure.
"""

from scpf import Axis, Box, Cylinder, component


def _leaf_body(owner, *, side, owned_segments):
    """Build one printed leaf with alternating knuckles."""
    barrel_radius = owner.barrel_diameter / 2
    segment_length = (
        owner.hinge_length - 4 * owner.axial_clearance
    ) / 5

    plate_x = side * (barrel_radius + owner.leaf_reach / 2)
    plate_z = -barrel_radius + owner.leaf_thickness / 2

    leaf = Box(
        owner.leaf_reach,
        owner.hinge_length,
        owner.leaf_thickness,
    ).at(
        plate_x,
        0,
        plate_z,
    )

    # Each leaf owns alternating barrel segments. Small local bridges overlap
    # both its plate and its own barrel segments, while staying clear of the
    # other leaf's knuckles.
    for index in owned_segments:
        y = (
            -owner.hinge_length / 2
            + segment_length / 2
            + index * (segment_length + owner.axial_clearance)
        )

        knuckle = Cylinder(
            d=owner.barrel_diameter,
            h=segment_length,
            axis=Axis.Y,
        ).at(0, y, 0)

        bridge = Box(
            owner.bridge_width,
            segment_length,
            owner.bridge_height,
        ).at(
            side * barrel_radius,
            y,
            -owner.bridge_height / 2,
        )

        leaf = leaf + knuckle + bridge

    # One continuous bore is simpler and more exact than cutting every
    # knuckle independently. It only intersects the alternating barrel
    # segments because the mounting plate starts outside the barrel radius.
    pin_bore = Cylinder(
        d=owner.pin_diameter + 2 * owner.pin_radial_clearance,
        h=owner.hinge_length + 2,
        axis=Axis.Y,
    )
    leaf = leaf - pin_bore

    # Two simple through holes per leaf. They are deliberately ordinary
    # clearance bores in this prototype; screw-head treatment belongs to the
    # enclosure fit review, not to this first hinge geometry.
    hole_x = side * (barrel_radius + owner.leaf_reach / 2)
    for y in (-owner.mounting_hole_pitch / 2, owner.mounting_hole_pitch / 2):
        cutter = Cylinder(
            d=owner.mounting_hole_diameter,
            h=owner.leaf_thickness + 2,
            axis=Axis.Z,
        ).at(
            hole_x,
            y,
            plate_z,
        )
        leaf = leaf - cutter

    return leaf.with_material(
        "PETG hinge leaf",
        density_g_cm3=1.27,
        color="#30343B",
    )


@component(include="*")
class DisplayHingeLeafA:
    hinge_length = 36.0
    leaf_reach = 24.0
    leaf_thickness = 4.0
    barrel_diameter = 10.0
    pin_diameter = 4.0
    pin_radial_clearance = 0.30
    axial_clearance = 0.40
    bridge_width = 3.0
    bridge_height = 4.0
    mounting_hole_diameter = 4.5
    mounting_hole_pitch = 18.0

    def build(self):
        return _leaf_body(self, side=1, owned_segments=(0, 2, 4))


@component(include="*")
class DisplayHingeLeafB:
    hinge_length = 36.0
    leaf_reach = 24.0
    leaf_thickness = 4.0
    barrel_diameter = 10.0
    pin_diameter = 4.0
    pin_radial_clearance = 0.30
    axial_clearance = 0.40
    bridge_width = 3.0
    bridge_height = 4.0
    mounting_hole_diameter = 4.5
    mounting_hole_pitch = 18.0

    def build(self):
        return _leaf_body(self, side=-1, owned_segments=(1, 3))


@component(include="*")
class DisplayHingePin:
    hinge_length = 36.0
    pin_diameter = 4.0
    pin_end_overhang = 1.0

    def build(self):
        return Cylinder(
            d=self.pin_diameter,
            h=self.hinge_length + 2 * self.pin_end_overhang,
            axis=Axis.Y,
        ).with_material(
            "Steel hinge pin",
            density_g_cm3=7.85,
            color="#AEB4BA",
        )


class DisplayHinge:
    """Complete reusable hinge occurrence shown in the fully-open state."""

    def build(self):
        return DisplayHingeLeafA() + DisplayHingeLeafB() + DisplayHingePin()


DisplayHinge()
