"""WIP Benchdog Clamp reconstructed from the supplied SolidCraft source.

This model intentionally follows only the final visible source state. Earlier
dog-expansion and compact-fork concepts remain in the retained native source,
but are hidden/replaced there and are not part of this first Forge baseline.

World axes match the native document:
    X: across the rail profile
    Y: along the rail / hinge pin
    Z: up

The native document finishes with one common +Z move (feature 83). The reusable
parts below keep their pre-move source coordinates and the assembly applies the
same final placement once per occurrence.
"""

from scpf import (
    Anchor,
    Axis,
    Box,
    Cylinder,
    Edges,
    Placement,
    Polygon2D,
    Sketch,
    component,
)


def _box_from_corner(length, width, height, x, y, z):
    return Box(
        length,
        width,
        height,
        anchor=Anchor.BOTTOM,
    ).at(
        x + length / 2,
        y + width / 2,
        z,
        anchor=Anchor.BOTTOM,
    )


@component(include="*")
class BenchdogClampSlide:
    """Final visible T-slide with fixed centre hinge eye (source 63-66, 71, 80)."""

    rail_inside_width = 12.0
    rail_opening = 7.0
    rail_clearance = 0.3
    rail_top = 6.0
    pin_diameter = 3.0
    hinge_height = 3.5
    hinge_outer_radius = 3.0
    hinge_axial_clearance = 0.25
    hinge_left_shift = 3.0

    def build(self):
        foot_x = 2.0 - self.rail_inside_width / 2 + self.rail_clearance
        foot_z = self.rail_top - 8.4 + self.rail_clearance
        foot_height = (
            self.rail_top - 2.0 - self.rail_clearance
            - foot_z
        )
        slide = _box_from_corner(
            self.rail_inside_width - 2 * self.rail_clearance,
            16.0,
            foot_height,
            foot_x,
            -8.0,
            foot_z,
        )

        neck_x = 2.0 - self.rail_opening / 2 + self.rail_clearance
        neck_z = self.rail_top - 2.0 - self.rail_clearance
        eye_base_z = (
            self.rail_top
            + self.hinge_height
            - self.hinge_outer_radius
            - self.rail_clearance
        )
        slide = slide + _box_from_corner(
            self.rail_opening - 2 * self.rail_clearance,
            16.0,
            eye_base_z - neck_z,
            neck_x,
            -8.0,
            neck_z,
        )

        eye_x = 2.0 - self.hinge_left_shift
        eye_width = 8.0 - 2 * self.hinge_axial_clearance
        slide = slide + _box_from_corner(
            4.0,
            eye_width,
            self.rail_top + self.hinge_height - eye_base_z,
            -self.hinge_left_shift,
            -4.0 + self.hinge_axial_clearance,
            eye_base_z,
        )
        slide = slide + Cylinder(
            d=2 * self.hinge_outer_radius,
            h=eye_width,
            axis=Axis.Y,
            anchor=Anchor.FRONT,
        ).at(
            eye_x,
            -4.0 + self.hinge_axial_clearance,
            self.rail_top + self.hinge_height,
            anchor=Anchor.FRONT,
        )

        # Late source feature 80 thickens the right side of the fixed eye.
        thick_x = 3.75 - self.hinge_left_shift
        slide = slide + _box_from_corner(
            6.5 - thick_x,
            eye_width,
            (
                self.rail_top + self.hinge_height + 2.0
                - eye_base_z
            ),
            thick_x,
            -4.0 + self.hinge_axial_clearance,
            eye_base_z,
        )

        pin_hole = Cylinder(
            d=self.pin_diameter + 0.2,
            h=20.0,
            axis=Axis.Y,
            anchor=Anchor.FRONT,
        ).at(
            eye_x,
            -10.0,
            self.rail_top + self.hinge_height,
            anchor=Anchor.FRONT,
        )
        return slide - pin_hole


