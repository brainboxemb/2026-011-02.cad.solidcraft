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

        top_left_front = bracket.copy().attach(
            roof,
            parent=Anchor.FRONT_TOP_LEFT,
            child="front_mount",
            gap=roof_front_gap,
            angle=90,
        )
        top_right_front = bracket.copy().attach(
            roof,
            parent=Anchor.FRONT_TOP_RIGHT,
            child="front_mount",
            gap=roof_front_gap,
            angle=90,
        )
        bottom_right_front = bracket.copy().attach(
            bottom,
            parent=Anchor.FRONT_BOTTOM_RIGHT,
            child="front_mount",
            gap=bottom_gap,
            angle=90,
        )
        bottom_left_front = bracket.copy().attach(
            bottom,
            parent=Anchor.FRONT_BOTTOM_LEFT,
            child="front_mount",
            gap=bottom_gap,
            angle=90,
        )

        top_left_rear = bracket.copy().attach(
            roof,
            parent=Anchor.BACK_TOP_LEFT,
            child="rear_mount",
            gap=roof_rear_gap,
            angle=0,
        )
        top_right_rear = bracket.copy().attach(
            roof,
            parent=Anchor.BACK_TOP_RIGHT,
            child="rear_mount",
            gap=roof_rear_gap,
            angle=0,
        )
        bottom_right_rear = bracket.copy().attach(
            bottom,
            parent=Anchor.BACK_BOTTOM_RIGHT,
            child="rear_mount",
            gap=bottom_gap,
            angle=0,
        )
        bottom_left_rear = bracket.copy().attach(
            bottom,
            parent=Anchor.BACK_BOTTOM_LEFT,
            child="rear_mount",
            gap=bottom_gap,
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
