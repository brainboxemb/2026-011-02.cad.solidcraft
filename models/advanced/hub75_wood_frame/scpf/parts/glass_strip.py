"""Mitred wooden glazing retainer."""

from scpf import Polygon2D, Sketch, component, pv


@component
class GlassStrip:
    """One neutral mitred glazing strip in local coordinates."""

    length = 844.0
    width = 12.0
    depth = 12.0

    # Build-only appearance details.
    material_name = None
    color = None

    def build(self):
        if not 0 < pv(self.width) < pv(self.length) / 2:
            raise ValueError("GlassStrip width must be less than half its length")

        half = self.length / 2
        start = -half
        end = half
        inner_start = start + self.width
        inner_end = end - self.width

        with Sketch(name="Profile", plane="XZ") as sketch:
            Polygon2D([
                (start, 0),
                (end, 0),
                (inner_end, self.width),
                (inner_start, self.width),
            ], plane="XZ", world=True)

        return sketch.extrude(
            self.depth,
        ).with_material(
            self.material_name or "PINE glazing",
            density_g_cm3=0.55,
            color=self.color or "#E3BF80",
        )
