"""Two vertical roundwood side handles placed in the rear side-wall recesses."""

from scpf import Placement, assembly, half

from parts.handle_ring import HandleRing
from parts.roundwood_handle import RoundwoodHandle


ROD_DIAMETER = 22.0
RING_RADIAL_THICKNESS = 3.0
RING_HEIGHT = 10.0
RING_BORE_CLEARANCE = 0.4


@assembly
class SideHandles:
    """First handle study: only the roundwood, with no mounting hardware."""

    opening_width = 844.0
    opening_height = 362.0
    lower_compartment_height = 70.0
    frame_wood_thickness = 12.0
    side_panel_depth = 110.0

    side_recess_lower_keep = 80.0
    side_recess_upper_keep = 80.0

    def build(self):
        # The side-wall outside face is one full plywood thickness outside
        # the clear opening. Move the Ø22 rod inward until its outside surface
        # is flush with that plywood outside face.
        side_outer_x = (
            half(self.opening_width)
            + self.frame_wood_thickness
        )
        handle_x = (
            side_outer_x
            - half(ROD_DIAMETER)
        )

        # Align the back of the Ø22 rod exactly with the 110 mm rear edge of
        # the side panel. The rod centre therefore sits one radius forward.
        # Default: Y=110 - 11 = 99 mm.
        handle_y = self.side_panel_depth - half(ROD_DIAMETER)

        # Use exactly the same vertical limits as the visible side-wall recess.
        # The rod is shown clamped directly between those two limits. Mounting
        # details are intentionally left out until the ergonomics are right.
        opening_bottom_z = (
            2 * self.frame_wood_thickness
            + self.lower_compartment_height
        )
        recess_bottom_z = (
            opening_bottom_z
            + self.side_recess_lower_keep
        )
        recess_top_z = (
            opening_bottom_z
            + self.opening_height
            - self.side_recess_upper_keep
        )
        rod_length = recess_top_z - recess_bottom_z

        left_rod = RoundwoodHandle(
            name="left_handle_rod",
            diameter=ROD_DIAMETER,
            length=rod_length,
            placement=Placement(
                x=-handle_x,
                y=handle_y,
                z=recess_bottom_z,
            ),
        ).group("SideHandles")

        right_rod = RoundwoodHandle(
            name="right_handle_rod",
            diameter=ROD_DIAMETER,
            length=rod_length,
            placement=Placement(
                x=handle_x,
                y=handle_y,
                z=recess_bottom_z,
            ),
        ).group("SideHandles")

        # The first mounting study adds only simple protective rings. Each
        # 10 mm ring wraps the rod at the lower or upper end; it does not yet
        # connect the handle mechanically to the plywood.
        left_bottom_ring = HandleRing(
            name="left_handle_ring_bottom",
            rod_diameter=ROD_DIAMETER,
            radial_thickness=RING_RADIAL_THICKNESS,
            height=RING_HEIGHT,
            bore_clearance=RING_BORE_CLEARANCE,
            placement=Placement(
                x=-handle_x,
                y=handle_y,
                z=recess_bottom_z,
            ),
        ).group("SideHandles")

        left_top_ring = HandleRing(
            name="left_handle_ring_top",
            rod_diameter=ROD_DIAMETER,
            radial_thickness=RING_RADIAL_THICKNESS,
            height=RING_HEIGHT,
            bore_clearance=RING_BORE_CLEARANCE,
            placement=Placement(
                x=-handle_x,
                y=handle_y,
                z=recess_top_z - RING_HEIGHT,
            ),
        ).group("SideHandles")

        right_bottom_ring = HandleRing(
            name="right_handle_ring_bottom",
            rod_diameter=ROD_DIAMETER,
            radial_thickness=RING_RADIAL_THICKNESS,
            height=RING_HEIGHT,
            bore_clearance=RING_BORE_CLEARANCE,
            placement=Placement(
                x=handle_x,
                y=handle_y,
                z=recess_bottom_z,
            ),
        ).group("SideHandles")

        right_top_ring = HandleRing(
            name="right_handle_ring_top",
            rod_diameter=ROD_DIAMETER,
            radial_thickness=RING_RADIAL_THICKNESS,
            height=RING_HEIGHT,
            bore_clearance=RING_BORE_CLEARANCE,
            placement=Placement(
                x=handle_x,
                y=handle_y,
                z=recess_top_z - RING_HEIGHT,
            ),
        ).group("SideHandles")

        return (
            left_rod
            + right_rod
            + left_bottom_ring
            + left_top_ring
            + right_bottom_ring
            + right_top_ring
        )
