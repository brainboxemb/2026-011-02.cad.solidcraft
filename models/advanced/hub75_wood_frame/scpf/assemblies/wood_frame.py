"""Main plywood frame subassembly."""

from scpf import AnchorTopology, assembly, pv

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

        # Semantic frame anchors belong here, not on the generic Board.
        # The references select the vertical outside edges of the side walls.
        # SolidCraft stores that topology, so width/height/thickness edits move
        # the selected edge/corner without Board needing application knowledge.
        t = pv(self.frame_wood_thickness)
        opening_w = pv(self.opening_width)
        opening_h = pv(self.opening_height)
        depth = pv(self.cabinet_depth)

        left_x = -(opening_w / 2 + t)
        right_x = opening_w / 2 + t
        left_mid_x = -(opening_w / 2 + t / 2)
        right_mid_x = opening_w / 2 + t / 2
        bottom_z = t
        top_z = t + opening_h
        mid_z = (bottom_z + top_z) / 2

        def vertical_ref(x, on_x, y, z, frame_z, frame_x):
            return AnchorTopology(
                edge=(x, y, mid_z),
                on=(on_x, y, mid_z),
                corner=(x, y, z),
                z=frame_z,
                x=frame_x,
            )

        for name, target, reference in (
            (
                "front_bottom_left",
                left,
                vertical_ref(
                    left_x, left_mid_x, 0, bottom_z,
                    (0, 0, 1), (1, 0, 0),
                ),
            ),
            (
                "front_top_left",
                left,
                vertical_ref(
                    left_x, left_mid_x, 0, top_z,
                    (0, 0, -1), (1, 0, 0),
                ),
            ),
            (
                "front_bottom_right",
                right,
                vertical_ref(
                    right_x, right_mid_x, 0, bottom_z,
                    (0, 0, 1), (-1, 0, 0),
                ),
            ),
            (
                "front_top_right",
                right,
                vertical_ref(
                    right_x, right_mid_x, 0, top_z,
                    (0, 0, -1), (-1, 0, 0),
                ),
            ),
            (
                "back_bottom_left",
                left,
                vertical_ref(
                    left_x, left_mid_x, depth, bottom_z,
                    (0, 0, 1), (1, 0, 0),
                ),
            ),
            (
                "back_top_left",
                left,
                vertical_ref(
                    left_x, left_mid_x, depth, top_z,
                    (0, 0, -1), (1, 0, 0),
                ),
            ),
            (
                "back_bottom_right",
                right,
                vertical_ref(
                    right_x, right_mid_x, depth, bottom_z,
                    (0, 0, 1), (-1, 0, 0),
                ),
            ),
            (
                "back_top_right",
                right,
                vertical_ref(
                    right_x, right_mid_x, depth, top_z,
                    (0, 0, -1), (-1, 0, 0),
                ),
            ),
        ):
            frame = frame.with_anchor(name, target, reference)

        return frame
