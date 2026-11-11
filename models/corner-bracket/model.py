"""Standalone native regression for the shared fast corner bracket.

The original geometry now lives in components/corner_bracket.py
so the wooden screen reuses the exact same four-hole shape and edge history.
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
    plywood_thickness = _Shared.plywood_thickness
    bolt_offset = _Shared.bolt_offset
    bolt_spacing = _Shared.bolt_spacing
    bolt_y_offset = _Shared.bolt_y_offset
    bolt_diameter = _Shared.bolt_diameter
    bolt_clearance = _Shared.bolt_clearance
    head_diameter = _Shared.head_diameter
    head_clearance = _Shared.head_clearance
    head_recess = _Shared.head_recess

    def build(self):
        return _Shared.build(self)


CornerBracket()
