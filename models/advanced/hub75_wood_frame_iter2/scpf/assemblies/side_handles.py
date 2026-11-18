"""Two vertical roundwood side handles placed in the rear side-wall recesses."""

from scpf import Placement, assembly, half

from parts.roundwood_handle import RoundwoodHandle
from parts.side_handle_socket import SideHandleSocket


# Concept dimensions. These stay fixed until the handle position has been
# checked visually in the complete cabinet.
ROD_DIAMETER = 22.0
SOCKET_OUTER_DIAMETER = 34.0
SOCKET_HEIGHT = 24.0
SOCKET_BORE_CLEARANCE = 0.6
SOCKET_EDGE_INSET = 8.0
ROD_SOCKET_INSERT = 8.0


@assembly
class SideHandles:
    opening_width = 844.0
    opening_height = 362.0
    lower_compartment_height = 70.0
    frame_wood_thickness = 12.0
    cabinet_depth = 100.0

    side_recess_depth = 50.0
    side_recess_lower_keep = 80.0
    side_recess_upper_keep = 80.0

    def build(self):
        side_center_x = (
            half(self.opening_width)
            + half(self.frame_wood_thickness)
        )

        # The handle sits exactly halfway through the 50 mm rear recess.
        # Default geometry: recessed plywood edge Y=50, rear edge Y=100,
        # therefore the Ø22 handle centre is Y=75.
        recessed_edge_y = self.cabinet_depth - self.side_recess_depth
        handle_y = recessed_edge_y + half(self.side_recess_depth)
        bridge_depth = (
            handle_y
            - recessed_edge_y
            - half(SOCKET_OUTER_DIAMETER)
        )

        # Use the same vertical reference planes as the SideBoard profile.
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

        # Keep both sockets fully inside the visible recess for this concept.
        # The rod overlaps each socket by 8 mm, so its ends disappear naturally
        # inside the printed sleeves.
        bottom_socket_z = recess_bottom_z + SOCKET_EDGE_INSET
        top_socket_z = (
            recess_top_z
            - SOCKET_EDGE_INSET
            - SOCKET_HEIGHT
        )
        rod_bottom_z = (
            bottom_socket_z
            + SOCKET_HEIGHT
            - ROD_SOCKET_INSERT
        )
        rod_top_z = top_socket_z + ROD_SOCKET_INSERT
        rod_length = rod_top_z - rod_bottom_z

        result = None
        for side_name, side_x in (
            ("left", -side_center_x),
            ("right", side_center_x),
        ):
            bottom_socket = SideHandleSocket(
                name=f"{side_name}_handle_socket_bottom",
                panel_thickness=self.frame_wood_thickness,
                rod_diameter=ROD_DIAMETER,
                outer_diameter=SOCKET_OUTER_DIAMETER,
                height=SOCKET_HEIGHT,
                bridge_depth=bridge_depth,
                bore_clearance=SOCKET_BORE_CLEARANCE,
                placement=Placement(
                    x=side_x,
                    y=handle_y,
                    z=bottom_socket_z,
                ),
            ).group("SideHandles")

            top_socket = SideHandleSocket(
                name=f"{side_name}_handle_socket_top",
                panel_thickness=self.frame_wood_thickness,
                rod_diameter=ROD_DIAMETER,
                outer_diameter=SOCKET_OUTER_DIAMETER,
                height=SOCKET_HEIGHT,
                bridge_depth=bridge_depth,
                bore_clearance=SOCKET_BORE_CLEARANCE,
                placement=Placement(
                    x=side_x,
                    y=handle_y,
                    z=top_socket_z,
                ),
            ).group("SideHandles")

            rod = RoundwoodHandle(
                name=f"{side_name}_handle_rod",
                diameter=ROD_DIAMETER,
                length=rod_length,
                placement=Placement(
                    x=side_x,
                    y=handle_y,
                    z=rod_bottom_z,
                ),
            ).group("SideHandles")

            side_result = bottom_socket + top_socket + rod
            result = side_result if result is None else result + side_result

        return result
