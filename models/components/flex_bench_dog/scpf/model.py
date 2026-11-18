"""Reusable 20 mm flex bench dog based on the supplied Mini-MFT reference image.

The fit is intentionally passive: a slightly oversized insertion stem is split
by two crossing slots so the four quadrants can flex inward in a 20 mm dog hole.
No screw, nut, O-ring or separate expansion part is used.
"""


@component
class FlexBenchDog:
    # Native fit parameters. These are the dimensions most useful to tune after
    # a first print in a real 20 mm worktop.
    hole_diameter = 20.0
    interference = 0.20
    rim_diameter = 24.0
    slot_width = 1.5

    # Fixed first-prototype proportions inferred from the supplied image.
    WORKING_HEIGHT = 35.0
    RIM_THICKNESS = 3.0
    INSERTION_LENGTH = 38.0
    SLOT_LENGTH = 30.0

    def build(self):
        dog = Cylinder(
            d=self.hole_diameter,
            h=self.WORKING_HEIGHT,
            anchor=Anchor.BOTTOM,
        )

        rim = Cylinder(
            d=self.rim_diameter,
            h=self.RIM_THICKNESS,
            anchor=Anchor.BOTTOM,
        ).at(0, 0, self.WORKING_HEIGHT, anchor=Anchor.BOTTOM)
        dog = dog + rim

        stem_diameter = self.hole_diameter + self.interference
        stem_z = self.WORKING_HEIGHT + self.RIM_THICKNESS
        stem = Cylinder(
            d=stem_diameter,
            h=self.INSERTION_LENGTH,
            anchor=Anchor.BOTTOM,
        ).at(0, 0, stem_z, anchor=Anchor.BOTTOM)
        dog = dog + stem

        slot_z = stem_z + self.INSERTION_LENGTH - self.SLOT_LENGTH
        slot_x = Box(
            22.2,
            self.slot_width,
            self.SLOT_LENGTH,
        ).at(0, 0, slot_z, anchor=Anchor.BOTTOM)
        slot_y = Box(
            self.slot_width,
            22.2,
            self.SLOT_LENGTH,
        ).at(0, 0, slot_z, anchor=Anchor.BOTTOM)

        dog = dog - slot_x
        dog = dog - slot_y
        return dog
