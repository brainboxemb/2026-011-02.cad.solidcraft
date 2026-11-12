"""Attach eight reusable corner brackets to the actual frame boards."""

from scpf import Anchor, component

from models.components.corner_bracket.scpf.model import CornerBracket


Bracket = component(CornerBracket)


def attach_corner_brackets(
    *,
    roof,
    bottom,
    bracket_width,
    corner_radius,
    roof_front_overhang,
    roof_rear_overhang,
    panel_wood_thickness,
):
    """Build eight fixed bracket attachments from real board references."""

    bracket = Bracket(
        bracket_width=bracket_width,
        inside_corner_radius=corner_radius,
    )

    # The bracket origin is its inside XZ corner and lies at the centre of
    # bracket_width. Native corner origins already follow board width/height.
    # Only Y needs an inward offset from the selected front/back board face.
    half = bracket_width / 2
    bottom_gap = -half
    roof_front_gap = -(roof_front_overhang + half)
    roof_rear_gap = -(panel_wood_thickness + roof_rear_overhang + half)

    def attached(parent, parent_anchor, child_anchor, gap):
        return bracket.copy().attach(
            parent,
            parent=parent_anchor,
            child=child_anchor,
            gap=gap,
        )

    top_left_front = attached(
        roof, Anchor.FRONT_TOP_LEFT, "front_mount", roof_front_gap
    )
    top_right_front = attached(
        roof, Anchor.FRONT_TOP_RIGHT, "front_mount", roof_front_gap
    )
    bottom_right_front = attached(
        bottom, Anchor.FRONT_BOTTOM_RIGHT, "front_mount", bottom_gap
    )
    bottom_left_front = attached(
        bottom, Anchor.FRONT_BOTTOM_LEFT, "front_mount", bottom_gap
    )

    top_left_rear = attached(
        roof, Anchor.BACK_TOP_LEFT, "rear_mount", roof_rear_gap
    )
    top_right_rear = attached(
        roof, Anchor.BACK_TOP_RIGHT, "rear_mount", roof_rear_gap
    )
    bottom_right_rear = attached(
        bottom, Anchor.BACK_BOTTOM_RIGHT, "rear_mount", bottom_gap
    )
    bottom_left_rear = attached(
        bottom, Anchor.BACK_BOTTOM_LEFT, "rear_mount", bottom_gap
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
