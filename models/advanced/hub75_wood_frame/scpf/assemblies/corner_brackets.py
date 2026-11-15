"""Eight corner brackets attached around the four outside WoodFrame corners."""

from scpf import Anchor, AnchorFrame, assembly, half

from models.components.corner_bracket.scpf.model import CornerBracket


@assembly
class CornerBrackets:
    """Attach two brackets along Y at each outside X/Z cabinet corner."""

    wood_frame = None
    bracket_width = 24.0
    corner_radius = 4.0

    def build(self):
        if self.wood_frame is None:
            raise ValueError("CornerBrackets requires wood_frame")

        left_board = self.wood_frame.left
        right_board = self.wood_frame.right

        bracket = CornerBracket(
            arm_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
        )

        # CornerBracket is authored as one neutral L profile in local XZ.
        #
        #                    +Z
        #                     ^
        #        +------------+--------------------------+
        #        |            |        horizontal arm   |
        #        |            |                         |
        #        |            I-------------------------+
        #        |            |
        #        |            | vertical arm
        #        |            |
        #        +------------+
        #                     +-------------------------> +X
        #
        # I=(0,0,0) is the actual concave inside corner. That point must
        # coincide with the wooden cabinet corner. Do not offset the child
        # frame to a point on either arm: doing so makes the bracket float
        # beside the wood instead of wrapping it.
        #
        # The bracket is extruded symmetrically along local Y over
        # bracket_width. Front and rear use the same X/Z corner clocking; only
        # their position along the side-board depth differs.
        #
        # A positive half-width gap places:
        #   front bracket centre at Y=+bracket_width/2
        #   rear  bracket centre at Y=cabinet_depth-bracket_width/2
        #
        # so both brackets lie ON the side board rather than outside the front
        # and rear faces.
        front_mount = AnchorFrame(
            origin=(0, 0, 0),
            z=Anchor.BACK,
            x=Anchor.DOWN,
        )
        rear_mount = AnchorFrame(
            origin=(0, 0, 0),
            z=Anchor.FRONT,
            x=Anchor.RIGHT,
        )
        gap = half(self.bracket_width)

        top_left_front = bracket.copy().attach(
            left_board,
            parent=Anchor.FRONT_TOP_LEFT,
            child=front_mount,
            gap=gap,
        )
        top_right_front = bracket.copy().attach(
            right_board,
            parent=Anchor.FRONT_TOP_RIGHT,
            child=front_mount,
            gap=gap,
        )
        bottom_right_front = bracket.copy().attach(
            right_board,
            parent=Anchor.FRONT_BOTTOM_RIGHT,
            child=front_mount,
            gap=gap,
        )
        bottom_left_front = bracket.copy().attach(
            left_board,
            parent=Anchor.FRONT_BOTTOM_LEFT,
            child=front_mount,
            gap=gap,
        )

        top_left_rear = bracket.copy().attach(
            left_board,
            parent=Anchor.BACK_TOP_LEFT,
            child=rear_mount,
            gap=gap,
        )
        top_right_rear = bracket.copy().attach(
            right_board,
            parent=Anchor.BACK_TOP_RIGHT,
            child=rear_mount,
            gap=gap,
        )
        bottom_right_rear = bracket.copy().attach(
            right_board,
            parent=Anchor.BACK_BOTTOM_RIGHT,
            child=rear_mount,
            gap=gap,
        )
        bottom_left_rear = bracket.copy().attach(
            left_board,
            parent=Anchor.BACK_BOTTOM_LEFT,
            child=rear_mount,
            gap=gap,
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
