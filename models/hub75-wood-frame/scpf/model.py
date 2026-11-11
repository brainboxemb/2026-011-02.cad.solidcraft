"""Upright wooden HUB75 Basic Box with five lightweight panel envelopes.

The previous model kept the screen in XY, so it appeared lying flat in
SolidCraft's normal Z-up 3D view. This uses the physical CAD axes:
  X: screen width (left/right)
  Y: cabinet depth (negative = viewer/front, positive = back)
  Z: height (world up)
All parts stand in XZ. Five panels are grouped under HUB75Panels
as one native subassembly, while each wood component remains separate.
It is real geometry, NOT a screenshot camera fix.

Reference: Basic Box v29. Wooden opening Z=0..362, outside box
Z=-15..377. LED front plane Y=0, cabinet depth Y=-25..75,
outer back +Y. Provisional corner rails are not the final brackets.
"""
from scpf import component
from models.components.hub75_panels import HUB75Panels
from models.components.wood_box import (
    SideWall as SideDefinition,
    BottomBoard as BottomDefinition,
    RoofBoard as RoofDefinition,
    BackBoard as BackDefinition,
    Window as WindowDefinition,
    CornerRailConcept as CornerDefinition,
)

Side = component(SideDefinition)
Bottom = component(BottomDefinition)
Roof = component(RoofDefinition)
Back = component(BackDefinition)
Glass = component(WindowDefinition)
Corner = component(CornerDefinition)


class WoodenHub75BasicBox:
    internal_width = 844.0
    internal_height = 362.0
    plywood = 15.0
    overall_width = 874.0
    overall_height = 392.0
    panel_pitch = 160.0
    front_depth = -25.0
    cabinet_depth = 100.0

    def build(self):
        # One expandable native group for all five lightweight panels.
        # The frame's wood pieces remain separate, editable components.
        assembly = HUB75Panels(
            opening_height=self.internal_height, pitch=self.panel_pitch
        ).build()

        side_x = self.internal_width / 2 + self.plywood / 2
        top_z = self.internal_height
        depth_mid = self.front_depth + self.cabinet_depth / 2

        # Sides stand from Z=0 to 362. Their full depth is Y=-25..75.
        assembly = assembly + Side().move(x=-side_x, y=depth_mid)
        assembly = assembly + Side().move(x=side_x, y=depth_mid)

        # Bottom and roof are horizontal wood boards at the actual Z edges.
        assembly = assembly + Bottom().move(y=depth_mid, z=-self.plywood)
        # The roof extends 24 mm beyond the back of the main 100 mm cabinet.
        assembly = assembly + Roof().move(y=self.front_depth + RoofDefinition.depth / 2,
                                         z=top_z)

        # Separate, upright 9 mm rear panel and 4 mm front glass.
        # The back reaches Z=-7.5..369.5, inside the outer 392 mm height.
        back_bottom = (self.internal_height - BackDefinition.height) / 2
        assembly = assembly + Back().move(
            y=self.front_depth + self.cabinet_depth + BackDefinition.thickness / 2,
            z=back_bottom,
        )
        # Front glazing spans Z=1..361 and Y=-18..-14.
        assembly = assembly + Glass().move(y=-16, z=1)

        # Four L-shaped EXTERNAL corner rail concepts in the upright XZ
        # plane. Rotate about the cabinet's depth axis (Y), NOT Z.
        # 0, -90, 180, +90 orient the open corners toward the cabinet.
        outer_x = self.overall_width / 2
        bottom_z = -self.plywood
        top_z = self.internal_height + self.plywood
        for x, z, angle in (
            (-outer_x, bottom_z, 0),
            (outer_x, bottom_z, -90),
            (outer_x, top_z, 180),
            (-outer_x, top_z, 90),
        ):
            # XZ positive extrusion follows the sketch normal -Y.
            # Start at the back (Y=+75), continue to the front (Y=-25).
            rail = Corner().move(x=x, y=self.front_depth + self.cabinet_depth, z=z)
            if angle:
                rail = rail.rotate(axis=(0, 1, 0), degrees=angle)
            assembly = assembly + rail

        return assembly


WoodenHub75BasicBox()
