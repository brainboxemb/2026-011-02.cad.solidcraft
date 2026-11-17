"""Simple MFT worktop — plate and standard dog-hole grid only.

The 805 x 555 x 18 mm plate and 20 mm hole diameter use the chosen worktop
envelope. The hole layout is our centred 96 mm MFT grid, not a claim about
the measured Craftmaker S30 hole positions.
"""


class SimpleMFT:
    width = 805.0
    depth = 555.0
    thickness = 18.0
    hole_diameter = 20.0
    hole_pitch = 96.0

    COLUMNS = 7
    ROWS = 5

    def build(self):
        board = Box(
            self.width,
            self.depth,
            self.thickness,
            anchor=Anchor.BOTTOM,
        )

        # One source hole at the lower-left grid position. Its offset remains
        # linked to the 96 mm pitch so the full 7 x 5 pattern stays centred.
        with Sketch(
            name="Dog hole",
            on=board,
            parent=Anchor.TOP,
        ) as hole:
            hole.add(
                Circle2D(d=self.hole_diameter),
                offset=(
                    -3 * self.hole_pitch,
                    -2 * self.hole_pitch,
                ),
            )

        source_cut = hole.extrude(Depth.THROUGH_ALL)
        board = board - source_cut

        return board.rectangular_pattern(
            source_cut,
            count=self.COLUMNS,
            spacing=self.hole_pitch,
            direction=Axis.X,
            count2=self.ROWS,
            spacing2=self.hole_pitch,
            direction2=Axis.Y,
        )
