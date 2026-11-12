"""Lightweight HUB75 placement envelope for large wooden-box assemblies.

No native loft, cutouts, rear PCB, or mounting bores: this component only
occupies the measured external bounding volume. The basic representation
stands upright in XZ (Z is world up, Y is front-to-back). Use Hub75Panel
(advanced) from components.hub75 for real module mounting details.
"""
from scpf import Box


HUB75_PANEL_WIDTH = 159.70
HUB75_PANEL_HEIGHT = 319.71
HUB75_PANEL_DEPTH = 14.50


class Hub75PanelBasic:
    def build(self):
        return Box(
            HUB75_PANEL_WIDTH,
            HUB75_PANEL_DEPTH,
            HUB75_PANEL_HEIGHT,
        ).with_material(
            "LED panel envelope", density_g_cm3=1.2, color="#242B32"
        )
