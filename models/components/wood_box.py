"""Simple prototype woodworking components.

Reference: Batavierenrace 55th edition Basic Box / LIGHTPLY concept (v29).
The class names describe individual manufacturing pieces. In this concept
the four corner rails represent the external 3D-printed corner connections,
NOT the final corner_bracket geometry from the OpenSCAD archive.
"""
from scpf import Box, Polygon2D


class SideWall:
    thickness = 15.0
    height = 362.0
    depth = 100.0

    def build(self):
        return Box(self.thickness, self.height, self.depth).with_material(
            "LIGHTPLY side wall", density_g_cm3=0.55, color="#CBA36B"
        )


class BottomBoard:
    width = 874.0
    thickness = 15.0
    depth = 100.0

    def build(self):
        return Box(self.width, self.thickness, self.depth).with_material(
            "LIGHTPLY bottom", density_g_cm3=0.55, color="#CBA36B"
        )


class RoofBoard:
    width = 874.0
    thickness = 15.0
    depth = 124.0

    def build(self):
        return Box(self.width, self.thickness, self.depth).with_material(
            "LIGHTPLY roof", density_g_cm3=0.55, color="#CBA36B"
        )


class BackBoard:
    width = 874.0
    height = 377.0
    thickness = 9.0

    def build(self):
        return Box(self.width, self.height, self.thickness).with_material(
            "LIGHTPLY rear", density_g_cm3=0.55, color="#A87D4D"
        )


class Window:
    width = 840.0
    height = 360.0
    thickness = 4.0

    def build(self):
        # Color is only a visual placeholder: no optical transparency claims.
        return Box(self.width, self.height, self.thickness).with_material(
            "Plexiglass", density_g_cm3=1.19, color="#B7DAEF"
        )


class CornerRailConcept:
    arm_length = 100.0
    wall = 6.0
    depth = 100.0

    def build(self):
        # External, full-depth L-shaped coupling. Prototype: no bolts,
        # chamfers, elephant-foot relief or exact panel-attachment seats.
        outline = Polygon2D([
            (0, 0), (self.arm_length, 0),
            (self.arm_length, self.wall),
            (self.wall, self.wall),
            (self.wall, self.arm_length), (0, self.arm_length),
        ])
        return outline.extrude(self.depth).with_material(
            "Printed corner connector concept",
            density_g_cm3=1.25, color="#D65A3F"
        )
