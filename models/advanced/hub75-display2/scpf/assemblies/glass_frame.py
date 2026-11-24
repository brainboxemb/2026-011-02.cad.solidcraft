"""Four-piece mitred glazing-frame subassembly."""

from scpf import X, Y, Placement, assembly, half, midpoint

from parts.glass_strip import GlassStrip


@assembly
class GlassFrame:
    opening_width = 844.0
    opening_height = 362.0
    opening_bottom_z = 12.0
    glazing_wood_width = 12.0
    glazing_wood_depth = 12.0

    def build(self):
        opening_bottom = self.opening_bottom_z
        opening_top = opening_bottom + self.opening_height
        opening_center_z = midpoint(opening_bottom, opening_top)

        bottom = GlassStrip(
            length=self.opening_width,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            material_name="PINE glazing horizontal",
            color="#E3BF80",
            placement=Placement(z=opening_bottom),
        )

        top = GlassStrip(
            length=self.opening_width,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            material_name="PINE glazing horizontal",
            color="#E3BF80",
            placement=Placement(
                y=self.glazing_wood_depth,
                z=opening_top,
                rotation=(X, 180),
            ),
        )

        left = GlassStrip(
            length=self.opening_height,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            material_name="PINE glazing vertical",
            color="#A9793E",
            placement=Placement(
                x=-half(self.opening_width),
                z=opening_center_z,
                rotation=(Y, 90),
            ),
        )

        right = GlassStrip(
            length=self.opening_height,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            material_name="PINE glazing vertical",
            color="#A9793E",
            placement=Placement(
                x=half(self.opening_width),
                z=opening_center_z,
                rotation=(Y, -90),
            ),
        )

        return (bottom + top + left + right).group("WoodGlassFrame")
