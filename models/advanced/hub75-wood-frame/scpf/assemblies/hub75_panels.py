"""Five-panel HUB75 subassembly."""

from scpf import component, pv

from components.hub75_basic import Hub75PanelBasic


Panel = component(Hub75PanelBasic)


def build_hub75_panels(*, opening_height, panel_count, panel_pitch):
    height = pv(opening_height)
    count = int(pv(panel_count))
    pitch = pv(panel_pitch)

    if count < 1 or count % 2 != 1:
        raise ValueError("panel_count must be a positive odd number")

    panel_y = Hub75PanelBasic.depth / 2
    panel_z = (height - Hub75PanelBasic.height) / 2
    middle = Panel().move(y=panel_y, z=panel_z)
    panels = middle

    for column in range(count):
        if column == count // 2:
            continue
        x = (column - count // 2) * pitch
        panels = panels + middle.copy().move(x=x)

    return panels.group("HUB75Panels")