@component(include="*")
class BenchdogClampHingeArm:
    """One source hinge arm; the assembly places a mirrored pair at ±Y."""

    rail_top = 6.0
    pin_diameter = 3.0
    hinge_height = 3.5
    hinge_outer_radius = 3.0
    hinge_left_shift = 3.0

    def build(self):
        eye_x = 2.0 - self.hinge_left_shift
        arm = _box_from_corner(
            11.0,
            4.0,
            3.0,
            -9.0 - self.hinge_left_shift,
            -2.0,
            self.rail_top + self.hinge_height - 1.5,
        )
        arm = arm + Cylinder(
            d=2 * self.hinge_outer_radius,
            h=4.0,
            axis=Axis.Y,
        ).at(
            eye_x,
            0.0,
            self.rail_top + self.hinge_height,
        )
        pin_hole = Cylinder(
            d=self.pin_diameter + 0.2,
            h=20.0,
            axis=Axis.Y,
        ).at(
            eye_x,
            0.0,
            self.rail_top + self.hinge_height,
        )
        return arm - pin_hole


@component(include="*")
class BenchdogClampHingePin:
    """Low Ø3 hinge pin with a Ø5 × 1.5 mm head (source 73-74)."""

    rail_top = 6.0
    pin_diameter = 3.0
    hinge_height = 3.5
    hinge_left_shift = 3.0

    def build(self):
        x = 2.0 - self.hinge_left_shift
        z = self.rail_top + self.hinge_height
        pin = Cylinder(
            d=self.pin_diameter,
            h=16.5,
            axis=Axis.Y,
            anchor=Anchor.FRONT,
        ).at(x, -8.0, z, anchor=Anchor.FRONT)
        head = Cylinder(
            d=5.0,
            h=1.5,
            axis=Axis.Y,
            anchor=Anchor.FRONT,
        ).at(x, -9.5, z, anchor=Anchor.FRONT)
        return pin + head


@component(include="*")
class BenchdogClampRailContext:
    """40 mm native dummy rail profile retained as WIP fit context."""

    rail_top = 6.0
    profile_inside_width = 12.55
    profile_opening = 8.30
    profile_length = 40.0

    SLOT_LIP_RADIUS = 1.6
    LOWER_RADIUS = 0.9

    def build(self):
        half_inside = self.profile_inside_width / 2
        half_opening = self.profile_opening / 2

        # These are world (X, Z) points reconstructed from native Sketch 76.
        # Polygon2D(world=True) handles SolidCraft's native XZ sketch-Y sign.
        points = [
            ("p1", (2.0 - half_inside - 1.8, self.rail_top)),
            ("p2", (2.0 - half_opening, self.rail_top)),
            ("p3", (2.0 - half_opening, self.rail_top - 2.0)),
            ("p4", (2.0 - half_inside, self.rail_top - 2.0)),
            ("p5", (2.0 - half_inside, self.rail_top - 8.4)),
            ("p6", (2.0 + half_inside, self.rail_top - 8.4)),
            ("p7", (2.0 + half_inside, self.rail_top - 2.0)),
            ("p8", (2.0 + half_opening, self.rail_top - 2.0)),
            ("p9", (2.0 + half_opening, self.rail_top)),
            ("p10", (2.0 + half_inside + 1.8, self.rail_top)),
            ("p11", (2.0 + half_inside + 1.8, self.rail_top - 6.8)),
            ("p12", (17.1, self.rail_top - 6.8)),
            ("p13", (17.1, self.rail_top - 7.6)),
            ("p14", (29.0, self.rail_top - 7.6)),
            ("p15", (29.0, self.rail_top - 6.8)),
            ("p16", (39.5, self.rail_top - 6.8)),
            ("p17", (39.5, self.rail_top - 9.4)),
            ("p18", (2.0 + half_inside + 1.8, self.rail_top - 9.4)),
            ("p19", (2.0 + half_inside + 1.8, self.rail_top - 10.4)),
            ("p20", (2.0 - half_inside - 1.8, self.rail_top - 10.4)),
        ]

        with Sketch(name="Dummy rail profile", plane="XZ") as sketch:
            Polygon2D(points, plane="XZ", world=True)

        rail = sketch.extrude(self.profile_length, sym=True)

        # Native source features 78/79 round the extrusion-axis edges at
        # profile vertices p1, p10 and p20.
        rail = rail.fillet(
            self.SLOT_LIP_RADIUS,
            edges=Edges.from_vertices("p1", "p10"),
        )
        rail = rail.fillet(
            self.LOWER_RADIUS,
            edges=Edges.from_vertices("p20"),
        )
        return rail


