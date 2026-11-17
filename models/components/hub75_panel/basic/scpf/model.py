"""Lightweight HUB75 placement envelope for large wooden-box assemblies.

No native loft, cutouts, rear PCB, or mounting bores: this component only
occupies the measured external bounding volume. The dimensions are fixed
product constants; occurrence placement belongs to the owning assembly.
"""
from scpf import Direction, Polygon2D, Sketch, component, half


HUB75_PANEL_WIDTH = 159.70
HUB75_PANEL_HEIGHT = 319.71
HUB75_PANEL_DEPTH = 14.50


@component
class Hub75PanelBasic:
    def build(self):
        half_width = half(HUB75_PANEL_WIDTH)

        with Sketch(
            name="Profile",
            plane="XZ",
        ) as sketch:
            Polygon2D([
                (-half_width, 0),
                (half_width, 0),
                (half_width, HUB75_PANEL_HEIGHT),
                (-half_width, HUB75_PANEL_HEIGHT),
            ], plane="XZ", world=True)

        return sketch.extrude(HUB75_PANEL_DEPTH, sym=True).with_material(
            "LED panel envelope", density_g_cm3=1.2, color="#242B32"
        )
