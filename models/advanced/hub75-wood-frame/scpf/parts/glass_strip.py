"""Mitred wooden glazing retainer."""

from scpf import Direction, Polygon2D, component, pv


@component
class GlassStrip:
    """One strip type for both horizontal and vertical retainers."""

    length = 844.0
    width = 12.0
    depth = 12.0
    length_center = 0.0
    width_base = 0.0
    finish = 0

    def build(self):
        if not 0 < pv(self.width) < pv(self.length) / 2:
            raise ValueError("GlassStrip width must be less than half its length")

        half = self.length / 2
        start = self.length_center - half
        end = self.length_center + half
        inner_start = start + self.width
        inner_end = end - self.width
        outer = self.width_base
        inner = outer + self.width

        profile = Polygon2D([
            (start, outer),
            (end, outer),
            (inner_end, inner),
            (inner_start, inner),
        ], plane="XZ", world=True)

        dark = pv(self.finish) >= 0.5
        return profile.extrude(
            self.depth,
            direction=Direction.SYMMETRIC,
        ).with_material(
            "LIGHTPLY glazing vertical" if dark else "LIGHTPLY glazing horizontal",
            density_g_cm3=0.55,
            color="#A9793E" if dark else "#E3BF80",
        )
