"""Reusable Festool FS-style guide rail component.

The rail length is the only adjustable CAD parameter. The simplified
cross-section is based directly on the measured Festool dimensions published
in TSO Products' Guide Rail Extrusion Comparison Guide.
"""
from scpf import Polygon2D, Sketch, component


@component
class FestoolGuideRail:
    length = 1400.0

    # TSO Products measured Festool guide-rail dimensions (mm).
    # Names deliberately follow the A-H labels in the source drawing.
    TSO_A_OPENING_LEFT = 8.30
    TSO_B_LEFT_FEATURE = 16.10
    TSO_D_HEIGHT = 10.50
    TSO_E_OPENING_CENTER = 8.30
    TSO_F_CENTER_FEATURE = 16.10
    TSO_G_CENTER_RIGHT = 64.20
    TSO_H_TOTAL_WIDTH = 184.20

    # TSO does not dimension the small wall/base thicknesses. These are kept
    # deliberately simple because this component is intended as a useful CAD
    # representation of the guide rail, not a manufacturing drawing.
    BASE_THICKNESS = 2.0
    TOP_LIP_THICKNESS = 1.5

    def build(self):
        height = self.TSO_D_HEIGHT
        base = self.BASE_THICKNESS

        left_outer = self.TSO_B_LEFT_FEATURE
        left_opening = self.TSO_A_OPENING_LEFT
        left_wall = (left_outer - left_opening) / 2
        left_inner_l = left_wall
        left_inner_r = left_outer - left_wall

        center_right = self.TSO_G_CENTER_RIGHT
        center_outer = self.TSO_F_CENTER_FEATURE
        center_opening = self.TSO_E_OPENING_CENTER
        center_left = center_right - center_outer
        center_wall = (center_outer - center_opening) / 2
        center_inner_l = center_left + center_wall
        center_inner_r = center_right - center_wall

        # X = rail width, Y = rail length, Z = height.
        #
        # The profile intentionally captures the dimensions that matter for an
        # MFT/guide-rail assembly: total width/height and the two characteristic
        # mounting/guide features. Small extrusion ribs are omitted.
        points = [
            ("bottom_left", (0.0, 0.0)),
            ("bottom_right", (self.TSO_H_TOTAL_WIDTH, 0.0)),
            ("right_top", (self.TSO_H_TOTAL_WIDTH, base)),

            ("center_right_base", (center_right, base)),
            ("center_right_top", (center_right, height)),
            ("center_inner_right_top", (center_inner_r, height)),
            ("center_inner_right_bottom", (center_inner_r, base)),
            ("center_inner_left_bottom", (center_inner_l, base)),
            ("center_inner_left_top", (center_inner_l, height)),
            ("center_left_top", (center_left, height)),
            ("center_left_base", (center_left, base)),

            ("left_right_base", (left_outer, base)),
            ("left_right_top", (left_outer, height - self.TOP_LIP_THICKNESS)),
            ("left_inner_right_top", (left_inner_r, height - self.TOP_LIP_THICKNESS)),
            ("left_inner_right_bottom", (left_inner_r, base)),
            ("left_inner_left_bottom", (left_inner_l, base)),
            ("left_inner_left_top", (left_inner_l, height)),
            ("left_top", (0.0, height)),
        ]

        with Sketch(name="Festool FS profile", plane="XZ") as profile:
            Polygon2D(points, plane="XZ", world=True)

        return profile.extrude(self.length, sym=True)
