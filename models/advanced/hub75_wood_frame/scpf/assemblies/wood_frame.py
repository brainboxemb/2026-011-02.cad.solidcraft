"""Main plywood frame subassembly."""

from scpf import BOTTOM, LEFT, RIGHT, TOP, assembly

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
            corner_radius=self.corner_radius,
            fillet=(BOTTOM + LEFT, BOTTOM + RIGHT),
            material_name="LIGHTPLY bottom",
        )
        bottom = bottom.move(
            0,
            0,
            0,
        ).group("WoodBoxFrame")

        left = Board(
            name="left",
            width=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.opening_height,
            material_name="LIGHTPLY side board",
        )
        left = left.move(
            -(self.opening_width / 2 + self.frame_wood_thickness / 2),
            0,
            opening_bottom,
        ).group("WoodBoxFrame")

        right = Board(
            name="right",
            width=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.opening_height,
            material_name="LIGHTPLY side board",
        )
        right = right.move(
            self.opening_width / 2 + self.frame_wood_thickness / 2,
            0,
            opening_bottom,
        ).group("WoodBoxFrame")

        roof = Board(
            name="roof",
            width=outer_width,
            depth=roof_rear - roof_front,
            height=self.frame_wood_thickness,
            corner_radius=self.corner_radius,
            fillet=(TOP + LEFT, TOP + RIGHT),
            material_name="LIGHTPLY roof",
        )
        roof = roof.move(
            0,
            roof_front,
            opening_top,
        ).group("WoodBoxFrame")

        rear = Board(
            name="rear",
            width=outer_width,
            depth=self.panel_wood_thickness,
            height=opening_top,
            material_name="LIGHTPLY rear",
            color="#A87D4D",
        )
        rear = rear.move(
            0,
            rear_y,
            0,
        ).group("WoodBoxFrame")

        return left + right + bottom + roof + rear
