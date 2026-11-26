"""Shared source geometry for HUB75 tube-clamp interface variants."""

from math import cos, radians, sin

from scpf import Sketch


# Physical dimensions shared by the female-slot and male-dovetail variants.
CLAMP_WALL = 2.0
CLAMP_WIDTH = 12.0
CLAMP_OPEN = 90.0

DOVE_RUN = 16.0
DOVE_HEAD = 12.0
DOVE_DEPTH = 2.05
DOVE_ANGLE = 45.0
DOVE_LAND_ROOT = 0.65
DOVE_LAND_HEAD = 0.8
DOVE_ROUND = 0.2
DOVE_GROOVE_FLAT = 0.4


def _open_clamp_ring(*, clamp_r, clamp_r_out):
    """Features 1/2: shared open elastic clamp ring in the native XY frame."""
    half_open = radians(CLAMP_OPEN / 2.0)
    radial_mid = (clamp_r + clamp_r_out) / 2.0

    outer_x = clamp_r_out * cos(half_open)
    outer_y = clamp_r_out * sin(half_open)
    inner_x = clamp_r * cos(half_open)
    inner_y = clamp_r * sin(half_open)
    lip_center_x = radial_mid * cos(half_open)
    lip_center_y = radial_mid * sin(half_open)

    with Sketch(
        name="Open klemring met afgeronde lippen",
        plane="XY",
        offset=-CLAMP_WIDTH / 2.0,
    ) as sketch:
        profile = sketch.profile(start=(outer_x, outer_y))
        profile.arc_center_to(
            (outer_x, -outer_y),
            center=(0.0, 0.0),
            clockwise=False,
        )
        profile.arc_center_to(
            (inner_x, -inner_y),
            center=(lip_center_x, -lip_center_y),
            clockwise=False,
        )
        profile.arc_center_to(
            (inner_x, inner_y),
            center=(0.0, 0.0),
            clockwise=True,
        )
        profile.arc_center_to(
            (outer_x, outer_y),
            center=(lip_center_x, lip_center_y),
            clockwise=False,
        )
        profile.close()

    return sketch
