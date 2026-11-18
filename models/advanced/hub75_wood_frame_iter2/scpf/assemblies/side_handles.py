"""Two vertical roundwood side handles placed in the rear side-wall recesses."""

from scpf import Placement, assembly, half

from parts.roundwood_handle import RoundwoodHandle


ROD_DIAMETER = 22.0


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
        side_center_x = (
            half(self.opening_width)
            + half(self.frame_wood_thickness)
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

        left = RoundwoodHandle(
            name="left_handle_rod",
            diameter=ROD_DIAMETER,
            length=rod_length,
            placement=Placement(
                x=-side_center_x,
                y=handle_y,
                z=recess_bottom_z,
            ),
        ).group("SideHandles")

        right = RoundwoodHandle(
            name="right_handle_rod",
            diameter=ROD_DIAMETER,
            length=rod_length,
            placement=Placement(
                x=side_center_x,
                y=handle_y,
                z=recess_bottom_z,
            ),
        ).group("SideHandles")

        return left + right
