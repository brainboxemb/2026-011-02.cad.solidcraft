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


class GlassSideStrip:
    """A 15 x 15 mm wooden retaining strip running vertically."""
    width = 15.0
    depth = 15.0
    height = 362.0

    def build(self):
        return Box(self.width, self.depth, self.height).with_material(
            "LIGHTPLY glazing side strip", density_g_cm3=0.55, color="#C89D61"
        )


class GlassCrossStrip:
    """Retaining strip between the vertical strips, top or bottom."""
    length = 814.0
    depth = 15.0
    thickness = 15.0

    def build(self):
        return Box(self.length, self.depth, self.thickness).with_material(
            "LIGHTPLY glazing cross strip", density_g_cm3=0.55, color="#C89D61"
        )
