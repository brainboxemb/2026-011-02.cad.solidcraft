"""Fixed-size plexiglass window, vertically centred in the opening."""

from scpf import Direction, Polygon2D, Sketch, component


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
        half_width = GLASS_WIDTH / 2
        bottom = (
            self.opening_bottom_z
            + (self.opening_height - GLASS_HEIGHT) / 2
        )
        top = bottom + GLASS_HEIGHT

        with Sketch(
            name="Profile",
            plane="XZ",
            offset=self.front_y,
        ) as sketch:
            Polygon2D([
                (-half_width, bottom),
                (half_width, bottom),
                (half_width, top),
                (-half_width, top),
            ], plane="XZ", world=True)

        return sketch.extrude(
            GLASS_THICKNESS,
            direction=Direction.POSITIVE,
        ).with_material(
            "Plexiglass",
            density_g_cm3=1.19,
            color="#B7DAEF",
        )
