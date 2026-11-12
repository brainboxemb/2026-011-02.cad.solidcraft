"""Five-panel HUB75 subassembly."""

from scpf import assembly, component

from models.components.hub75_basic import (
    HUB75_PANEL_DEPTH,
    HUB75_PANEL_HEIGHT,
    Hub75PanelBasic,
)


Panel = component(Hub75PanelBasic)

# This model is specifically the five-panel display. Count and pitch define
# that fixed product layout; they are not editable SolidCraft parameters.
PANEL_COUNT = 5
PANEL_PITCH = 160.0


@assembly
class HUB75Panels:
    opening_height = 362.0
    opening_bottom_z = 12.0
    panel_recess_depth = 25.0

    def build(self):
        panel_y = self.panel_recess_depth + HUB75_PANEL_DEPTH / 2
        panel_z = (
            self.opening_bottom_z
            + (self.opening_height - HUB75_PANEL_HEIGHT) / 2
        )
        middle = Panel(
            y_center=panel_y,
            z_position=panel_z,
        )
        panels = middle

        for column in range(PANEL_COUNT):
            if column == PANEL_COUNT // 2:
                continue
            x = (column - PANEL_COUNT // 2) * PANEL_PITCH
            panels = panels + middle.copy().move(x=x)

        return panels.group("HUB75Panels")
