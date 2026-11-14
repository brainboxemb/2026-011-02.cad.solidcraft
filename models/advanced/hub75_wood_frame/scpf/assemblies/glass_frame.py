"""Four-piece mitred glazing-frame subassembly."""

from scpf import X, Y, assembly

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
        opening_center_z = opening_bottom + self.opening_height / 2

        bottom = GlassStrip(
            length=self.opening_width,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            material_name="PINE glazing horizontal",
            color="#E3BF80",
        )
        bottom = bottom.move(
            0,
            0,
            opening_bottom,
        )

        top = GlassStrip(
            length=self.opening_width,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            material_name="PINE glazing horizontal",
            color="#E3BF80",
        )
        top = top.rotate(X, 180).move(
            0,
            self.glazing_wood_depth,
            opening_top,
        )

        left = GlassStrip(
            length=self.opening_height,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            material_name="PINE glazing vertical",
            color="#A9793E",
        )
        left = left.rotate(Y, 90).move(
            -(self.opening_width / 2),
            0,
            opening_center_z,
        )

        right = GlassStrip(
            length=self.opening_height,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            material_name="PINE glazing vertical",
            color="#A9793E",
        )
        right = right.rotate(Y, -90).move(
            self.opening_width / 2,
            0,
            opening_center_z,
        )

        return (bottom + top + left + right).group("WoodGlassFrame")