@component(include="*")
class BenchdogClampDog:
    """Straight Ø20 bench dog reference; source head feature 82 is suppressed."""

    rail_top = 6.0
    profile_inside_width = 12.55
    doghole_diameter = 20.0
    benchdog_rail_clearance = 0.5
    benchdog_along_position = 19.5

    DOG_HEIGHT = 27.5

    def build(self):
        x = (
            2.0
            - self.profile_inside_width / 2
            - 1.8
            - self.benchdog_rail_clearance
            - self.doghole_diameter / 2
        )
        return Cylinder(
            d=self.doghole_diameter,
            h=self.DOG_HEIGHT,
            anchor=Anchor.BOTTOM,
        ).at(
            x,
            self.benchdog_along_position,
            self.rail_top - 10.4,
            anchor=Anchor.BOTTOM,
        )


class BenchdogClamp:
    """Current visible WIP state of the source doghole-clamp design."""

    rail_inside_width = 12.0
    rail_opening = 7.0
    rail_top = 6.0
    rail_clearance = 0.3

    pin_diameter = 3.0
    hinge_height = 3.5
    hinge_outer_radius = 3.0
    hinge_axial_clearance = 0.25
    hinge_left_shift = 3.0

    profile_inside_width = 12.55
    profile_opening = 8.30
    profile_length = 40.0

    doghole_diameter = 20.0
    benchdog_rail_clearance = 0.5
    benchdog_along_position = 19.5

    def build(self):
        # Native source feature 83 moves all final visible bodies together so
        # the reference rail datum lands at its intended final Z position.
        final_z_shift = 10.4 - self.rail_top

        slide = BenchdogClampSlide(
            rail_inside_width=self.rail_inside_width,
            rail_opening=self.rail_opening,
            rail_clearance=self.rail_clearance,
            rail_top=self.rail_top,
            pin_diameter=self.pin_diameter,
            hinge_height=self.hinge_height,
            hinge_outer_radius=self.hinge_outer_radius,
            hinge_axial_clearance=self.hinge_axial_clearance,
            hinge_left_shift=self.hinge_left_shift,
            placement=Placement(z=final_z_shift),
        )

        left_arm = BenchdogClampHingeArm(
            rail_top=self.rail_top,
            pin_diameter=self.pin_diameter,
            hinge_height=self.hinge_height,
            hinge_outer_radius=self.hinge_outer_radius,
            hinge_left_shift=self.hinge_left_shift,
            placement=Placement(y=-6.0, z=final_z_shift),
        )
        right_arm = left_arm.copy(
            placement=Placement(y=6.0, z=final_z_shift),
        )

        hinge_pin = BenchdogClampHingePin(
            rail_top=self.rail_top,
            pin_diameter=self.pin_diameter,
            hinge_height=self.hinge_height,
            hinge_left_shift=self.hinge_left_shift,
            placement=Placement(z=final_z_shift),
        )

        rail = BenchdogClampRailContext(
            rail_top=self.rail_top,
            profile_inside_width=self.profile_inside_width,
            profile_opening=self.profile_opening,
            profile_length=self.profile_length,
            placement=Placement(z=final_z_shift),
        )

        dog = BenchdogClampDog(
            rail_top=self.rail_top,
            profile_inside_width=self.profile_inside_width,
            doghole_diameter=self.doghole_diameter,
            benchdog_rail_clearance=self.benchdog_rail_clearance,
            benchdog_along_position=self.benchdog_along_position,
            placement=Placement(z=final_z_shift),
        )

        return slide + left_arm + right_arm + hinge_pin + rail + dog


BenchdogClamp()
