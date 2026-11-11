"""Prototype 1 wooden Basic Box + five lightweight HUB75 envelopes.

Drawn from the Basic Box v29 concept (not the aluminium v1.0/v1.2 rail
project). X is width, Y is vertical height, Z is front-to-back depth.
The five LED front faces are on Z=0. The wood reaches from Z=-25 to
+75 and the outside 9 mm rear panel starts at Z=75. The 4 mm plexiglass
is in front of the LEDs. Mounting hardware and precise optics are WIP.
"""
from scpf import component
from models.components.hub75_basic import Hub75PanelBasic as BasicDefinition
from models.components.wood_box import (
    SideWall as SideDefinition,
    BottomBoard as BottomDefinition,
    RoofBoard as RoofDefinition,
    BackBoard as BackDefinition,
    Window as WindowDefinition,
    CornerRailConcept as CornerDefinition,
)

Panel = component(BasicDefinition)
Side = component(SideDefinition)
Bottom = component(BottomDefinition)
Roof = component(RoofDefinition)
Back = component(BackDefinition)
Glass = component(WindowDefinition)
Corner = component(CornerDefinition)


class WoodenHub75BasicBox:
    # From the existing prototype reference, *not* inferred from HUB75's PCB.
    internal_width = 844.0
    internal_height = 362.0
    plywood = 15.0
    overall_width = 874.0
    overall_height = 392.0
    panel_pitch = 160.0
    corner_z = -25.0

    def build(self):
        # Panel instances are first: the centre stays at the global origin.
        # This preserves simple occurrence.copy translation and orientation.
        centre = Panel()
        assembly = centre
        for column in (0, 1, 3, 4):
            x = (column - 2) * self.panel_pitch
            copy = centre.copy().move(x=x)
            if column in (1, 3):
                copy = copy.rotate(axis=(0, 0, 1), degrees=180)
            assembly = assembly + copy

        side_x = self.internal_width / 2 + self.plywood / 2
        board_y = self.internal_height / 2 + self.plywood / 2

        # Boards and window are separate native components, not fused
        # to one BRep. These placements form the *basic* wooden envelope.
        assembly = assembly + Side().move(x=-side_x, z=-25)
        assembly = assembly + Side().move(x=side_x, z=-25)
        assembly = assembly + Bottom().move(y=-board_y, z=-25)
        assembly = assembly + Roof().move(y=board_y, z=-25)
        assembly = assembly + Back().move(z=75)
        assembly = assembly + Glass().move(z=-18)

        # The L sections show the intended external corner connections.
        # Exact bolt holes and outside fit will be derived from the
        # separate Corner Bracket reference, NOT assumed correct here.
        outer_x = self.overall_width / 2
        outer_y = self.overall_height / 2
        for x, y, angle in (
            (-outer_x, -outer_y, 0),
            (outer_x, -outer_y, 90),
            (outer_x, outer_y, 180),
            (-outer_x, outer_y, 270),
        ):
            rail = Corner().move(x=x, y=y, z=self.corner_z)
            if angle:
                rail = rail.rotate(axis=(0, 0, 1), degrees=angle)
            assembly = assembly + rail

        return assembly


WoodenHub75BasicBox()
