"""Main plywood frame subassembly."""

from scpf import BOTTOM, LEFT, RIGHT, TOP, Placement, assembly, half

from parts.board import Board


@assembly
class WoodFrame:
    opening_width = 844.0
    opening_height = 362.0
    lower_compartment_height = 70.0
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

        bottom_top = self.frame_wood_thickness
        shelf_bottom = bottom_top + self.lower_compartment_height
        opening_bottom = shelf_bottom + self.frame_wood_thickness
        opening_top = opening_bottom + self.opening_height

        # The side boards sit on the bottom board and run continuously to the
        # underside of the roof. This includes the lower compartment, the
        # intermediate shelf thickness and the display opening.
        side_height = (
            self.lower_compartment_height
            + self.frame_wood_thickness
            + self.opening_height
        )
        side_center_x = (
            half(self.opening_width)
            + half(self.frame_wood_thickness)
        )

        bottom = Board(
            name="bottom",
            width=outer_width,
            depth=self.cabinet_depth,
            height=self.frame_wood_thickness,
            corner_radius=self.corner_radius,
            fillet=(BOTTOM + LEFT, BOTTOM + RIGHT),
            material_name="LIGHTPLY bottom",
            placement=Placement(),
        ).group("WoodBoxFrame")

        shelf = Board(
            name="intermediate_shelf",
            # The shelf sits between the two side walls. Using outer_width
            # here would make the shelf pass through both 12 mm side boards.
            # Grooves can be added later as explicit joinery features.
            width=self.opening_width,
            depth=self.cabinet_depth,
            height=self.frame_wood_thickness,
            material_name="LIGHTPLY intermediate shelf",
            placement=Placement(z=shelf_bottom),
        ).group("WoodBoxFrame")

        left = Board(
            name="left",
            width=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=side_height,
            material_name="LIGHTPLY side board",
            placement=Placement(
                x=-side_center_x,
                z=bottom_top,
            ),
        ).group("WoodBoxFrame")

        right = Board(
            name="right",
            width=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=side_height,
            material_name="LIGHTPLY side board",
            placement=Placement(
                x=side_center_x,
                z=bottom_top,
            ),
        ).group("WoodBoxFrame")

        roof = Board(
            name="roof",
            width=outer_width,
            depth=roof_rear - roof_front,
            height=self.frame_wood_thickness,
            corner_radius=self.corner_radius,
            fillet=(TOP + LEFT, TOP + RIGHT),
            material_name="LIGHTPLY roof",
            placement=Placement(
                y=roof_front,
                z=opening_top,
            ),
        ).group("WoodBoxFrame")

        rear = Board(
            name="rear",
            width=outer_width,
            depth=self.panel_wood_thickness,
            height=opening_top,
            material_name="LIGHTPLY rear",
            color="#A87D4D",
            placement=Placement(y=rear_y),
        ).group("WoodBoxFrame")

        return left + right + bottom + shelf + roof + rear
