"""Simple bolted flange built from SolidCraft primitives."""

from math import cos, radians, sin


class Flange:
    BOLTS = 6
    PCD = 70.0

    def build(self):
        flange = Cylinder(d=100, h=10, anchor=Anchor.BOTTOM)

        hub = Cylinder(d=44, h=16, anchor=Anchor.BOTTOM).at(
            0, 0, 10, anchor=Anchor.BOTTOM
        )
        flange = flange + hub

        bore = Hole(
            d=24,
            depth=26,
            direction=(0, 0, -1),
        ).at(0, 0, 26)
        flange = flange + bore

        radius = self.PCD / 2
        for index in range(self.BOLTS):
            angle = radians(index * 360 / self.BOLTS)
            bolt_hole = Hole(
                d=9,
                depth=10,
                direction=(0, 0, -1),
            ).at(
                radius * cos(angle),
                radius * sin(angle),
                10,
            )
            flange = flange + bolt_hole

        return flange
