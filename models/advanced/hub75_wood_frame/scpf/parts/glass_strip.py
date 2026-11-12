"""Simple pine glazing retainer with two 45-degree mitred ends."""

from scpf import Polygon2D, component, pv


@component
class GlassStrip:
    """One strip type for all four sides of the glazing frame."""

    length = 844.0
    width = 12.0
    depth = 12.0

    # Parent-owned placement/orientation inputs. These stay private when the
    # strip is used by itself, but parent Parameter/Expression bindings remain
    # symbolic when GlassFrame positions the four manufactured pieces.
    _x_position = 0.0
    _y_position = 0.0
    _z_position = 0.0
    _vertical = 0
    _width_sign = 1
    _finish = 0

    def build(self):
        if not 0 < pv(self.width) < pv(self.length) / 2:
            raise ValueError("GlassStrip width must be less than half its length")

        half = self.length / 2
        start = -half
        end = half
        inner_start = start + self.width
        inner_end = end - self.width

        def placed(along, across):
            if pv(self._vertical):
                return (
                    self._x_position + across * self._width_sign,
                    self._z_position + along,
                )
            return (
                self._x_position + along,
                self._z_position + across * self._width_sign,
            )

        # A glazing strip is just one rectangular strip whose two ends are
        # mitred at 45 degrees. The four-point XZ profile keeps parent-owned
        # placement symbolic; extrusion is always straight towards +Y.
        profile = Polygon2D([
            placed(start, 0),
            placed(end, 0),
            placed(inner_end, self.width),
            placed(inner_start, self.width),
        ], plane="XZ", world=True).at(y=self._y_position)

        dark = pv(self._finish) >= 0.5
        return profile.extrude(self.depth).with_material(
            "PINE glazing vertical" if dark else "PINE glazing horizontal",
            density_g_cm3=0.55,
            color="#A9793E" if dark else "#E3BF80",
        )
