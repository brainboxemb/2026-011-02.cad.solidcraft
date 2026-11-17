"""Simple MFT worktop inspired by the Craftmaker S30 replacement top.

The plate envelope and dog-hole diameter follow the published replacement-top
dimensions. The 76 mm pitch, 20 mm corner cuts and 24 mm clamp-slot width are
photo/video-based design estimates, not manufacturer dimensions.

The expected clamp layout uses three diagonal dog-hole positions per arm with
two native Slot segments: grid index 1 -> 2 and grid index 2 -> 3. There is no
slot from the plate centre to grid index 1.
"""


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
                (-half_w, half_d - c),
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
        for name, sx, sy in (
            ("Slot NE", +1, +1),
            ("Slot NW", -1, +1),
            ("Slot SW", -1, -1),
            ("Slot SE", +1, -1),
        ):
            with Sketch(name=name, on=board, parent=Anchor.TOP) as slots:
                SlotCenterToCenter2D(
                    (sx * pitch, sy * pitch),
                    (sx * 2 * pitch, sy * 2 * pitch),
                    self.SLOT_WIDTH,
                )
                SlotCenterToCenter2D(
                    (sx * 2 * pitch, sy * 2 * pitch),
                    (sx * 3 * pitch, sy * 3 * pitch),
                    self.SLOT_WIDTH,
                )

            board = board - slots.extrude(Depth.THROUGH_ALL)

        return board
