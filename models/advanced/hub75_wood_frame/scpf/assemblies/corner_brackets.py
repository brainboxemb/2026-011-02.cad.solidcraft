"""Eight corner brackets attached outside an existing WoodFrame."""

from scpf import assembly

from models.components.corner_bracket.scpf.model import CornerBracket


@assembly
class CornerBrackets:
    """Attach brackets around the four outside corners of the side boards."""

    wood_frame = None
    bracket_width = 24.0
    frame_wood_thickness = 12.0
    corner_radius = 4.0

    def build(self):
        if self.wood_frame is None:
            raise ValueError("CornerBrackets requires wood_frame")

        left = self.wood_frame.left
        right = self.wood_frame.right

        bracket = CornerBracket(
            arm_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
        )

        # The board anchors are real SolidCraft edge/corner topology on the
        # side walls. Their Z axis points toward the corresponding outside
        # wood corner. The rigid-joint offset stays symbolic:
        #
        #     side-wall corner
        #            *
        #            |  frame_wood_thickness - corner_radius
        #            |
        #            T  wood fillet tangent
        #
        # The child reference T is the matching intrinsic tangent anchor
        # exposed by CornerBracket. The names describe only local +/-Y
        # geometry; this assembly decides which endpoint becomes front/rear.

        # Both bottom (+Z parent frame) and top (-Z parent frame) use the same
        # negative offset to move from the side-wall corner to the tangent of
        # the convex wooden fillet.
        tangent_gap = -(
            self.frame_wood_thickness - self.corner_radius
        )

        top_left_front = bracket.copy().attach(
            left,
            parent="front_top_left_vertical",
            child="inner_tangent_negative_y",
            gap=tangent_gap,
            angle=0,
        )
        top_right_front = bracket.copy().attach(
            right,
            parent="front_top_right_vertical",
            child="inner_tangent_positive_y",
            gap=tangent_gap,
            angle=0,
        )
        bottom_right_front = bracket.copy().attach(
            right,
            parent="front_bottom_right_vertical",
            child="inner_tangent_negative_y",
            gap=tangent_gap,
            angle=0,
        )
        bottom_left_front = bracket.copy().attach(
            left,
            parent="front_bottom_left_vertical",
            child="inner_tangent_positive_y",
            gap=tangent_gap,
            angle=0,
        )

        top_left_rear = bracket.copy().attach(
            left,
            parent="back_top_left_vertical",
            child="inner_tangent_positive_y",
            gap=tangent_gap,
            angle=0,
        )
        top_right_rear = bracket.copy().attach(
            right,
            parent="back_top_right_vertical",
            child="inner_tangent_negative_y",
            gap=tangent_gap,
            angle=0,
        )
        bottom_right_rear = bracket.copy().attach(
            right,
            parent="back_bottom_right_vertical",
            child="inner_tangent_positive_y",
            gap=tangent_gap,
            angle=0,
        )
        bottom_left_rear = bracket.copy().attach(
            left,
            parent="back_bottom_left_vertical",
            child="inner_tangent_negative_y",
            gap=tangent_gap,
            angle=0,
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
