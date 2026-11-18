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
    LOGO_OUTER = 8.0
    LOGO_INNER = 5.0
    LOGO_HEIGHT = 0.6

    def build(self):
        # The rim rests on the worktop at Z=0. The cylindrical working section
        # starts on top of the rim and finishes at Z=ABOVE_WORKTOP.
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

        # Round the shoulder slightly and soften the upper perimeter.
        upper = upper.fillet(
            self.TOP_FILLET,
            edges=[(self.hole_diameter / 2, 0, self.RIM_THICKNESS)],
        )
        upper = upper.chamfer(
            self.TOP_CHAMFER,
            edges=[(self.hole_diameter / 2, 0, self.ABOVE_WORKTOP)],
        )
        dog = rim + upper

        # Straight insert root, with only the free 2 mm flared outward.
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

        # Slots start at the free end and stop 4 mm before the worktop. The
        # resulting four legs can spring inward when the flared tips enter a
        # nominal 20 mm dog hole.
        slot_z = -self.INSERTION_LENGTH
        slot_span = self.hole_diameter + self.interference + 2.0
        slot_x = Box(
            slot_span,
            self.slot_width,
            self.SLOT_LENGTH,
        ).at(0, 0, slot_z, anchor=Anchor.BOTTOM)
        slot_y = Box(
            self.slot_width,
            slot_span,
            self.SLOT_LENGTH,
        ).at(0, 0, slot_z, anchor=Anchor.BOTTOM)
        dog = dog - slot_x
        dog = dog - slot_y

        # Small raised box-outline logo on the top face.
        logo = Box(
            self.LOGO_OUTER,
            self.LOGO_OUTER,
            self.LOGO_HEIGHT,
        ).at(0, 0, self.ABOVE_WORKTOP, anchor=Anchor.BOTTOM)
        logo_cut = Box(
            self.LOGO_INNER,
            self.LOGO_INNER,
            self.LOGO_HEIGHT,
        ).at(0, 0, self.ABOVE_WORKTOP, anchor=Anchor.BOTTOM)
        logo = logo - logo_cut
        dog = dog + logo

        return dog
