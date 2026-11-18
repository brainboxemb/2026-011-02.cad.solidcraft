"""Main plywood frame subassembly."""

from scpf import BOTTOM, LEFT, RIGHT, TOP, Placement, assembly, half

from parts.board import Board
from parts.side_board import SideBoard


# Fixed lower-compartment layout. These are product-layout constants rather
# than editable CAD parameters: the clear bays are 30% / 40% / 30%.
LOWER_SIDE_BAY_FRACTION = 0.30
LOWER_CENTER_BAY_FRACTION = 0.40


@assembly
class WoodFrame:
    opening_width = 844.0
    opening_height = 362.0
    lower_compartment_height = 70.0
    frame_wood_thickness = 12.0
    panel_wood_thickness = 9.0
    cabinet_depth = 120.0
    side_panel_depth = 120.0
    roof_front_overhang = 10.0
    roof_rear_overhang = 1.0
    corner_radius = 4.0

    # Rear recess in the display section of both side walls.
    side_recess_depth = 50.0
    side_recess_radius = 20.0
    side_recess_lower_keep = 80.0
    side_recess_upper_keep = 80.0

    def build(self):
        # The future 9 mm rear board will sit inside the 120 mm cabinet depth
        # and between the side walls. Flush with the rear edge, it occupies
        # Y=111..120 instead of adding another 9 mm behind the cabinet.
        rear_y = self.cabinet_depth - self.panel_wood_thickness
        roof_front = -self.roof_front_overhang

        # The roof follows the cabinet rear edge directly. With 10 mm front
        # overhang and 1 mm rear overhang its total depth is 131 mm.
        roof_rear = self.side_panel_depth + self.roof_rear_overhang
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

        # The lower storage section remains full depth. The rear recess starts
        # only after 80 mm of full-depth side wall above the intermediate shelf
        # and stops 80 mm before the roof. These distances are measured inside
        # the SideBoard's local Z system, whose bottom is the top of the bottom
        # board.
        shelf_top_local = (
            self.lower_compartment_height
            + self.frame_wood_thickness
        )
        side_recess_bottom = (
            shelf_top_local
            + self.side_recess_lower_keep
        )
        side_recess_top = (
            side_height
            - self.side_recess_upper_keep
        )

        # Two 12 mm dividers split the clear lower-compartment space into
        # 30% / 40% / 30% visible bays. First remove both divider thicknesses,
        # then apply the fractions to the remaining clear bay width. This keeps
        # the visible openings in the requested ratio rather than merely placing
        # divider centre-lines at 30% and 70% of the cabinet width.
        clear_bay_width = (
            self.opening_width
            - 2 * self.frame_wood_thickness
        )
        side_bay_width = clear_bay_width * LOWER_SIDE_BAY_FRACTION
        center_bay_width = clear_bay_width * LOWER_CENTER_BAY_FRACTION
        divider_offset = (
            half(self.opening_width)
            - side_bay_width
            - half(self.frame_wood_thickness)
        )

        bottom = Board(
            name="bottom",
            width=outer_width,
            depth=self.side_panel_depth,
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
            depth=self.side_panel_depth,
            height=self.frame_wood_thickness,
            material_name="LIGHTPLY intermediate shelf",
            placement=Placement(z=shelf_bottom),
        ).group("WoodBoxFrame")

        lower_divider_left = Board(
            name="lower_divider_left",
            width=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.lower_compartment_height,
            material_name="LIGHTPLY lower divider",
            placement=Placement(
                x=-divider_offset,
                z=bottom_top,
            ),
        ).group("WoodBoxFrame")

        lower_divider_right = Board(
            name="lower_divider_right",
            width=self.frame_wood_thickness,
            depth=self.cabinet_depth,
            height=self.lower_compartment_height,
            material_name="LIGHTPLY lower divider",
            placement=Placement(
                x=divider_offset,
                z=bottom_top,
            ),
        ).group("WoodBoxFrame")

        left = SideBoard(
            name="left",
            thickness=self.frame_wood_thickness,
            depth=self.side_panel_depth,
            height=side_height,
            recess_depth=self.side_recess_depth,
            recess_radius=self.side_recess_radius,
            recess_bottom=side_recess_bottom,
            recess_top=side_recess_top,
            placement=Placement(
                x=-side_center_x,
                z=bottom_top,
            ),
        ).group("WoodBoxFrame")

        right = SideBoard(
            name="right",
            thickness=self.frame_wood_thickness,
            depth=self.side_panel_depth,
            height=side_height,
            recess_depth=self.side_recess_depth,
            recess_radius=self.side_recess_radius,
            recess_bottom=side_recess_bottom,
            recess_top=side_recess_top,
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

        # Rear board is intentionally disabled for the current iteration-2
        # layout work. Keep the definition here so it can be restored once the
        # lower-compartment and rear-access design is decided.
        #
        # rear = Board(
        #     name="rear",
        #     # The rear board fits between the side walls rather than covering
        #     # their rear edges, so its width is the clear opening width.
        #     width=self.opening_width,
        #     depth=self.panel_wood_thickness,
        #     height=opening_top,
        #     material_name="LIGHTPLY rear",
        #     color="#A87D4D",
        #     placement=Placement(y=rear_y),
        # ).group("WoodBoxFrame")

        return (
            left
            + right
            + bottom
            + shelf
            + lower_divider_left
            + lower_divider_right
            + roof
        )
