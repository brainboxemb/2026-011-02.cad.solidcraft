"""Mitred wooden glazing retainer."""

from scpf import Polygon2D, Sketch, component, half


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
        # length and width remain native editable parameters. A Python pv()
        # check would validate only the initial Forge run, not later edits in
        # the saved SolidCraft design, so geometry keeps the values symbolic.
        half_length = half(self.length)
        start = -half_length
        end = half_length
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
