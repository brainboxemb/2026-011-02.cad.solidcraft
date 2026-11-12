"""Five-panel HUB75 subassembly."""

from scpf import assembly, component, pv

from components.hub75_basic import (
    HUB75_PANEL_DEPTH,
    HUB75_PANEL_HEIGHT,
    Hub75PanelBasic,
)


Panel = component(Hub75PanelBasic)


@assembly
class HUB75Panels:
    opening_height = 362.0
    panel_count = 5
    panel_pitch = 160.0
    panel_recess_depth = 25.0

    def build(self):
        count = int(pv(self.panel_count))
        if count < 1 or count % 2 != 1:
            raise ValueError("panel_count must be a positive odd number")

        panel_y = self.panel_recess_depth + HUB75_PANEL_DEPTH / 2
        panel_z = (self.opening_height - HUB75_PANEL_HEIGHT) / 2
        middle = Panel(
            z_position=panel_z,
        ).move(
            y=panel_y,
        )
        panels = middle

        for column in range(count):
            if column == count // 2:
                continue
            x = (column - count // 2) * self.panel_pitch
            panels = panels + middle.copy().move(x=x)

        return panels.group("HUB75Panels")
