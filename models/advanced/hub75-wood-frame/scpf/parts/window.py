"""Fixed plexiglass window with fixed dimensions and Z position."""

from scpf import Direction, Polygon2D, component


GLASS_WIDTH = 840.0
GLASS_HEIGHT = 360.0
GLASS_THICKNESS = 4.0
GLASS_BOTTOM_CLEARANCE = 1.0


@component
class Window:
    """Fixed plexiglass sheet independent of the adjustable opening height."""

    def build(self):
        half_width = GLASS_WIDTH / 2
        bottom = GLASS_BOTTOM_CLEARANCE
        top = bottom + GLASS_HEIGHT

        profile = Polygon2D([
            (-half_width, bottom),
            (half_width, bottom),
            (half_width, top),
            (-half_width, top),
        ], plane="XZ", world=True)

        return profile.extrude(
            GLASS_THICKNESS,
            direction=Direction.SYMMETRIC,
        ).with_material(
            "Plexiglass",
            density_g_cm3=1.19,
            color="#B7DAEF",
        )
