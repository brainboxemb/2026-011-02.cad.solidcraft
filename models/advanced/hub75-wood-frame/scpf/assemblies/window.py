"""Window occurrence placement."""

from scpf import component, pv

from parts.window import Window


WindowPart = component(Window)


def build_window(
    *,
    glass_width,
    glass_height,
    glass_thickness,
    glass_bottom_clearance,
    frame_front_y,
    glazing_depth,
):
    width = pv(glass_width)
    height = pv(glass_height)
    thickness = pv(glass_thickness)
    bottom = pv(glass_bottom_clearance)
    front = pv(frame_front_y)
    trim_depth = pv(glazing_depth)

    glass_front = front + trim_depth
    return WindowPart(
        width=width,
        height=height,
        thickness=thickness,
    ).move(
        y=glass_front + thickness / 2,
        z=bottom,
    )
