"""Eight corner brackets attached outside an existing WoodFrame."""

from scpf import AnchorFrame, assembly

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

        # CornerBracket.arm_width is passed from self.bracket_width above.
        # Keep the joint on the broad bracket face rather than its Y=0 centre.
        gap = -(self.bracket_width / 2)

        # WoodFrame moves each semantic parent anchor one wood thickness
        # outward from the side-board edge. The bracket needs only this fixed
        # local Z correction: its mounting reference is arm_height away from
        # the neutral L-profile origin. At the default 12 mm wood thickness
        # the two corrections cancel; changing the wood thickness leaves this
        # bracket correction fixed while the WoodFrame offset stays symbolic.
        bracket_z_correction = CornerBracket.arm_height

        def parent_anchor(name):
            anchor = self.wood_frame.anchor(name)
            return anchor, (
                anchor.offset[0],
                anchor.offset[1] + bracket_z_correction,
            )

        top_left_front_anchor, top_left_front_offset = parent_anchor("front_top_left")
        top_left_front = bracket.copy().attach(
            top_left_front_anchor.target,
            parent=top_left_front_anchor.reference,
            child=front_mount_a,
            offset=top_left_front_offset,
            gap=gap,
            angle=0,
        )
        top_right_front_anchor, top_right_front_offset = parent_anchor("front_top_right")
        top_right_front = bracket.copy().attach(
            top_right_front_anchor.target,
            parent=top_right_front_anchor.reference,
            child=front_mount_b,
            offset=top_right_front_offset,
            gap=gap,
            angle=0,
        )
        bottom_right_front_anchor, bottom_right_front_offset = parent_anchor("front_bottom_right")
        bottom_right_front = bracket.copy().attach(
            bottom_right_front_anchor.target,
            parent=bottom_right_front_anchor.reference,
            child=front_mount_a,
            offset=bottom_right_front_offset,
            gap=gap,
            angle=180,
        )
        bottom_left_front_anchor, bottom_left_front_offset = parent_anchor("front_bottom_left")
        bottom_left_front = bracket.copy().attach(
            bottom_left_front_anchor.target,
            parent=bottom_left_front_anchor.reference,
            child=front_mount_b,
            offset=bottom_left_front_offset,
            gap=gap,
            angle=0,
        )

        top_left_rear_anchor, top_left_rear_offset = parent_anchor("back_top_left")
        top_left_rear = bracket.copy().attach(
            top_left_rear_anchor.target,
            parent=top_left_rear_anchor.reference,
            child=rear_mount_a,
            offset=top_left_rear_offset,
            gap=gap,
            angle=0,
        )
        top_right_rear_anchor, top_right_rear_offset = parent_anchor("back_top_right")
        top_right_rear = bracket.copy().attach(
            top_right_rear_anchor.target,
            parent=top_right_rear_anchor.reference,
            child=rear_mount_b,
            offset=top_right_rear_offset,
            gap=gap,
            angle=0,
        )
        bottom_right_rear_anchor, bottom_right_rear_offset = parent_anchor("back_bottom_right")
        bottom_right_rear = bracket.copy().attach(
            bottom_right_rear_anchor.target,
            parent=bottom_right_rear_anchor.reference,
            child=rear_mount_a,
            offset=bottom_right_rear_offset,
            gap=gap,
            angle=180,
        )
        bottom_left_rear_anchor, bottom_left_rear_offset = parent_anchor("back_bottom_left")
        bottom_left_rear = bracket.copy().attach(
            bottom_left_rear_anchor.target,
            parent=bottom_left_rear_anchor.reference,
            child=rear_mount_b,
            offset=bottom_left_rear_offset,
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
