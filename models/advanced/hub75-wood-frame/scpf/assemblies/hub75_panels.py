"""Five-panel HUB75 subassembly."""

from scpf import component, pv

from components.hub75_basic import Hub75PanelBasic


Panel = component(Hub75PanelBasic)


class HUB75Panels:
    opening_height = 362.0
    panel_count = 5
    panel_pitch = 160.0

    def build(self):
        count = int(pv(self.panel_count))
        if count < 1 or count % 2 != 1:
            raise ValueError("panel_count must be a positive odd number")

        panel_y = Hub75PanelBasic.depth / 2
        panel_z = (pv(self.opening_height) - Hub75PanelBasic.height) / 2
        middle = Panel().move(y=panel_y, z=panel_z)
        panels = middle

        for column in range(count):
            if column == count // 2:
                continue
            x = (column - count // 2) * pv(self.panel_pitch)
            panels = panels + middle.copy().move(x=x)

        return panels.group("HUB75Panels")
