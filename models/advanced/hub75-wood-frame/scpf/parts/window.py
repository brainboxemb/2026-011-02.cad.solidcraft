"""Fixed-size plexiglass window with parametric vertical centring."""

from scpf import Direction, Polygon2D, component


GLASS_WIDTH = 840.0
GLASS_HEIGHT = 360.0
GLASS_THICKNESS = 4.0


@component
class Window:
    """Fixed plexiglass sheet kept centred inside the opening."""

    opening_height = 362.0

    def build(self):
        half_width = GLASS_WIDTH / 2
        bottom = (self.opening_height - GLASS_HEIGHT) / 2
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
