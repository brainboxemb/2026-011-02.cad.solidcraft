"""Simple bolted flange built from SolidCraft primitives."""

class Flange:
    bolts = 6
    pcd = 70.0

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

        bolt_hole = Hole(
            d=9,
            depth=10,
            direction=(0, 0, -1),
        ).at(self.pcd / 2, 0, 10)
        flange = flange + bolt_hole

        return flange.circular_pattern(
            bolt_hole,
            count=self.bolts,
            axis=Axis.Z,
        )
