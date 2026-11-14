"""Fixed-size plexiglass window, vertically centred in the opening."""

from scpf import BOTTOM, FRONT, Box, component


GLASS_WIDTH = 840.0
GLASS_HEIGHT = 360.0
GLASS_THICKNESS = 4.0


@component
class Window:
    """Fixed plexiglass sheet whose position follows the opening centre."""

    opening_height = 362.0
    opening_bottom_z = 12.0
    front_y = 12.0

    def build(self):
        bottom = (
            self.opening_bottom_z
            + (self.opening_height - GLASS_HEIGHT) / 2
        )

        return Box(
            GLASS_WIDTH,
            GLASS_THICKNESS,
            GLASS_HEIGHT,
        ).at(
            0,
            self.front_y,
            bottom,
            anchor=FRONT + BOTTOM,
        ).with_material(
            "Plexiglass",
            density_g_cm3=1.19,
            color="#B7DAEF",
        )
