"""Main plywood frame subassembly."""

from scpf import BACK, BOTTOM, FRONT, LEFT, RIGHT, TOP, assembly

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
        outer_width = self.opening_width + 2 * self.frame_wood_thickness
        roof_depth = (
            self.roof_front_overhang
            + self.cabinet_depth
            + self.panel_wood_thickness
            + self.roof_rear_overhang
        )

        bottom = Board(
            name="bottom",
            width=outer_width,
            depth=self.cabinet_depth,
            height=self.frame_wood_thickness,
            corner_radius=self.corner_radius,
            fillet=(BOTTOM + LEFT, BOTTOM + RIGHT),
            material_name="LIGHTPLY bottom",
        )
        bottom = bottom.group("WoodBoxFrame")

        left = Board(
            name="left",
            width=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.opening_height,
            material_name="LIGHTPLY side board",
        )
        left = left.attach(
            bottom,
            parent=FRONT + TOP + LEFT,
            child=FRONT + BOTTOM + LEFT,
        )
        left = left.group("WoodBoxFrame")

        right = Board(
            name="right",
            width=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.opening_height,
            material_name="LIGHTPLY side board",
        )
        right = right.attach(
            bottom,
            parent=FRONT + TOP + RIGHT,
            child=FRONT + BOTTOM + RIGHT,
        )
        right = right.group("WoodBoxFrame")

        roof = Board(
            name="roof",
            width=outer_width,
            depth=roof_depth,
            height=self.frame_wood_thickness,
            corner_radius=self.corner_radius,
            fillet=(TOP + LEFT, TOP + RIGHT),
            material_name="LIGHTPLY roof",
        )
        roof = roof.attach(
            left,
            parent=FRONT + TOP + LEFT,
            child=FRONT + BOTTOM + LEFT,
            gap=self.roof_front_overhang,
        )
        roof = roof.group("WoodBoxFrame")

        rear = Board(
            name="rear",
            width=outer_width,
            depth=self.panel_wood_thickness,
            height=self.frame_wood_thickness + self.opening_height,
            material_name="LIGHTPLY rear",
            color="#A87D4D",
        )
        rear = rear.attach(
            bottom,
            parent=BACK + BOTTOM + LEFT,
            child=FRONT + BOTTOM + LEFT,
        )
        rear = rear.group("WoodBoxFrame")

        return left + right + bottom + roof + rear
