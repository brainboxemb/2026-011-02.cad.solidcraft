"""HUB75 wooden enclosure: grouped geometry, physically upright (Z up).

Source: 55th-edition Basic Box v29, 874 x 392 mm external.
Basic modules are coplanar rectangular envelopes. The detailed HUB75
reference independently retains PCB/connector orientations.
"""
from scpf import component
from models.advanced.hub75_wood_frame.assemblies.hub75_panels import HUB75Panels
from models.advanced.hub75_wood_frame.parts.wood import Window as WindowDefinition
from models.advanced.hub75_wood_frame.assemblies.wood_frames import WoodBoxFrame, WoodGlassFrame, CornerBrackets

Glass = component(WindowDefinition)


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
        # Native model-browser groups, not a flattened CSG assembly:
        panels = HUB75Panels(
            opening_height=self.internal_height, pitch=self.panel_pitch
        ).build()
        box = WoodBoxFrame(
            width=self.internal_width, height=self.internal_height,
            plywood=self.plywood, front_y=self.front_depth,
            depth=self.cabinet_depth,
        ).build()
        glass_frame = WoodGlassFrame().build()
        brackets = CornerBrackets().build()

        # Plexiglass is separate from the wooden strips for real assembly.
        # Glass thickness Y=-18..-14, opening between Z=1..361.
        window = Glass().move(y=-16, z=1)
        return panels + box + glass_frame + brackets + window


WoodenHub75BasicBox()
