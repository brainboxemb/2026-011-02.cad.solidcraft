"""Simple prototype woodworking components.

Reference: Batavierenrace 55th edition Basic Box / LIGHTPLY concept (v29).
The class names describe individual manufacturing pieces. In this concept
the four printed corner connectors are sourced from the shared
CornerBracket model, not placeholder 100 mm L-rails.

WORLD: X = screen width, Y = screen depth, Z = vertical (up).
All wooden parts are native SolidCraft solids standing upright, not
a horizontal XY layout rotated only in the camera.
"""
from scpf import Box


class SideWall:
    thickness = 15.0
    height = 362.0
    depth = 100.0

    def build(self):
        return Box(self.thickness, self.depth, self.height).with_material(
            "LIGHTPLY side wall", density_g_cm3=0.55, color="#CBA36B"
        )


class BottomBoard:
    width = 874.0
    thickness = 15.0
    depth = 100.0

    def build(self):
        return Box(self.width, self.depth, self.thickness).with_material(
            "LIGHTPLY bottom", density_g_cm3=0.55, color="#CBA36B"
        )


class RoofBoard:
    width = 874.0
    thickness = 15.0
    depth = 124.0

    def build(self):
        return Box(self.width, self.depth, self.thickness).with_material(
            "LIGHTPLY roof", density_g_cm3=0.55, color="#CBA36B"
        )


class BackBoard:
    width = 874.0
    height = 377.0
    thickness = 9.0

    def build(self):
        return Box(self.width, self.thickness, self.height).with_material(
            "LIGHTPLY rear", density_g_cm3=0.55, color="#A87D4D"
        )


class Window:
    width = 840.0
    height = 360.0
    thickness = 4.0

    def build(self):
        # Color is only a visual placeholder: no optical transparency claims.
        return Box(self.width, self.thickness, self.height).with_material(
            "Plexiglass", density_g_cm3=1.19, color="#B7DAEF"
        )


# The retaining frame is assembled out of four true mitred wooden strips.
# Both mating ends are cut on the SAME 45-degree bisector, not overlaid.
# The outer contour follows the same R4 rounding as the CornerBracket's
# inside corner. A short polygonal arc approximates a physical curved cut,
# split between the two 45-degree mating surfaces without a seam gap.
from math import cos, sin, radians
from scpf import Polygon2D, Direction
from scpf.core import value_of
from components.corner_bracket import CornerBracket


def _arc(cx, cz, radius, start, end, segments=6):
    """Sample an exact-angle contour, including both endpoints."""
    return [
        (cx + radius * cos(radians(start + (end-start)*i/segments)),
         cz + radius * sin(radians(start + (end-start)*i/segments)))
        for i in range(segments+1)
    ]


def _rounded_side_profile(width, height, radius):
    """Left vertical strip profile in XZ, outside at X=0.

    Outer edges connect to quarter-circle ends. At the miter the
    circular contour meets a 45-degree cut (x=z at the lower end).
    Right side is the SAME shape turned 180 degrees around Z.
    """
    if not 0 < radius < width < height/2:
        raise ValueError("side strip requires 0 < radius < width < height/2")
    upper = _arc(radius, height-radius, radius, 180, 135)
    lower = _arc(radius, radius, radius, 225, 180)
    return (
        [(0, radius), (0, height-radius)]
        + upper[1:]
        + [(width, height-width), (width, width)]
        + lower[:-1]
    )


def _rounded_cross_profile(length, thickness, radius):
    """Bottom strip XZ profile, full outer length with 45-degree mitres.

    The side strip's lower arc covers degrees 180..225. This horizontal
    strip owns degrees 225..270 and mirrors them at the right corner.
    The assembled outside corner is therefore one continuous R4 arc.
    Top piece is the SAME shape turned 180 degrees around X.
    """
    if not 0 < radius < thickness < length/2:
        raise ValueError("cross strip requires 0 < radius < thickness < length/2")
    half = length/2
    left = _arc(-half+radius, radius, radius, 225, 270)
    right = _arc(half-radius, radius, radius, 270, 315)
    return (
        left + [(half-radius, 0)] + right[1:]
        + [(half-thickness, thickness), (-half+thickness, thickness)]
    )


class GlassSideStrip:
    """Side retaining strip, R4 corners, mitred top and bottom."""
    width = 15.0
    depth = 15.0
    height = 362.0
    corner_radius = CornerBracket.inside_corner_radius

    def build(self):
        # Distinct darker finish helps distinguish the two vertical
        # retainers from the horizontal ones and the box itself.
        profile = Polygon2D(
            _rounded_side_profile(
                value_of(self.width), value_of(self.height),
                value_of(self.corner_radius)
            ),
            plane="XZ", world=True,
        )
        return profile.extrude(
            self.depth, direction=Direction.SYMMETRIC,
        ).with_material(
            "LIGHTPLY glazing side strip", density_g_cm3=0.55, color="#A9793E"
        )


class GlassCrossStrip:
    """Upper/lower retaining strip; two R4 outer ends, 45° mitres."""
    length = 844.0
    depth = 15.0
    thickness = 15.0
    corner_radius = CornerBracket.inside_corner_radius

    def build(self):
        # Light finish: top/bottom parts are visually different from
        # the darker side strips and regular LIGHTPLY walls.
        profile = Polygon2D(
            _rounded_cross_profile(
                value_of(self.length), value_of(self.thickness),
                value_of(self.corner_radius)
            ),
            plane="XZ", world=True,
        )
        return profile.extrude(
            self.depth, direction=Direction.SYMMETRIC,
        ).with_material(
            "LIGHTPLY glazing cross strip", density_g_cm3=0.55, color="#E3BF80"
        )
