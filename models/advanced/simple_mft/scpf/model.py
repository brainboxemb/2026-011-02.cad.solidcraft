"""Simple MFT worktop inspired by the Craftmaker S30 replacement top.

The plate envelope and dog-hole diameter follow the published replacement-top
dimensions. The 76 mm pitch, 20 mm corner cuts and 24 mm clamp-slot width are
photo/video-based design estimates, not manufacturer dimensions.

The clamp-slot layout is derived from the SolidCraft reference model: each
diagonal arm uses grid positions 1, 2 and 3. Forge 0.6.1 can express that
directly as one native center-to-center Slot from position 1 to position 3,
which passes through the middle grid position.
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
    SLOT_START_INDEX = 1
    SLOT_END_INDEX = 3

    def build(self):
        half_w = self.width / 2
        half_d = self.depth / 2
        c = self.corner_chamfer

        # Eight-point outline: straight corner cuts, not fillets.
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

        # One source hole drives the complete centred 9 x 7 native pattern.
        with Sketch(name="Dog hole", on=board, parent=Anchor.TOP) as hole:
            hole.add(
                Circle2D(d=self.hole_diameter),
                offset=(
                    -4 * self.hole_pitch,
                    -3 * self.hole_pitch,
                ),
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

        # SolidCraft 0.42's direct Slot creators require numeric coordinates.
        # Use the three diagonal grid positions from the reference model as one
        # continuous native Slot: end-cap centres at index 1 and 3, with the
        # index-2 dog-hole centre on the Slot axis.
        pitch = self.hole_pitch.value
        start = self.SLOT_START_INDEX * pitch
        end = self.SLOT_END_INDEX * pitch

        arms = (
            ("Slot NE", +1, +1),
            ("Slot NW", -1, +1),
            ("Slot SW", -1, -1),
            ("Slot SE", +1, -1),
        )

        for name, sx, sy in arms:
            with Sketch(name=name, on=board, parent=Anchor.TOP) as slot:
                SlotCenterToCenter2D(
                    (sx * start, sy * start),
                    (sx * end, sy * end),
                    self.SLOT_WIDTH,
                )

            board = board - slot.extrude(Depth.THROUGH_ALL)

        return board
