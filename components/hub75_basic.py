"""Lightweight HUB75 placement envelope for large wooden-box assemblies.

No native loft, cutouts, rear PCB, or mounting bores: this component only
occupies the measured external bounding volume. The dimensions are fixed
product constants; depth and vertical placement may be linked to parent parameters.
"""
from scpf import Direction, Polygon2D


HUB75_PANEL_WIDTH = 159.70
HUB75_PANEL_HEIGHT = 319.71
HUB75_PANEL_DEPTH = 14.50


class Hub75PanelBasic:
    y_center = 0.0
    z_position = 0.0

    def build(self):
        half_width = HUB75_PANEL_WIDTH / 2
        bottom = self.z_position
        top = bottom + HUB75_PANEL_HEIGHT

        profile = Polygon2D([
            (-half_width, bottom),
            (half_width, bottom),
            (half_width, top),
            (-half_width, top),
        ], plane="XZ", world=True).at(y=self.y_center)

        return profile.extrude(
            HUB75_PANEL_DEPTH,
            direction=Direction.SYMMETRIC,
        ).with_material(
            "LED panel envelope", density_g_cm3=1.2, color="#242B32"
        )
