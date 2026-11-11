"""Lightweight HUB75 placement envelope for large wooden-box assemblies.

No native loft, cutouts, rear PCB, or mounting bores: this component only
occupies the measured external bounding volume. Use Hub75Panel (advanced)
from models.components.hub75 when designing module clamps and interfaces.
"""
from scpf import Box


class Hub75PanelBasic:
    width = 159.70
    height = 319.71
    depth = 14.50

    def build(self):
        return Box(self.width, self.height, self.depth).with_material(
            "LED panel envelope", density_g_cm3=1.2, color="#242B32"
        )
