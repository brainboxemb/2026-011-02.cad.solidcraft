"""Fixed plexiglass window part."""

from scpf import Box


GLASS_WIDTH = 840.0
GLASS_HEIGHT = 360.0
GLASS_THICKNESS = 4.0
GLASS_BOTTOM_CLEARANCE = 1.0


class Window:
    """Fixed plexiglass sheet used by this display."""

    def build(self):
        return Box(
            GLASS_WIDTH,
            GLASS_THICKNESS,
            GLASS_HEIGHT,
        ).with_material(
            "Plexiglass",
            density_g_cm3=1.19,
            color="#B7DAEF",
        )
