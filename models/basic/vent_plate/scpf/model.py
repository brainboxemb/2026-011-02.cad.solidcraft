"""Vent Plate from the SolidCraft example, using one native feature pattern.

The source cut is authored once. SCPF 0.6.1 lowers rectangular_pattern()
directly to SolidCraft's solid.pattern.rectangular history feature.
"""


class Plate:
    cols = 6
    rows = 3
    pitch = 16.0

    def build(self):
        # Match the source SolidCraft box corner [0, 0, 0].
        plate = Box(120, 80, 4).at(
            60, 40, 0,
            anchor=Anchor.BOTTOM,
        )
        plate = plate.fillet(8, edges=Edges.VERTICAL)

        # The source rectangle is X=18..24, Y=12..26. The attached sketch
        # coordinates are relative to the 120 x 80 plate centre (60, 40).
        with Sketch(name="Vent", on=plate, parent=Anchor.BOTTOM) as vent:
            vent.add(
                Rectangle2D(6, 14),
                offset=(-39, -21),
            )

        source_cut = vent.extrude(4)
        plate = plate - source_cut

        return plate.rectangular_pattern(
            source_cut,
            count=self.cols,
            spacing=self.pitch,
            direction=Axis.X,
            count2=self.rows,
            spacing2=22,
            direction2=Axis.Y,
        )
