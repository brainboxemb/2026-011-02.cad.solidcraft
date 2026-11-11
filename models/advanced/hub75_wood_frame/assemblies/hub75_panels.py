"""Five uniform basic HUB75 panel envelopes in a named native subassembly.

The basic panel has no connector/PCB geometry: a rotation of its box has
no useful visual meaning and caused confusing native occurrence placements.
All front faces are coplanar at Y=0, all bottoms at Z=21.145 mm.
Advanced, physically oriented modules stay in the detailed HUB75 model.
"""
from scpf import component
from components.hub75_basic import Hub75PanelBasic

Panel = component(Hub75PanelBasic)


class HUB75Panels:
    """Five lightweight panel copies under one editable parent component."""

    def __init__(self, *, opening_height=362.0, pitch=160.0):
        self.opening_height = opening_height
        self.pitch = pitch

    def build(self):
        panel_bottom = (self.opening_height - Hub75PanelBasic.height) / 2
        front_to_centre = Hub75PanelBasic.depth / 2
        centre = Panel().move(y=front_to_centre, z=panel_bottom)
        panels = centre
        for column in (0, 1, 3, 4):
            # No native rotation in the geometry-only representation.
            # It only needs the correct physical envelope and alignment.
            panels = panels + centre.copy().move(
                x=(column - 2) * self.pitch
            )
        return panels.group("HUB75Panels")
