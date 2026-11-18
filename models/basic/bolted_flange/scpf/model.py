"""Bolted flange with a native circular bolt-hole pattern."""


class Flange:
    bolts = 6
    pcd = 70.0

    def build(self):
        flange = Cylinder(d=100, h=10, anchor=Anchor.BOTTOM)

        with Sketch(name="BoltHole", on=flange, parent=Anchor.TOP) as bolt:
            bolt.add(
                Circle2D(d=9),
                offset=(self.pcd / 2, 0),
            )

        source_cut = bolt.extrude(Depth.THROUGH_ALL)
        flange = flange - source_cut
        flange = flange.circular_pattern(
            source_cut,
            count=self.bolts,
            axis=Axis.Z,
        )

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

        return flange
