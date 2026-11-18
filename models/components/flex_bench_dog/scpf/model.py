"""Reusable 20 mm flex bench dog based on the supplied Mini-MFT reference image.

The CAD orientation is functional rather than a prescribed print orientation:
the worktop surface is Z=0, the 18 mm insert points downward and the dog rises
20 mm above the worktop. A small flare at the free insert end provides passive
spring preload after the stem is split into four flexible quadrants.
"""


@component
class FlexBenchDog:
    hole_diameter = 20.0
    interference = 0.20
    rim_diameter = 24.0
    slot_width = 1.5

    ABOVE_WORKTOP = 20.0
    RIM_THICKNESS = 3.0
    INSERTION_LENGTH = 18.0
    TIP_FLARE_LENGTH = 2.0
    SLOT_LENGTH = 14.0
    TOP_FILLET = 1.0
    TOP_CHAMFER = 0.6
    LOGO_SIZE = 8.0
    LOGO_HEIGHT = 0.6

    def build(self):
        # Rim bottom is the worktop datum. The narrower working cylinder starts
        # on the rim and ends at the requested 20 mm height above the worktop.
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

        # Straight insert root below Z=0, with only the free 2 mm flared.
        insert = Cylinder(
            d=self.hole_diameter,
            h=self.INSERTION_LENGTH,
            anchor=Anchor.BOTTOM,
        ).at(0, 0, -self.INSERTION_LENGTH, anchor=Anchor.BOTTOM)
        dog = dog + insert

        flare = Cylinder(
            d=self.hole_diameter + self.interference,
            h=self.TIP_FLARE_LENGTH,
            anchor=Anchor.BOTTOM,
        ).at(0, 0, -self.INSERTION_LENGTH, anchor=Anchor.BOTTOM)
        dog = dog + flare

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

        # Finish the visible upper body after the main solid has been formed.
        dog = dog.fillet(
            self.TOP_FILLET,
            edges=[(self.hole_diameter / 2, 0, self.RIM_THICKNESS)],
        )
        dog = dog.chamfer(
            self.TOP_CHAMFER,
            edges=[(self.hole_diameter / 2, 0, self.ABOVE_WORKTOP)],
        )

        # Small raised square used as a simple BBE/box mark.
        with Sketch(
            name="Top logo",
            on=dog,
            plane="XY",
            origin=(0, 0, self.ABOVE_WORKTOP),
        ) as logo:
            Rectangle2D(self.LOGO_SIZE, self.LOGO_SIZE)
        dog = dog + logo.extrude(self.LOGO_HEIGHT)

        return dog
