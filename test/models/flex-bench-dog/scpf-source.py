"""Reusable 20 mm flex bench dog based on the supplied Mini-MFT reference image.

The CAD orientation is functional rather than a prescribed print orientation:
the worktop surface is Z=0, the insert extends 20 mm downward and the dog rises
20 mm upward. The insert tapers continuously from Ø20.0 at the worktop to
Ø20.2 at the free end, providing passive spring preload after the stem is split
into four flexible quadrants.
"""

from scpf import (
    Anchor,
    Cone,
    Cylinder,
    Polygon2D,
    Rectangle2D,
    Sketch,
    component,
)


def _logo_strip_points(p0, p1, width):
    """Return one square-ended polygon strip around a logo centreline."""
    x0, y0 = p0
    x1, y1 = p1
    dx = x1 - x0
    dy = y1 - y0
    length = (dx * dx + dy * dy) ** 0.5
    half_width = width / 2.0

    ux = dx / length
    uy = dy / length
    px = -uy * half_width
    py = ux * half_width
    ex = ux * half_width
    ey = uy * half_width

    # Extend both ends by half the line width. Neighbouring ribs overlap at
    # cube vertices without combining intersecting loops in one Sketch.
    return (
        (x0 - ex + px, y0 - ey + py),
        (x1 + ex + px, y1 + ey + py),
        (x1 + ex - px, y1 + ey - py),
        (x0 - ex - px, y0 - ey - py),
    )


@component
class FlexBenchDog:
    hole_diameter = 20.0
    interference = 0.20
    rim_diameter = 22.0
    slot_width = 1.5
    slot_corner_radius = 0.5

    ABOVE_WORKTOP = 20.0
    RIM_THICKNESS = 1.5
    RIM_SEAT_CHAMFER = 1.0
    INSERTION_LENGTH = 20.0
    SLOT_LENGTH = 16.0
    TOP_CHAMFER = 0.6
    BOTTOM_CHAMFER = 1.0
    LOGO_LINE_WIDTH = 0.6
    LOGO_DEPTH = 0.6

    LOGO_SEGMENTS = (
        ((0.0, 4.0), (3.5, 2.0)),
        ((3.5, 2.0), (3.5, -2.0)),
        ((3.5, -2.0), (0.0, -4.0)),
        ((0.0, -4.0), (-3.5, -2.0)),
        ((-3.5, -2.0), (-3.5, 2.0)),
        ((-3.5, 2.0), (0.0, 4.0)),
        ((0.0, 0.0), (0.0, 4.0)),
        ((0.0, 0.0), (3.5, -2.0)),
        ((0.0, 0.0), (-3.5, -2.0)),
    )

    def build(self):
        # The stop collar sits on the small 45-degree mouth chamfer of a
        # nominal 20 mm MFT hole. Its Ø22 × 1.5 mm envelope is chamfered only
        # at the lower outside edge: 1 mm radial difference gives a 1 mm axial
        # 45-degree seat, leaving a 0.5 mm straight Ø22 land above it.
        rim = Cylinder(
            d=self.rim_diameter,
            h=self.RIM_THICKNESS,
            anchor=Anchor.BOTTOM,
        )
        rim = rim.chamfer(
            self.RIM_SEAT_CHAMFER,
            edges=[(self.rim_diameter / 2, 0, 0)],
        )

        working_height = self.ABOVE_WORKTOP - self.RIM_THICKNESS
        upper = Cylinder(
            d=self.hole_diameter,
            h=working_height,
            anchor=Anchor.BOTTOM,
        ).at(0, 0, self.RIM_THICKNESS, anchor=Anchor.BOTTOM)
        dog = rim + upper

        # Full-length insertion taper: Ø20.2 at the free end (Z=-20) to
        # nominal Ø20.0 at the worktop datum (Z=0). Forge #746 provides the
        # native joined-Cone path; no stepped cylindrical tip remains.
        insert = Cone(
            d=self.hole_diameter + self.interference,
            top_d=self.hole_diameter,
            h=self.INSERTION_LENGTH,
            anchor=Anchor.BOTTOM,
        ).at(0, 0, -self.INSERTION_LENGTH, anchor=Anchor.BOTTOM)
        dog = dog + insert

        # Give the complete free insert edge a larger lead-in before splitting
        # it into four flexible legs.
        dog = dog.chamfer(
            self.BOTTOM_CHAMFER,
            edges=[(
                (self.hole_diameter + self.interference) / 2,
                0,
                -self.INSERTION_LENGTH,
            )],
        )

        # Two native sketch cuts form the cross slots. They start at the free
        # end and stop 4 mm below the worktop, leaving a solid flex root.
        slot_span = self.hole_diameter + self.interference + 2.0

        with Sketch(
            name="Flex slot X",
            on=dog,
            plane="XY",
            origin=(0, 0, -self.INSERTION_LENGTH),
        ) as slot_x:
            Rectangle2D(slot_span, self.slot_width)
        dog = dog - slot_x.extrude(self.SLOT_LENGTH)

        with Sketch(
            name="Flex slot Y",
            on=dog,
            plane="XY",
            origin=(0, 0, -self.INSERTION_LENGTH),
        ) as slot_y:
            Rectangle2D(self.slot_width, slot_span)
        dog = dog - slot_y.extrude(self.SLOT_LENGTH)

        # Round only the four vertical material corners around the central
        # cross. The rectangular slot dimensions and 4 mm solid root remain
        # unchanged.
        slot_half = self.slot_width / 2
        slot_edge_z = -self.INSERTION_LENGTH + self.SLOT_LENGTH / 2
        dog = dog.fillet(
            self.slot_corner_radius,
            edges=[
                (slot_half, slot_half, slot_edge_z),
                (-slot_half, slot_half, slot_edge_z),
                (-slot_half, -slot_half, slot_edge_z),
                (slot_half, -slot_half, slot_edge_z),
            ],
        )

        # Light chamfer on the visible upper perimeter.
        dog = dog.chamfer(
            self.TOP_CHAMFER,
            edges=[(self.hole_diameter / 2, 0, self.ABOVE_WORKTOP)],
        )

        # Recess the accepted BrainBox wireframe as nine independent closed
        # polygon strips. Each strip keeps the accepted centreline and 0.6 mm
        # width, extends half a line width beyond each endpoint, and is cut
        # independently so intersecting ribs cannot create filled face regions.
        for index, (p0, p1) in enumerate(self.LOGO_SEGMENTS, start=1):
            with Sketch(
                name=f"Top logo rib {index}",
                on=dog,
                plane="XY",
                origin=(0, 0, self.ABOVE_WORKTOP),
            ) as rib:
                Polygon2D(
                    _logo_strip_points(p0, p1, self.LOGO_LINE_WIDTH),
                    plane="XY",
                )
            dog = dog - rib.extrude(-self.LOGO_DEPTH)

        return dog
