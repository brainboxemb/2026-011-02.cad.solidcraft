"""Eight corner brackets attached outside an existing WoodFrame."""

from scpf import Anchor, AnchorFrame, assembly

from models.components.corner_bracket.scpf.model import CornerBracket


@assembly
class CornerBrackets:
    """Attach brackets around the four outside corners of the side boards."""

    wood_frame = None
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

        # Mounting orientation belongs to this HUB75 assembly, not to the
        # reusable CornerBracket geometry. Read the existing bracket profile
        # dimension; do not introduce a second assembly parameter for it.
        w = CornerBracket.arm_height
        front_mount_a = AnchorFrame(
            origin=(0, 0, -w),
            z=(0, 1, 0),
            x=(0, 0, -1),
        )
        front_mount_b = AnchorFrame(
            origin=(w, 0, 0),
            z=(0, 1, 0),
            x=(0, 0, -1),
        )
        rear_mount_a = AnchorFrame(
            origin=(0, 0, -w),
            z=(0, -1, 0),
            x=(1, 0, 0),
        )
        rear_mount_b = AnchorFrame(
            origin=(w, 0, 0),
            z=(0, -1, 0),
            x=(1, 0, 0),
        )

        gap = -(self.bracket_width / 2)

        top_left_front = bracket.copy().attach(
            left,
            parent=Anchor.FRONT_TOP_LEFT,
            child=front_mount_a,
            gap=gap,
            angle=0,
        )
        top_right_front = bracket.copy().attach(
            right,
            parent=Anchor.FRONT_TOP_RIGHT,
            child=front_mount_b,
            gap=gap,
            angle=0,
        )
        bottom_right_front = bracket.copy().attach(
            right,
            parent=Anchor.FRONT_BOTTOM_RIGHT,
            child=front_mount_a,
            gap=gap,
            angle=0,
        )
        bottom_left_front = bracket.copy().attach(
            left,
            parent=Anchor.FRONT_BOTTOM_LEFT,
            child=front_mount_b,
            gap=gap,
            angle=0,
        )

        top_left_rear = bracket.copy().attach(
            left,
            parent=Anchor.BACK_TOP_LEFT,
            child=rear_mount_a,
            gap=gap,
            angle=0,
        )
        top_right_rear = bracket.copy().attach(
            right,
            parent=Anchor.BACK_TOP_RIGHT,
            child=rear_mount_b,
            gap=gap,
            angle=0,
        )
        bottom_right_rear = bracket.copy().attach(
            right,
            parent=Anchor.BACK_BOTTOM_RIGHT,
            child=rear_mount_a,
            gap=gap,
            angle=0,
        )
        bottom_left_rear = bracket.copy().attach(
            left,
            parent=Anchor.BACK_BOTTOM_LEFT,
            child=rear_mount_b,
            gap=gap,
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
