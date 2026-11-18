"""Reusable 20 mm flex bench dog based on the supplied Mini-MFT reference image.

The worktop surface is Z=0. The dog extends 20 mm upward and the insert extends
20 mm downward. The complete insert is a shallow frustum: Ø20.0 mm at the rim
and Ø20.2 mm at the free end. Two crossing slots turn that taper into four
flexible legs that provide passive spring preload without separate hardware.
"""


@component
class FlexBenchDog:
    hole_diameter = 20.0
    interference = 0.20
    rim_diameter = 22.0
    slot_width = 1.5

    ABOVE_WORKTOP = 20.0
    RIM_THICKNESS = 1.5
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
        # Very small stop rim: only 1 mm radial overhang around the Ø20 body.
        rim = Cylinder(
            d=self.rim_diameter,
            h=self.RIM_THICKNESS,
            anchor=Anchor.BOTTOM,
        )

        working_height = self.ABOVE_WORKTOP - self.RIM_THICKNESS
        upper = Cylinder(
            d=self.hole_diameter,
            h=working_height,
            anchor=Anchor.BOTTOM,
        ).at(0, 0, self.RIM_THICKNESS, anchor=Anchor.BOTTOM)
        dog = rim + upper

        # One true full-length taper. The base/free end is slightly larger;
        # Anchor.TOP keeps the Ø20 top end exactly at the worktop datum Z=0.
        insert = Cone(
            d=self.hole_diameter + self.interference,
            top_d=self.hole_diameter,
            h=self.INSERTION_LENGTH,
            anchor=Anchor.TOP,
        )
        dog = dog + insert

        # Larger lead-in chamfer on the free lower edge.
        dog = dog.chamfer(
            self.BOTTOM_CHAMFER,
            edges=[(
                (self.hole_diameter + self.interference) / 2,
                0,
                -self.INSERTION_LENGTH,
            )],
        )

        # Cross slots start at the free end and stop 4 mm below the rim.
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

        # Light chamfer on the visible upper perimeter.
        dog = dog.chamfer(
            self.TOP_CHAMFER,
            edges=[(self.hole_diameter / 2, 0, self.ABOVE_WORKTOP)],
        )

        # Recess the cube/box wireframe from the supplied logo reference.
        with Sketch(
            name="Top logo",
            on=dog,
            plane="XY",
            origin=(0, 0, self.ABOVE_WORKTOP),
        ) as logo:
            for p0, p1 in self.LOGO_SEGMENTS:
                SlotCenterToCenter2D(p0, p1, self.LOGO_LINE_WIDTH)
        dog = dog - logo.extrude(-self.LOGO_DEPTH)

        return dog
