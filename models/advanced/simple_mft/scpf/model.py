"""Simple MFT worktop inspired by the Craftmaker S30 replacement top.

The plate envelope and dog-hole diameter follow the published replacement-top
dimensions. The 76 mm pitch, 20 mm corner cuts and 75 x 24 mm clamp slots are
photo/video-based design estimates, not manufacturer dimensions.
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
    SLOT_LENGTH = 75.0
    SLOT_INNER_INDEX = 2
    SLOT_COUNT_PER_ARM = 2

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

        # SolidCraft 0.42's native Slot creator currently requires numeric
        # coordinates. Four master slots are placed at grid index 2; each is
        # patterned one grid step outward along its arm. This keeps the eight
        # slots as four native two-instance patterns rather than eight manually
        # positioned cuts.
        pitch = self.hole_pitch.value
        inner = self.SLOT_INNER_INDEX * pitch
        half_axis = (self.SLOT_LENGTH - self.SLOT_WIDTH) / (2 * sqrt(2))
        diagonal_step = pitch * sqrt(2)

        arms = (
            ("Slot NE", +inner, +inner, +1, +1),
            ("Slot NW", -inner, +inner, -1, +1),
            ("Slot SW", -inner, -inner, -1, -1),
            ("Slot SE", +inner, -inner, +1, -1),
        )

        for name, cx, cy, sx, sy in arms:
            # Slot axis follows the radial X arm: NW/SE use \\, NE/SW use /.
            dx = sx * half_axis
            dy = sy * half_axis
            with Sketch(name=name, on=board, parent=Anchor.TOP) as slot:
                SlotOverall2D(
                    (cx - dx, cy - dy),
                    (cx + dx, cy + dy),
                    self.SLOT_WIDTH,
                )

            slot_cut = slot.extrude(Depth.THROUGH_ALL)
            board = board - slot_cut
            board = board.rectangular_pattern(
                slot_cut,
                count=self.SLOT_COUNT_PER_ARM,
                spacing=diagonal_step,
                direction=(sx / sqrt(2), sy / sqrt(2), 0),
            )

        return board
