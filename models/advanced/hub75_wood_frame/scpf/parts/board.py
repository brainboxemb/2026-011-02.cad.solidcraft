"""Generic rectangular wooden board component."""

from scpf import BOTTOM, FRONT, Box, component


@component
class Board:
    width = 100.0
    depth = 100.0
    height = 100.0
    corner_radius = 0.0

    # Build-only role details. They are deliberately not SolidCraft parameters.
    fillet = None
    material_name = None
    color = None

    def build(self):
        body = Box(
            self.width,
            self.depth,
            self.height,
        ).at(
            0,
            0,
            0,
            anchor=FRONT + BOTTOM,
        )

        if self.fillet:
            body = body.fillet(
                self.corner_radius,
                edges=self.fillet,
            )

        return body.with_material(
            self.material_name or "LIGHTPLY",
            density_g_cm3=0.55,
            color=self.color or "#CBA36B",
        )
