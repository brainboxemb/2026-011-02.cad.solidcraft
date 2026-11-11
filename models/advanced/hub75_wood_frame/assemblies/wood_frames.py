"""Native subassemblies for the upright plywood HUB75 Basic Box.

HUB75Panels is separate. These native parent components keep the browser
clean and let each manufactured part be selected individually:
  WoodBoxFrame   -- sides, floor, roof, back
  WoodGlassFrame -- four 15x15 mm glazing retainers (glass is separate)
  CornerBrackets -- four occurrences of the REAL fast four-hole bracket

World X = width, Y = depth (front -Y), Z = up.
"""
from scpf import component
from scpf.core import value_of

from models.components.wood_box import (
    SideWall, BottomBoard, RoofBoard, BackBoard,
    GlassSideStrip, GlassCrossStrip,
)
from models.components.corner_bracket_fast import CornerBracketFast

Side = component(SideWall)
Bottom = component(BottomBoard)
Roof = component(RoofBoard)
Back = component(BackBoard)
GlassSide = component(GlassSideStrip)
GlassCross = component(GlassCrossStrip)
Bracket = component(CornerBracketFast)


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
            z=(self.height - BackBoard.height) / 2,
        )
        return frame.group("WoodBoxFrame")


class WoodGlassFrame:
    """Four rectangular wooden 15x15 retainers behind the plexiglass.

    The glass itself is a separate component at Y=-18..-14.
    Retainers are at Y=-14..1, touching the *rear* of the glass,
    with no overlap with the active 800x320 panel grid.
    """
    opening_width = 844.0
    opening_height = 362.0
    strip = 15.0
    glass_rear_y = -14.0

    def build(self):
        x = (self.opening_width - self.strip) / 2
        y = self.glass_rear_y + self.strip / 2
        left = GlassSide().move(x=-x, y=y)
        frame = left + left.copy().move(x=2*x)
        bottom = GlassCross().move(y=y)
        frame = frame + bottom + bottom.copy().move(
            z=self.opening_height - self.strip
        )
        return frame.group("WoodGlassFrame")


class CornerBrackets:
    """The shared four-hole fast bracket at the four actual wood corners.

    The L inside vertex belongs at each *interior aperture corner*,
    not at the extreme outer corner. Rotations are 180 deg around
    X/Y/Z, which turn the arms into the wood without floating free.
    """
    opening_width = 844.0
    opening_height = 362.0
    plywood = 15.0
    front_y = -25.0

    def build(self):
        half = self.opening_width / 2
        front_band_y = self.front_y + CornerBracketFast.bracket_width / 2
        top_left = Bracket(plywood_thickness=value_of(self.plywood)).move(
            x=-half, y=front_band_y, z=self.opening_height
        )
        corners = top_left
        for dx, dz, axis in (
            (self.opening_width, 0.0, (0, 0, 1)),       # upper right
            (0.0, -self.opening_height, (1, 0, 0)),    # lower left
            (self.opening_width, -self.opening_height, (0, 1, 0)), # lower right
        ):
            corners = corners + top_left.copy().move(
                x=dx, z=dz
            ).rotate(axis=axis, degrees=180)
        return corners.group("CornerBrackets")
