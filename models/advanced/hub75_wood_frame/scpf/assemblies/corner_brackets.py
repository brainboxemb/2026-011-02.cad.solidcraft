"""Eight explicit placements of one reusable printed corner bracket."""

from scpf import Placement, Y, assembly, half

from models.components.corner_bracket.scpf.model import CornerBracket


@assembly
class CornerBrackets:
    """Place brackets around the four outside corners of the wooden cabinet."""

    opening_width = 844.0
    opening_height = 362.0
    frame_wood_thickness = 12.0
    cabinet_depth = 100.0
    bracket_width = 24.0
    corner_radius = 4.0

    def build(self):
        # This deliberately uses explicit occurrence Placement rather than
        # AnchorFrame/attach. AnchorFrame has a known regression in the current
        # Forge/SolidCraft path and is not required to describe these eight
        # cabinet-corner poses.
        outer_half = half(self.opening_width) + self.frame_wood_thickness
        top_z = self.opening_height + 2 * self.frame_wood_thickness
        front_y = half(self.bracket_width)
        rear_y = self.cabinet_depth - half(self.bracket_width)

        # CornerBracket is modelled once in its neutral top-left orientation.
        # Seen from the front, the four cabinet corners are quarter-turns
        # around Y: 0, 90, 180 and 270 degrees.
        top_left_front = CornerBracket(
            arm_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
            placement=Placement(
                x=-outer_half,
                y=front_y,
                z=top_z,
            ),
        )

        top_left_rear = top_left_front.copy(
            placement=Placement(
                x=-outer_half,
                y=rear_y,
                z=top_z,
            ),
        )

        top_right_front = top_left_front.copy(
            placement=Placement(
                x=outer_half,
                y=front_y,
                z=top_z,
                rotation=(Y, 90),
            ),
        )
        top_right_rear = top_left_front.copy(
            placement=Placement(
                x=outer_half,
                y=rear_y,
                z=top_z,
                rotation=(Y, 90),
            ),
        )

        bottom_right_front = top_left_front.copy(
            placement=Placement(
                x=outer_half,
                y=front_y,
                z=0,
                rotation=(Y, 180),
            ),
        )
        bottom_right_rear = top_left_front.copy(
            placement=Placement(
                x=outer_half,
                y=rear_y,
                z=0,
                rotation=(Y, 180),
            ),
        )

        bottom_left_front = top_left_front.copy(
            placement=Placement(
                x=-outer_half,
                y=front_y,
                z=0,
                rotation=(Y, 270),
            ),
        )
        bottom_left_rear = top_left_front.copy(
            placement=Placement(
                x=-outer_half,
                y=rear_y,
                z=0,
                rotation=(Y, 270),
            ),
        )

        return (
            top_left_front
            + top_left_rear
            + top_right_front
            + top_right_rear
            + bottom_right_front
            + bottom_right_rear
            + bottom_left_front
            + bottom_left_rear
        ).group("CornerBrackets")
