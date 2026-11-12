"""Four-piece mitred glazing-frame subassembly."""

from scpf import X, Y, assembly

from parts.glass_strip import GlassStrip


@assembly
class GlassFrame:
    opening_width = 844.0
    opening_height = 362.0
    opening_bottom_z = 12.0
    glazing_wood_width = 12.0
    _glazing_wood_depth = 12.0

    def build(self):
        trim_y = self._glazing_wood_depth / 2
        opening_bottom = self.opening_bottom_z
        opening_top = opening_bottom + self.opening_height

        bottom = GlassStrip(
            length=self.opening_width,
            width=self.glazing_wood_width,
            depth=self._glazing_wood_depth,
            length_center=0,
            width_base=opening_bottom,
            finish=0,
        ).move(y=trim_y)

        top = GlassStrip(
            length=self.opening_width,
            width=self.glazing_wood_width,
            depth=self._glazing_wood_depth,
            length_center=0,
            width_base=-opening_top,
            finish=0,
        ).rotate(X, 180).move(y=trim_y)

        left = GlassStrip(
            length=self.opening_height,
            width=self.glazing_wood_width,
            depth=self._glazing_wood_depth,
            length_center=-(self.opening_height / 2) - opening_bottom,
            width_base=-(self.opening_width / 2),
            finish=1,
        ).rotate(Y, 90).move(y=trim_y)

        right = GlassStrip(
            length=self.opening_height,
            width=self.glazing_wood_width,
            depth=self._glazing_wood_depth,
            length_center=self.opening_height / 2 + opening_bottom,
            width_base=-(self.opening_width / 2),
            finish=1,
        ).rotate(Y, -90).move(y=trim_y)

        return (bottom + top + left + right).group("WoodGlassFrame")
