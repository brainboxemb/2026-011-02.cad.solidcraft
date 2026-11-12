"""Main plywood frame subassembly."""

from scpf import assembly

from parts.board import BackBoard, BottomBoard, LeftBoard, RightBoard, RoofBoard


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
        rear = self.cabinet_depth
        back_outer = rear + self.panel_wood_thickness
        roof_front = -self.roof_front_overhang
        roof_rear = back_outer + self.roof_rear_overhang
        outer_width = self.opening_width + 2 * self.frame_wood_thickness
        body_y = self.cabinet_depth / 2

        left = LeftBoard(
            thickness=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.opening_height,
        ).move(
            x=-(self.opening_width / 2 + self.frame_wood_thickness / 2),
            y=body_y,
        )
        right = RightBoard(
            thickness=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.opening_height,
        ).move(
            x=self.opening_width / 2 + self.frame_wood_thickness / 2,
            y=body_y,
        )
        sides = left + right

        bottom = BottomBoard(
            width=outer_width,
            depth=self.cabinet_depth,
            thickness=self.frame_wood_thickness,
            corner_radius=self.corner_radius,
        ).move(
            y=body_y,
            z=-self.frame_wood_thickness,
        )

        roof = RoofBoard(
            width=outer_width,
            depth=roof_rear - roof_front,
            thickness=self.frame_wood_thickness,
            corner_radius=self.corner_radius,
        ).move(
            y=(roof_front + roof_rear) / 2,
            z=self.opening_height,
        )

        rear_board = BackBoard(
            width=outer_width,
            height=self.opening_height + self.frame_wood_thickness,
            thickness=self.panel_wood_thickness,
        ).move(
            y=rear + self.panel_wood_thickness / 2,
            z=-self.frame_wood_thickness,
        )

        return (sides + bottom + roof + rear_board).group("WoodBoxFrame")
