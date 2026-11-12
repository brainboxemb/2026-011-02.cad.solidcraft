"""Fixed-size plexiglass window, positioned from assembly parameters."""

from scpf import Direction, Polygon2D, component


GLASS_WIDTH = 840.0
GLASS_HEIGHT = 360.0
GLASS_THICKNESS = 4.0


@component
class Window:
    """Fixed plexiglass sheet kept centred inside the opening."""

    opening_height = 362.0
    glazing_wood_depth = 12.0

    def build(self):
        bottom = (self.opening_height - GLASS_HEIGHT) / 2
        top = bottom + GLASS_HEIGHT
        front = self.glazing_wood_depth
        rear = front + GLASS_THICKNESS

        profile = Polygon2D([
            (front, bottom),
            (rear, bottom),
            (rear, top),
            (front, top),
        ], plane="YZ", world=True)

        return profile.extrude(
            GLASS_WIDTH,
            direction=Direction.SYMMETRIC,
        ).with_material(
            "Plexiglass",
            density_g_cm3=1.19,
            color="#B7DAEF",
        )
