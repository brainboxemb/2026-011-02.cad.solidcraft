"""Reusable Festool FS-style guide rail component.

The rail length is the only adjustable CAD parameter. Cross-section dimensions
are fixed reference dimensions. The major width/channel dimensions come from
TSO Products' measured guide-rail comparison; small wall/base details are an
initial reconstruction that must be checked against the Printables STEP
reference before the profile is treated as dimensionally complete.
"""
from scpf import Polygon2D, Sketch, component


@component
class FestoolGuideRail:
    length = 1400.0

    # TSO Products, measured Festool guide-rail cross-section (mm).
    TOTAL_WIDTH = 184.20
    TOTAL_HEIGHT = 10.50
    LEFT_CHANNEL_OPENING = 8.30
    LEFT_CHANNEL_OUTER = 16.10
    SECOND_CHANNEL_OPENING = 8.30
    SECOND_CHANNEL_OUTER = 16.10
    SECOND_CHANNEL_RIGHT = 64.20

    # Reconstruction details not dimensioned by the TSO comparison drawing.
    # Keep these fixed until checked against the Printables v13 STEP model.
    BASE_THICKNESS = 1.80
    CHANNEL_FLOOR = 2.40
    LIP_THICKNESS = 1.50
    SECOND_CHANNEL_SHOULDER = 2.30

    def build(self):
        h = self.TOTAL_HEIGHT
        base = self.BASE_THICKNESS

        left_outer = self.LEFT_CHANNEL_OUTER
        left_opening = self.LEFT_CHANNEL_OPENING
        left_wall = (left_outer - left_opening) / 2
        left_inner_l = left_wall
        left_inner_r = left_outer - left_wall

        second_right = self.SECOND_CHANNEL_RIGHT
        second_outer = self.SECOND_CHANNEL_OUTER
        second_opening = self.SECOND_CHANNEL_OPENING
        second_left = second_right - second_outer
        second_wall = (second_outer - second_opening) / 2
        second_inner_l = second_left + second_wall
        second_inner_r = second_right - second_wall

        # X = rail width, Y = rail length, Z = height.
        # This is a functional reconstruction of the main extrusion profile:
        # the left saw-guide channel, the second raised channel and the broad
        # low rail body. Minor ribs/recesses remain intentionally omitted until
        # the STEP comparison has been completed.
        points = [
            ("bottom_left", (0.0, 0.0)),
            ("bottom_right", (self.TOTAL_WIDTH, 0.0)),
            ("right_top", (self.TOTAL_WIDTH, base)),
            ("second_right_base", (second_right, base)),
            ("second_right_outer", (second_right, h - self.SECOND_CHANNEL_SHOULDER)),
            ("second_top_right", (second_inner_r + self.LIP_THICKNESS, h)),
            ("second_top_left", (second_inner_l - self.LIP_THICKNESS, h)),
            ("second_left_outer", (second_left, h - self.SECOND_CHANNEL_SHOULDER)),
            ("second_left_base", (second_left, base)),
            ("left_channel_right_base", (left_outer, base)),
            ("left_channel_right_top", (left_outer, h - self.LIP_THICKNESS)),
            ("left_channel_right_lip", (left_inner_r, h - self.LIP_THICKNESS)),
            ("left_channel_right_inner", (left_inner_r, self.CHANNEL_FLOOR)),
            ("left_channel_left_inner", (left_inner_l, self.CHANNEL_FLOOR)),
            ("left_channel_left_lip", (left_inner_l, h)),
            ("left_channel_left_top", (0.0, h)),
        ]

        with Sketch(name="Festool FS profile", plane="XZ") as profile:
            Polygon2D(points, plane="XZ", world=True)

        return profile.extrude(self.length, sym=True)
