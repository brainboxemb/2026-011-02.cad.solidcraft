"""Lightweight HUB75 placement envelope for large wooden-box assemblies.

No native loft, cutouts, rear PCB, or mounting bores: this component only
occupies the measured external bounding volume. The basic representation
stands upright in XZ (Z is world up, Y is front-to-back). Use Hub75Panel
(advanced) from components.hub75 for real module mounting details.
"""
from scpf import Box


class Hub75PanelBasic:
    width = 159.70
    height = 319.71
    depth = 14.50

    def build(self):
        return Box(self.width, self.depth, self.height).with_material(
            "LED panel envelope", density_g_cm3=1.2, color="#242B32"
        )
