"""Main plywood frame subassembly."""

from scpf import Anchor, assembly

from parts.board import Board


@assembly
class WoodFrame:
    opening_width = 844.0
    opening_height = 362.0
    frame_wood_thickness = 12.0
    panel_wood_thickness = 9.0
    cabinet_depth = 100.0
    roof_front_overhang = 10.0
    roof_rear_overhang = 1.0
    corner_radius = 4.0

    def build(self):
        rear_y = self.cabinet_depth
        back_outer = rear_y + self.panel_wood_thickness
        roof_front = -self.roof_front_overhang
        roof_rear = back_outer + self.roof_rear_overhang
        outer_width = self.opening_width + 2 * self.frame_wood_thickness
        opening_bottom = self.frame_wood_thickness
        opening_top = opening_bottom + self.opening_height

        bottom = Board(
            name="bottom",
            width=outer_width,
            depth=self.cabinet_depth,
            height=self.frame_wood_thickness,
            y_position=0.0,
            corner_radius=self.corner_radius,
            fillet="bottom",
            material_name="LIGHTPLY bottom",
        ).group("WoodBoxFrame")

        left = Board(
            name="left",
            width=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.opening_height,
            x_position=-(
                self.opening_width / 2
                + self.frame_wood_thickness / 2
            ),
            y_position=0.0,
            z_position=opening_bottom,
            material_name="LIGHTPLY side board",
        ).attach(
            bottom,
            as_built=True,
        ).group("WoodBoxFrame")

        right = Board(
            name="right",
            width=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.opening_height,
            x_position=(
                self.opening_width / 2
                + self.frame_wood_thickness / 2
            ),
            y_position=0.0,
            z_position=opening_bottom,
            material_name="LIGHTPLY side board",
        ).attach(
            bottom,
            as_built=True,
        ).group("WoodBoxFrame")


        roof = Board(
            name="roof",
            width=outer_width,
            depth=roof_rear - roof_front,
            height=self.frame_wood_thickness,
            y_position=roof_front,
            z_position=opening_top,
            corner_radius=self.corner_radius,
            fillet="top",
            material_name="LIGHTPLY roof",
        ).group("WoodBoxFrame")

        rear = Board(
            name="rear",
            width=outer_width,
            depth=self.panel_wood_thickness,
            height=opening_top,
            y_position=rear_y,
            material_name="LIGHTPLY rear",
            color="#A87D4D",
        ).group("WoodBoxFrame")

        frame = left + right + bottom + roof + rear

        # These semantic anchors belong to WoodFrame, not to generic Board.
        # Start at the actual top/bottom corner of each side board. The
        # second in-plane joint axis follows that vertical edge toward the
        # board interior, so a negative offset moves from the side-board edge
        # outward by exactly one frame wood thickness.
        #
        #              top outside datum
        #                    *
        #                    |  frame_wood_thickness
        # side-board top     *
        #                    |
        #                    |
        # side-board bottom  *
        #                    |  frame_wood_thickness
        #                    *
        #             bottom outside datum
        #
        # Keep this symbolic: SolidCraft re-evaluates the planar joint offset
        # when frame_wood_thickness changes in the saved design.
        outside_offset = (0, -self.frame_wood_thickness)

        for name, target, reference in (
            ("front_top_left", left, Anchor.FRONT_TOP_LEFT),
            ("front_bottom_left", left, Anchor.FRONT_BOTTOM_LEFT),
            ("front_top_right", right, Anchor.FRONT_TOP_RIGHT),
            ("front_bottom_right", right, Anchor.FRONT_BOTTOM_RIGHT),
            ("back_top_left", left, Anchor.BACK_TOP_LEFT),
            ("back_bottom_left", left, Anchor.BACK_BOTTOM_LEFT),
            ("back_top_right", right, Anchor.BACK_TOP_RIGHT),
            ("back_bottom_right", right, Anchor.BACK_BOTTOM_RIGHT),
        ):
            frame = frame.with_anchor(
                name,
                target,
                reference,
                offset=outside_offset,
            )

        return frame
