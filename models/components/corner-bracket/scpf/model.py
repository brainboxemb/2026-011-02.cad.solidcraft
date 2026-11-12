"""Standalone native regression for the shared hole-free corner bracket.

The original geometry now lives in components/corner_bracket.py
so the wooden screen reuses the exact same hole-free shape and edge history.
"""
from components.corner_bracket import CornerBracket as _Shared


class CornerBracket:
    bracket_width = _Shared.bracket_width
    wall_thickness = _Shared.wall_thickness
    horizontal_arm_length = _Shared.horizontal_arm_length
    vertical_arm_length = _Shared.vertical_arm_length
    outer_corner_chamfer = _Shared.outer_corner_chamfer
    arm_end_chamfer = _Shared.arm_end_chamfer
    side_edge_chamfer = _Shared.side_edge_chamfer
    elephant_foot_relief = _Shared.elephant_foot_relief
    inside_corner_radius = _Shared.inside_corner_radius

    def build(self):
        return _Shared.build(self)


CornerBracket()
