"""Four-piece mitred glazing-frame subassembly."""

from scpf import assembly

from parts.glass_strip import GlassStrip


@assembly
class GlassFrame:
    opening_width = 844.0
    opening_height = 362.0
    frame_front_y = -25.0
    glazing_width = 15.0
    glazing_depth = 15.0

    def build(self):
        trim_y = self.frame_front_y + self.glazing_depth / 2

        horizontal = GlassStrip(
            length=self.opening_width,
            width=self.glazing_width,
            depth=self.glazing_depth,
            finish=0,
        )
        bottom = horizontal.move(y=trim_y)
        top = horizontal.copy().rotate(
            axis=(1, 0, 0),
            degrees=180,
        ).move(
            y=trim_y,
            z=self.opening_height,
        )

        vertical = GlassStrip(
            length=self.opening_height,
            width=self.glazing_width,
            depth=self.glazing_depth,
            finish=1,
        )
        left = vertical.rotate(
            axis=(0, 1, 0),
            degrees=90,
        ).move(
            x=-self.opening_width / 2,
            y=trim_y,
            z=self.opening_height / 2,
        )
        right = vertical.copy().rotate(
            axis=(0, 1, 0),
            degrees=-90,
        ).move(
            x=self.opening_width / 2,
            y=trim_y,
            z=self.opening_height / 2,
        )

        return (bottom + top + left + right).group("WoodGlassFrame")
