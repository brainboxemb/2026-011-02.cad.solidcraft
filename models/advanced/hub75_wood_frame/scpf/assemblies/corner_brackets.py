"""Eight corner brackets attached to an existing WoodFrame assembly."""

from scpf import Anchor, assembly, component

from models.components.corner_bracket.scpf.model import CornerBracket


Bracket = component(CornerBracket)


@assembly
class CornerBrackets:
    """Construct the bracket assembly from an existing wood frame."""

    wood_frame = None
    bracket_width = 24.0
    corner_radius = 4.0
    roof_front_overhang = 10.0
    roof_rear_overhang = 1.0
    panel_wood_thickness = 9.0

    def build(self):
        if self.wood_frame is None:
            raise ValueError("CornerBrackets requires wood_frame")

        roof = self.wood_frame.roof
        bottom = self.wood_frame.bottom

        bracket = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
        )

        # X and Z come from the actual board corners. The remaining Y offset
        # places the symmetric bracket body inside the cabinet depth.
        half = self.bracket_width / 2
        bottom_gap = -half
        roof_front_gap = -(self.roof_front_overhang + half)
        roof_rear_gap = -(
            self.panel_wood_thickness + self.roof_rear_overhang + half
        )

        def attached(parent, parent_anchor, child_anchor, gap, angle):
            return bracket.copy().attach(
                parent,
                parent=parent_anchor,
                child=child_anchor,
                gap=gap,
                angle=angle,
            )

        top_left_front = attached(
            roof,
            Anchor.FRONT_TOP_LEFT,
            "front_mount",
            roof_front_gap,
            90,
        )
        top_right_front = attached(
            roof,
            Anchor.FRONT_TOP_RIGHT,
            "front_mount",
            roof_front_gap,
            90,
        )
        bottom_right_front = attached(
            bottom,
            Anchor.FRONT_BOTTOM_RIGHT,
            "front_mount",
            bottom_gap,
            90,
        )
        bottom_left_front = attached(
            bottom,
            Anchor.FRONT_BOTTOM_LEFT,
            "front_mount",
            bottom_gap,
            90,
        )

        top_left_rear = attached(
            roof,
            Anchor.BACK_TOP_LEFT,
            "rear_mount",
            roof_rear_gap,
            0,
        )
        top_right_rear = attached(
            roof,
            Anchor.BACK_TOP_RIGHT,
            "rear_mount",
            roof_rear_gap,
            0,
        )
        bottom_right_rear = attached(
            bottom,
            Anchor.BACK_BOTTOM_RIGHT,
            "rear_mount",
            bottom_gap,
            0,
        )
        bottom_left_rear = attached(
            bottom,
            Anchor.BACK_BOTTOM_LEFT,
            "rear_mount",
            bottom_gap,
            0,
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
