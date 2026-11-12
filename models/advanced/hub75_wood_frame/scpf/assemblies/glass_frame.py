"""Four-piece mitred glazing-frame subassembly."""

from scpf import assembly

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
        opening_half_width = self.opening_width / 2

        bottom = GlassStrip(
            length=self.opening_width,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            _x_position=0,
            _z_position=opening_bottom,
            _vertical=0,
            _width_sign=1,
            _finish=0,
        )

        top = GlassStrip(
            length=self.opening_width,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            _x_position=0,
            _z_position=opening_top,
            _vertical=0,
            _width_sign=-1,
            _finish=0,
        )

        left = GlassStrip(
            length=self.opening_height,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            _x_position=-opening_half_width,
            _z_position=opening_center_z,
            _vertical=1,
            _width_sign=1,
            _finish=1,
        )

        right = GlassStrip(
            length=self.opening_height,
            width=self.glazing_wood_width,
            depth=self.glazing_wood_depth,
            _x_position=opening_half_width,
            _z_position=opening_center_z,
            _vertical=1,
            _width_sign=-1,
            _finish=1,
        )

        return (bottom + top + left + right).group("WoodGlassFrame")
