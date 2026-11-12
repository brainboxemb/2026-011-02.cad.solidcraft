"""Four-piece mitred glazing-frame subassembly."""

from scpf import component, pv

from parts.glass_strip import GlassStrip


Strip = component(GlassStrip)


def build_glass_frame(
    *,
    opening_width,
    opening_height,
    frame_front_y,
    glazing_width,
    glazing_depth,
):
    width = pv(opening_width)
    height = pv(opening_height)
    front = pv(frame_front_y)
    trim_width = pv(glazing_width)
    trim_depth = pv(glazing_depth)
    trim_y = front + trim_depth / 2

    horizontal = Strip(
        length=width,
        width=trim_width,
        depth=trim_depth,
        finish=0,
    )
    bottom = horizontal.move(y=trim_y)
    top = horizontal.copy().rotate(
        axis=(1, 0, 0),
        degrees=180,
    ).move(
        y=trim_y,
        z=height,
    )

    vertical = Strip(
        length=height,
        width=trim_width,
        depth=trim_depth,
        finish=1,
    )
    left = vertical.rotate(
        axis=(0, 1, 0),
        degrees=90,
    ).move(
        x=-width / 2,
        y=trim_y,
        z=height / 2,
    )
    right = vertical.copy().rotate(
        axis=(0, 1, 0),
        degrees=-90,
    ).move(
        x=width / 2,
        y=trim_y,
        z=height / 2,
    )

    return (bottom + top + left + right).group("WoodGlassFrame")
