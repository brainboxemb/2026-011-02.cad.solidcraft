"""Five lightweight HUB75 modules as one named SolidCraft subassembly.

The component's name is deliberately plural: HUB75Panels. It contains five
occurrences of ONE native Hub75PanelBasic definition, with the alternate
modules turned around the world Y (depth) axis. The native browser shows the
group as an expandable component, with the wooden enclosure parts beside it.

X = horizontal, Y = front/back, Z = up. Basic panels only: the advanced
loft/PCB reference stays a separate, independently qualified model.
"""
from scpf import component
from models.components.hub75_basic import Hub75PanelBasic

Panel = component(Hub75PanelBasic)


class HUB75Panels:
    """A reusable five-panel group inside the surrounding woodwork assembly."""

    def __init__(self, *, opening_height=362.0, pitch=160.0):
        self.opening_height = opening_height
        self.pitch = pitch

    def build(self):
        panel_bottom = (self.opening_height - Hub75PanelBasic.height) / 2
        panel_y = Hub75PanelBasic.depth / 2

        centre = Panel().move(y=panel_y, z=panel_bottom)
        panels = centre
        for column in (0, 1, 3, 4):
            x = (column - 2) * self.pitch
            occurrence = centre.copy().move(x=x)
            if column in (1, 3):
                # A Y-axis half-turn flips the height direction. Move the
                # occurrence's pivot to the top before applying the turn.
                occurrence = occurrence.move(z=Hub75PanelBasic.height).rotate(
                    axis=(0, 1, 0), degrees=180
                )
            panels = panels + occurrence

        # This is a REAL native parent component, not a cosmetic list label.
        return panels.group("HUB75Panels")
