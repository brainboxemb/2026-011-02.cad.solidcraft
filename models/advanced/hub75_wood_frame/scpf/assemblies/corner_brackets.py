"""Eight corner brackets attached outside an existing WoodFrame."""

from scpf import AnchorTopology, assembly, pv

from models.components.corner_bracket.scpf.model import CornerBracket


@assembly
class CornerBrackets:
    """Attach brackets around the four outside corners of the side boards."""

    wood_frame = None
    frame_wood_thickness = 12.0
    bracket_width = 24.0
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

        # The wooden corner and the bracket share the same corner radius.
        #
        # Side view in XZ, shown for a bottom corner:
        #
        #          side board
        #              |
        #              |  parent topology corner
        #              P  z = frame_wood_thickness
        #              |
        #              |  gap = frame_wood_thickness - corner_radius
        #              v
        #              T)  wood fillet tangent
        #            _/     z = corner_radius
        #     ______/
        #
        # The parent P stays on real side-board topology. SolidCraft keeps that
        # edge/corner reference when the board changes size. The native rigid
        # joint gap moves from P to tangent T and remains the parameter
        # expression "frame_wood_thickness - corner_radius".
        #
        # The child reference is the matching tangent point on the bracket's
        # inner fillet. It is selected from the straight inner vertical edge
        # on the broad front/rear face. Because this is also topology-backed,
        # changing bracket arm_width or inside_corner_radius moves the joint
        # with the corresponding face/edge instead of freezing an XYZ point.
        radius = pv(self.corner_radius)
        arm_width = pv(self.bracket_width)
        arm_height = CornerBracket.arm_height
        vertical_length = CornerBracket.vertical_arm_length

        edge_z = -(radius + vertical_length) / 2
        tangent_z = -radius
        on_x = -arm_height / 2

        def bracket_tangent(y):
            return AnchorTopology(
                edge=(0, y, edge_z),
                on=(on_x, y, edge_z),
                corner=(0, y, tangent_z),
                # -Z follows the straight inner vertical edge. SolidCraft
                # derives the in-plane frame axis from this edge/corner
                # topology; the joint angle below selects the left/right
                # clock orientation.
                z=(0, 0, -1),
            )

        front_tangent = bracket_tangent(-arm_width / 2)
        rear_tangent = bracket_tangent(arm_width / 2)

        tangent_gap = self.frame_wood_thickness - self.corner_radius

        # The topology frame fixes the tangent point and vertical normal.
        # The remaining clock orientation is a native joint turn:
        #
        #   left  corners: 180 deg
        #   right corners:   0 deg
        #
        # Which broad-face tangent is referenced depends on the clock
        # position. This keeps front brackets at Y=-arm_width..0 and rear
        # brackets at Y=cabinet_depth-arm_width..cabinet_depth without a
        # separate Y gap.
        top_left_front = bracket.copy().attach(
            left,
            parent="top_front_left",
            child=rear_tangent,
            gap=tangent_gap,
            angle=180,
        )
        top_right_front = bracket.copy().attach(
            right,
            parent="top_front_right",
            child=front_tangent,
            gap=tangent_gap,
            angle=0,
        )
        bottom_right_front = bracket.copy().attach(
            right,
            parent="bottom_front_right",
            child=rear_tangent,
            gap=tangent_gap,
            angle=0,
        )
        bottom_left_front = bracket.copy().attach(
            left,
            parent="bottom_front_left",
            child=front_tangent,
            gap=tangent_gap,
            angle=180,
        )

        top_left_rear = bracket.copy().attach(
            left,
            parent="top_back_left",
            child=rear_tangent,
            gap=tangent_gap,
            angle=180,
        )
        top_right_rear = bracket.copy().attach(
            right,
            parent="top_back_right",
            child=front_tangent,
            gap=tangent_gap,
            angle=0,
        )
        bottom_right_rear = bracket.copy().attach(
            right,
            parent="bottom_back_right",
            child=rear_tangent,
            gap=tangent_gap,
            angle=0,
        )
        bottom_left_rear = bracket.copy().attach(
            left,
            parent="bottom_back_left",
            child=front_tangent,
            gap=tangent_gap,
            angle=180,
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
