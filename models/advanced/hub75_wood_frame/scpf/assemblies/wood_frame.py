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
        opening_bottom = self.frame_wood_thickness
        opening_top = opening_bottom + self.opening_height

        left = LeftBoard(
            thickness=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.opening_height,
            x_position=-(self.opening_width / 2 + self.frame_wood_thickness / 2),
            y_position=0.0,
            z_position=opening_bottom,
        )
        right = RightBoard(
            thickness=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.opening_height,
            x_position=self.opening_width / 2 + self.frame_wood_thickness / 2,
            y_position=0.0,
            z_position=opening_bottom,
        )
        sides = left + right

        bottom = BottomBoard(
            width=outer_width,
            depth=self.cabinet_depth,
            thickness=self.frame_wood_thickness,
            y_position=0.0,
            corner_radius=self.corner_radius,
        )

        roof = RoofBoard(
            width=outer_width,
            depth=roof_rear - roof_front,
            thickness=self.frame_wood_thickness,
            y_position=roof_front,
            z_position=opening_top,
            corner_radius=self.corner_radius,
        )

        rear_board = BackBoard(
            width=outer_width,
            height=opening_top,
            thickness=self.panel_wood_thickness,
            y_position=rear,
        )

        return (sides + bottom + roof + rear_board).group("WoodBoxFrame")
