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
        #
        # CornerBracket local side profile (XZ), looking along +Y:
        #
        #                    +Z
        #                     ^
        #        +------------+--------------------------+
        #        |            |        horizontal arm   |
        #        |            |                         |
        #        |            I----B--------------------+
        #        |            |    B = (w, 0, 0)
        #        |            |
        #        |            A    A = (0, 0, -w)
        #        |            |
        #        +------------+
        #                     +-------------------------> +X
        #
        # I = the concave inside corner and component origin (0, 0, 0).
        # A and B are NOT points stored by CornerBracket; they are mounting
        # references chosen here by this assembly:
        #
        #   mount_a origin = (0, 0, -w)
        #       one arm_height below I, on the inside edge of the vertical arm.
        #
        #   mount_b origin = (w, 0, 0)
        #       one arm_height right of I, on the inside edge of the
        #       horizontal arm.
        #
        # Both origins have Y=0. The bracket itself is extruded symmetrically
        # over arm_width, so its broad faces are at:
        #
        #             local Y / bracket width
        #
        #        front face       centre        rear face
        #        Y=-arm_width/2    Y=0          Y=+arm_width/2
        #             |             |                 |
        #             +-------------+-----------------+
        #             <--------- arm_width ----------->
        #                           ^
        #                           |
        #                 AnchorFrame.origin
        #
        # The frame normal selects which side is front/rear:
        #
        #   front_mount_*: z = (0, +1, 0)
        #   rear_mount_* : z = (0, -1, 0)
        #
        # The AnchorFrame itself therefore remains on the Y=0 centre plane.
        # gap = -arm_width/2 below offsets the rigid joint along that normal:
        # front -> Y=-arm_width/2, rear -> Y=+arm_width/2.
        #
        # x=... on each AnchorFrame fixes the remaining rotation around the
        # normal. A/B plus the parent corner determine which of the four
        # clock positions the neutral L profile occupies.
        w = CornerBracket.arm_height
        mount_a = AnchorFrame(
            origin=(0, 0, -w),
            z=(0, 1, 0),
            x=(0, 0, -1),
        )
        mount_b = AnchorFrame(
            origin=(w, 0, 0),
            z=(0, 1, 0),
            x=(0, 0, -1),
        )

        # CornerBracket.arm_width is passed from self.bracket_width above.
        # Both mount frames share the same normal. Select the broad face only
        # with the joint gap: front and rear lie on opposite sides of Y=0.
        front_gap = -(self.bracket_width / 2)
        rear_gap = self.bracket_width / 2

        top_left_front = bracket.copy().attach(
            left,
            parent=Anchor.FRONT_TOP_LEFT,
            child=mount_a,
            gap=front_gap,
            angle=0,
        )
        top_right_front = bracket.copy().attach(
            right,
            parent=Anchor.FRONT_TOP_RIGHT,
            child=mount_b,
            gap=front_gap,
            angle=0,
        )
        bottom_right_front = bracket.copy().attach(
            right,
            parent=Anchor.FRONT_BOTTOM_RIGHT,
            child=mount_a,
            gap=front_gap,
            angle=0,
        )
        bottom_left_front = bracket.copy().attach(
            left,
            parent=Anchor.FRONT_BOTTOM_LEFT,
            child=mount_b,
            gap=front_gap,
            angle=0,
        )

        top_left_rear = bracket.copy().attach(
            left,
            parent=Anchor.BACK_TOP_LEFT,
            child=mount_a,
            gap=rear_gap,
            angle=0,
        )
        top_right_rear = bracket.copy().attach(
            right,
            parent=Anchor.BACK_TOP_RIGHT,
            child=mount_b,
            gap=rear_gap,
            angle=0,
        )
        bottom_right_rear = bracket.copy().attach(
            right,
            parent=Anchor.BACK_BOTTOM_RIGHT,
            child=mount_a,
            gap=rear_gap,
            angle=0,
        )
        bottom_left_rear = bracket.copy().attach(
            left,
            parent=Anchor.BACK_BOTTOM_LEFT,
            child=mount_b,
            gap=rear_gap,
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
