"""Eight corner brackets attached to an existing WoodFrame assembly."""

from scpf import Anchor, assembly, component

from models.components.corner_bracket.scpf.model import CornerBracket


Bracket = component(CornerBracket)


@assembly
class CornerBrackets:
    """Attach brackets to the four inside corners of the side boards."""

    wood_frame = None
    bracket_width = 24.0
    corner_radius = 4.0

    def build(self):
        if self.wood_frame is None:
            raise ValueError("CornerBrackets requires wood_frame")

        left = self.wood_frame.left
        right = self.wood_frame.right

        bracket = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
        )

        # The side-board corners define X and Z. The front/rear faces define Y;
        # half the bracket width moves each symmetric bracket fully inside.
        gap = -(self.bracket_width / 2)

        top_left_front = bracket.copy().attach(
            left,
            parent=Anchor.FRONT_TOP_RIGHT,
            child="front_mount",
            gap=gap,
            angle=180,
        )
        top_right_front = bracket.copy().attach(
            right,
            parent=Anchor.FRONT_TOP_LEFT,
            child="front_mount",
            gap=gap,
            angle=0,
        )
        bottom_right_front = bracket.copy().attach(
            right,
            parent=Anchor.FRONT_BOTTOM_LEFT,
            child="front_mount",
            gap=gap,
            angle=180,
        )
        bottom_left_front = bracket.copy().attach(
            left,
            parent=Anchor.FRONT_BOTTOM_RIGHT,
            child="front_mount",
            gap=gap,
            angle=0,
        )

        top_left_rear = bracket.copy().attach(
            left,
            parent=Anchor.BACK_TOP_RIGHT,
            child="rear_mount",
            gap=gap,
            angle=270,
        )
        top_right_rear = bracket.copy().attach(
            right,
            parent=Anchor.BACK_TOP_LEFT,
            child="rear_mount",
            gap=gap,
            angle=90,
        )
        bottom_right_rear = bracket.copy().attach(
            right,
            parent=Anchor.BACK_BOTTOM_LEFT,
            child="rear_mount",
            gap=gap,
            angle=270,
        )
        bottom_left_rear = bracket.copy().attach(
            left,
            parent=Anchor.BACK_BOTTOM_RIGHT,
            child="rear_mount",
            gap=gap,
            angle=90,
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
