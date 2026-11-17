"""Simple MFT worktop inspired by the Craftmaker S30 replacement top.

The plate envelope and dog-hole diameter follow the published replacement-top
dimensions. The 76 mm pitch, 20 mm corner cuts and clamp-slot dimensions are
photo-based design estimates, not manufacturer dimensions.

The current 2D expectation is calibrated from the front product photo:
- slot width about 24 mm;
- slot end-centre distance about 80 mm, giving about 104 mm overall length;
- per diagonal arm, the inner slot starts on grid ring 1 and extends outward;
- the outer slot starts on grid ring 3 and extends inward;
- grid ring 2 remains a normal dog hole between the two slots.
"""

from math import sqrt


class SimpleMFT:
    width = 805.0
    depth = 555.0
    thickness = 18.0
    hole_diameter = 20.0
    hole_pitch = 76.0
    corner_chamfer = 20.0

    COLUMNS = 9
    ROWS = 7

    SLOT_WIDTH = 24.0
    SLOT_CENTER_DISTANCE = 80.0

    def build(self):
        half_w = self.width / 2
        half_d = self.depth / 2
        c = self.corner_chamfer

        with Sketch(name="Worktop outline", plane="XY") as outline:
            Polygon2D([
                (-half_w + c, -half_d),
                (half_w - c, -half_d),
                (half_w, -half_d + c),
                (half_w, half_d - c),
                (half_w - c, half_d),
                (-half_w + c, half_d),
                (-half_w, -half_d + c),
            ])

        board = outline.extrude(self.thickness)

        with Sketch(name="Dog hole", on=board, parent=Anchor.TOP) as hole:
            hole.add(
                Circle2D(d=self.hole_diameter),
                offset=(-4 * self.hole_pitch, -3 * self.hole_pitch),
            )

        hole_cut = hole.extrude(Depth.THROUGH_ALL)
        board = board - hole_cut
        board = board.rectangular_pattern(
            hole_cut,
            count=self.COLUMNS,
            spacing=self.hole_pitch,
            direction=Axis.X,
            count2=self.ROWS,
            spacing2=self.hole_pitch,
            direction2=Axis.Y,
        )

        pitch = self.hole_pitch.value
        along_axis = self.SLOT_CENTER_DISTANCE / sqrt(2)

        for name, sx, sy in (
            ("Slot NE", +1, +1),
            ("Slot NW", -1, +1),
            ("Slot SW", -1, -1),
            ("Slot SE", +1, -1),
        ):
            inner_ring = (sx * pitch, sy * pitch)
            inner_outward = (
                sx * (pitch + along_axis),
                sy * (pitch + along_axis),
            )
            outer_ring = (sx * 3 * pitch, sy * 3 * pitch)
            outer_inward = (
                sx * (3 * pitch - along_axis),
                sy * (3 * pitch - along_axis),
            )

            with Sketch(name=name, on=board, parent=Anchor.TOP) as slots:
                SlotCenterToCenter2D(
                    inner_ring,
                    inner_outward,
                    self.SLOT_WIDTH,
                )
                SlotCenterToCenter2D(
                    outer_inward,
                    outer_ring,
                    self.SLOT_WIDTH,
                )

            board = board - slots.extrude(Depth.THROUGH_ALL)

        return board
