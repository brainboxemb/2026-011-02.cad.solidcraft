"""Native subassemblies for the upright plywood HUB75 Basic Box.

HUB75Panels is separate. These native parent components keep the browser
clean and let each manufactured part be selected individually:
  WoodBoxFrame   -- sides, floor, roof, back
  WoodGlassFrame -- four 15x15 mm glazing retainers (glass is separate)
  CornerBrackets -- four occurrences of the same shared, hole-free CornerBracket

World X = width, Y = depth (front -Y), Z = up.
"""
from scpf import component

from hub75_wood_frame.parts.wood import (
    SideWall, BottomBoard, RoofBoard, BackBoard,
    GlassSideStrip, GlassCrossStrip,
)
from components.corner_bracket import CornerBracket

Side = component(SideWall)
Bottom = component(BottomBoard)
Roof = component(RoofBoard)
Back = component(BackBoard)
GlassSide = component(GlassSideStrip)
GlassCross = component(GlassCrossStrip)
Bracket = component(CornerBracket)


class WoodBoxFrame:
    """Four 15 mm plywood sides plus separate 9 mm back board."""

    def __init__(self, *, width=844.0, height=362.0,
                 plywood=15.0, front_y=-25.0, depth=100.0):
        self.width, self.height = width, height
        self.plywood, self.front_y, self.depth = plywood, front_y, depth

    def build(self):
        half_side_spacing = self.width / 2 + self.plywood / 2
        depth_centre = self.front_y + self.depth / 2

        left = Side().move(x=-half_side_spacing, y=depth_centre)
        frame = left + left.copy().move(x=2 * half_side_spacing)
        frame = frame + Bottom().move(y=depth_centre, z=-self.plywood)

        # Roof: horizontal 874 x 124 x 15 mm, at Z=362..377.
        frame = frame + Roof().move(
            y=self.front_y + RoofBoard.depth / 2, z=self.height
        )
        # Rear: 9 mm behind the principal 100 mm body, still vertical.
        frame = frame + Back().move(
            y=self.front_y + self.depth + BackBoard.thickness / 2,
            # Back is 377 mm high, so its bottom follows the cabinet
            # bottom at -15 and its top STOPS at Z=362 under the roof.
            z=-self.plywood,
        )
        return frame.group("WoodBoxFrame")


class WoodGlassFrame:
    """Four 45°-mitred glazing strips IN FRONT of the plexiglass.

    The rear of the wooden frame touches the front glass face at Y=-18.
    All four strips are 15 mm wide/deep, from Y=-33 to -18. The
    outside XY/XZ mitered corners have a common R4 outer contour.
    """
    opening_width = 844.0
    opening_height = 362.0
    strip = 15.0
    glass_front_y = -18.0

    def build(self):
        half = self.opening_width / 2
        y = self.glass_front_y - self.strip / 2
        # The profile has its outer face at local x=0. On the right, the
        # 180° Z turn mirrors X while preserving the same Z height.
        left = GlassSide().move(x=-half, y=y)
        right = left.copy().move(x=self.opening_width).rotate(
            axis=(0, 0, 1), degrees=180
        )
        # The bottom profile is centred on X and its outside edge Z=0.
        # A 180° X turn changes bottom -> top without changing the mitre
        # line; symmetric Y extrusion makes reversal harmless.
        bottom = GlassCross().move(y=y)
        top = bottom.copy().move(z=self.opening_height).rotate(
            axis=(1, 0, 0), degrees=180
        )
        return (left + right + bottom + top).group("WoodGlassFrame")


class CornerBrackets:
    """Four genuine L brackets on the OUTSIDE of plywood corners.

    The sketch's inner vertex is at each OUTER plywood corner. A bracket
    horizontal wing rests above/below the top/bottom board, and the
    vertical wing lies left/right of the side board. Arms point inward
    along the board surfaces, rather than intersecting solid plywood.
    No screw holes are cut while the native warning-producing hole geometry
    is deferred; the outer form and orientation remain unchanged.
    """
    opening_width = 844.0
    opening_height = 362.0
    plywood = 15.0
    front_y = -25.0

    def build(self):
        outer_half = self.opening_width / 2 + self.plywood
        top_z = self.opening_height + self.plywood
        bottom_z = -self.plywood
        # Put the 24 mm wide bracket on the first 24 mm of case depth.
        # At top-left, local horizontal +X wing lies ON top of the roof
        # and the local vertical -Z wing lies OUTSIDE the left side board.
        front_band_y = self.front_y + CornerBracket.bracket_width / 2
        top_left = Bracket().move(
            x=-outer_half, y=front_band_y, z=top_z
        )
        corners = top_left
        for dx, dz, axis in (
            (2 * outer_half, 0.0, (0, 0, 1)),         # upper right
            (0.0, bottom_z - top_z, (1, 0, 0)),        # lower left
            (2 * outer_half, bottom_z - top_z, (0, 1, 0)), # lower right
        ):
            corners = corners + top_left.copy().move(
                x=dx, z=dz
            ).rotate(axis=axis, degrees=180)
        return corners.group("CornerBrackets")
