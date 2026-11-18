"""Reusable 20 mm flex bench dog based on the supplied Mini-MFT reference image.

The fit is intentionally passive: a slightly oversized insertion stem is split
by two crossing slots so the four quadrants can flex inward in a 20 mm dog hole.
No screw, nut, O-ring or separate expansion part is used.
"""


@component
class FlexBenchDog:
    hole_diameter = 20.0
    interference = 0.20
    working_height = 35.0
    rim_diameter = 24.0
    rim_thickness = 3.0
    insertion_length = 38.0
    slot_width = 1.5
    slot_length = 30.0

    def build(self):
        # The lower cylinder is the part that remains above the worktop.
        dog = Cylinder(
            d=self.hole_diameter,
            h=self.working_height,
            anchor=Anchor.BOTTOM,
        )

        # Small stop rim rests on the worktop.
        rim = Cylinder(
            d=self.rim_diameter,
            h=self.rim_thickness,
            anchor=Anchor.BOTTOM,
        ).at(0, 0, self.working_height, anchor=Anchor.BOTTOM)
        dog = dog + rim

        # The insertion stem is 0.2 mm oversized by default. The crossed slots
        # turn it into four flexible quadrants that can compress into the hole.
        stem_diameter = self.hole_diameter + self.interference
        stem_z = self.working_height + self.rim_thickness
        stem = Cylinder(
            d=stem_diameter,
            h=self.insertion_length,
            anchor=Anchor.BOTTOM,
        ).at(0, 0, stem_z, anchor=Anchor.BOTTOM)
        dog = dog + stem

        slot_z = stem_z + self.insertion_length - self.slot_length
        slot_x = Box(
            stem_diameter + 2.0,
            self.slot_width,
            self.slot_length,
        ).at(0, 0, slot_z, anchor=Anchor.BOTTOM)
        slot_y = Box(
            self.slot_width,
            stem_diameter + 2.0,
            self.slot_length,
        ).at(0, 0, slot_z, anchor=Anchor.BOTTOM)

        dog = dog - slot_x
        dog = dog - slot_y
        return dog
