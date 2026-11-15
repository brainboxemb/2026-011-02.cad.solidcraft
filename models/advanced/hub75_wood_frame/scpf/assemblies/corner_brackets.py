"""Eight corner brackets placed around the four outside cabinet corners."""

from scpf import Placement, X, Y, Z, assembly, half

from models.components.corner_bracket.scpf.model import CornerBracket


@assembly
class CornerBrackets:
    """Place two brackets along Y at each outside X/Z cabinet corner."""

    opening_width = 844.0
    opening_height = 362.0
    frame_wood_thickness = 12.0
    cabinet_depth = 100.0
    bracket_width = 24.0
    corner_radius = 4.0

    def build(self):
        outer_x = half(self.opening_width) + self.frame_wood_thickness
        bottom_z = 0.0
        top_z = self.opening_height + 2 * self.frame_wood_thickness

        front_y = half(self.bracket_width)
        rear_y = self.cabinet_depth - half(self.bracket_width)

        bracket = CornerBracket(
            arm_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
        )

        # CornerBracket is authored as one neutral L profile in local XZ.
        # Its concave inside corner I is the component origin.
        #
        # Neutral profile:
        #
        #                    +Z
        #                     ^
        #        +------------+--------------------------+
        #        |            |        horizontal arm   |
        #        |            |                         |
        #        |            I-------------------------+  +X
        #        |            |
        #        |            | vertical arm
        #        |            |
        #        +------------+
        #
        # I must coincide directly with the exterior convex cabinet corner.
        # The four required X/Z orientations are:
        #
        #   top-left     neutral      +X inward, -Z down
        #   top-right    Z 180°       -X inward, -Z down
        #   bottom-left  X 180°       +X inward, +Z up
        #   bottom-right Y 180°       -X inward, +Z up
        #
        # The bracket extrusion is symmetric around local Y, so these 180°
        # rotations may flip the local extrusion axis without changing the
        # physical front/rear envelope.
        #
        # Front and rear therefore share exactly the same X/Z Placement and
        # differ only in their Y centre:
        #
        #   front: 0 .. bracket_width
        #   rear:  cabinet_depth-bracket_width .. cabinet_depth

        top_left_front = bracket.copy(
            placement=Placement(
                x=-outer_x,
                y=front_y,
                z=top_z,
            ),
        )
        top_left_rear = bracket.copy(
            placement=Placement(
                x=-outer_x,
                y=rear_y,
                z=top_z,
            ),
        )

        top_right_front = bracket.copy(
            placement=Placement(
                x=outer_x,
                y=front_y,
                z=top_z,
                rotation=(Z, 180),
            ),
        )
        top_right_rear = bracket.copy(
            placement=Placement(
                x=outer_x,
                y=rear_y,
                z=top_z,
                rotation=(Z, 180),
            ),
        )

        bottom_left_front = bracket.copy(
            placement=Placement(
                x=-outer_x,
                y=front_y,
                z=bottom_z,
                rotation=(X, 180),
            ),
        )
        bottom_left_rear = bracket.copy(
            placement=Placement(
                x=-outer_x,
                y=rear_y,
                z=bottom_z,
                rotation=(X, 180),
            ),
        )

        bottom_right_front = bracket.copy(
            placement=Placement(
                x=outer_x,
                y=front_y,
                z=bottom_z,
                rotation=(Y, 180),
            ),
        )
        bottom_right_rear = bracket.copy(
            placement=Placement(
                x=outer_x,
                y=rear_y,
                z=bottom_z,
                rotation=(Y, 180),
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
