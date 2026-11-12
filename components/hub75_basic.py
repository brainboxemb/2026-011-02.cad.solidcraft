"""Lightweight HUB75 placement envelope for large wooden-box assemblies.

No native loft, cutouts, rear PCB, or mounting bores: this component only
occupies the measured external bounding volume. The dimensions are fixed
product constants; Y/Z placement may be linked to parent design parameters.
"""
from scpf import Direction, Polygon2D


HUB75_PANEL_WIDTH = 159.70
HUB75_PANEL_HEIGHT = 319.71
HUB75_PANEL_DEPTH = 14.50


class Hub75PanelBasic:
    y_position = 0.0
    z_position = 0.0

    def build(self):
        front = self.y_position
        rear = front + HUB75_PANEL_DEPTH
        bottom = self.z_position
        top = bottom + HUB75_PANEL_HEIGHT

        profile = Polygon2D([
            (front, bottom),
            (rear, bottom),
            (rear, top),
            (front, top),
        ], plane="YZ", world=True)

        return profile.extrude(
            HUB75_PANEL_WIDTH,
            direction=Direction.SYMMETRIC,
        ).with_material(
            "LED panel envelope", density_g_cm3=1.2, color="#242B32"
        )
