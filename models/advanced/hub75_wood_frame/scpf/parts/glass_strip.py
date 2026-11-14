"""Mitred wooden glazing retainer."""

from scpf import Direction, Polygon2D, Sketch, component, pv


@component
class GlassStrip:
    """One strip type for both horizontal and vertical retainers."""

    length = 844.0
    width = 12.0
    depth = 12.0
    _length_center = 0.0
    _width_base = 0.0
    _finish = 0
    _depth_sign = 1

    def build(self):
        if not 0 < pv(self.width) < pv(self.length) / 2:
            raise ValueError("GlassStrip width must be less than half its length")

        half = self.length / 2
        zero = self.length * 0
        center = zero + self._length_center
        outer = zero + self._width_base

        start = center - half
        end = center + half
        inner_start = start + self.width
        inner_end = end - self.width
        inner = outer + self.width

        with Sketch(name="Profile", plane="XZ") as sketch:
            Polygon2D([
                (start, outer),
                (end, outer),
                (inner_end, inner),
                (inner_start, inner),
            ], plane="XZ", world=True)

        dark = pv(self._finish) >= 0.5
        direction = (
            Direction.NEGATIVE
            if pv(self._depth_sign) < 0
            else Direction.POSITIVE
        )
        return sketch.extrude(
            self.depth,
            direction=direction,
        ).with_material(
            "PINE glazing vertical" if dark else "PINE glazing horizontal",
            density_g_cm3=0.55,
            color="#A9793E" if dark else "#E3BF80",
        )
