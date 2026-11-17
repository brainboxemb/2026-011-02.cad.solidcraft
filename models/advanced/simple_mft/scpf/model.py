"""Simple MFT worktop inspired by the Craftmaker S30 replacement top.

The plate envelope and dog-hole diameter follow the published replacement-top
dimensions. The 76 mm pitch, 20 mm corner cuts and clamp-slot dimensions are
photo-based design estimates, not manufacturer dimensions.

The current 2D expectation is calibrated from the front product photo:
- slot width about 24 mm;
- slot end-centre distance about 80 mm, giving about 104 mm overall length;
- per diagonal arm, the inner slot starts on grid ring 1 and extends outward;
- the outer slot starts on grid ring 3 and extends inward;
- the four diagonal grid-ring-2 dog-hole positions are omitted.
"""

from math import sqrt


EXCLUDED_DOG_HOLE_GRID = frozenset({
    (-2, -2),
    (-2, 2),
    (2, -2),
    (2, 2),
})


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

        # Keep a rectangular native base so attached Sketches use the native
        # rectangular face reference supported by SCPF.
        board = Box(
            self.width,
            self.depth,
            self.thickness,
            anchor=Anchor.BOTTOM,
        )

        # Chamfer the four vertical corner edges. An equal 20 mm chamfer on a
        # vertical edge produces the straight 20 x 20 mm plan-view corner cut
        # while retaining the rectangular Box as the anchor base.
        edge_z = self.thickness.value / 2
        board = board.chamfer(
            c,
            edges=[
                (-half_w, -half_d, edge_z),
                (half_w, -half_d, edge_z),
                (half_w, half_d, edge_z),
                (-half_w, half_d, edge_z),
            ],
        )

        # The visible 9 x 7 grid has four missing dog-hole positions on
        # diagonal ring 2. Build the actual hole set directly instead of
        # creating a complete rectangular pattern and adding material back.
        half_columns = self.COLUMNS // 2
        half_rows = self.ROWS // 2
        with Sketch(name="Dog holes", on=board, parent=Anchor.TOP) as holes:
            for row in range(-half_rows, half_rows + 1):
                for column in range(-half_columns, half_columns + 1):
                    if (column, row) in EXCLUDED_DOG_HOLE_GRID:
                        continue
                    holes.add(
                        Circle2D(d=self.hole_diameter),
                        offset=(
                            column * self.hole_pitch,
                            row * self.hole_pitch,
                        ),
                    )

        board = board - holes.extrude(Depth.THROUGH_ALL)

        # SolidCraft 0.42 native Slot creators require fixed numeric points.
        # Read the current parameter values explicitly instead of passing Forge
        # expressions into the Slot command.
        pitch = float(self.hole_pitch.value)
        slot_center_distance = float(self.SLOT_CENTER_DISTANCE)
        slot_width = float(self.SLOT_WIDTH)
        along_axis = slot_center_distance / sqrt(2)

        # All eight clamp Slots belong to one physical cut pattern, so keep
        # them together in one Sketch and one through-cut feature.
        with Sketch(name="Clamp slots", on=board, parent=Anchor.TOP) as slots:
            for sx, sy in (
                (+1, +1),
                (-1, +1),
                (-1, -1),
                (+1, -1),
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

                SlotCenterToCenter2D(
                    inner_ring,
                    inner_outward,
                    slot_width,
                )
                SlotCenterToCenter2D(
                    outer_inward,
                    outer_ring,
                    slot_width,
                )

        board = board - slots.extrude(Depth.THROUGH_ALL)

        return board
