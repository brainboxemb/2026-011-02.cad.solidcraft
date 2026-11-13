"""Generic rectangular wooden board component."""

from scpf import Direction, Edges, Polygon2D, component, pv


@component
class Board:
    width = 100.0
    depth = 100.0
    height = 100.0
    x_position = 0.0
    y_position = 0.0
    z_position = 0.0
    corner_radius = 0.0

    # Build-only role details. They are deliberately not SolidCraft parameters.
    fillet = None
    material_name = None
    color = None

    def build(self):
        half = self.width / 2
        center = self.width * 0 + self.x_position
        left = center - half
        right = center + half
        bottom = self.z_position
        top = bottom + self.height

        profile = Polygon2D([
            ("lower_left", (left, bottom)),
            ("lower_right", (right, bottom)),
            ("upper_right", (right, top)),
            ("upper_left", (left, top)),
        ], plane="XZ", world=True).at(y=self.y_position)

        body = profile.extrude(
            self.depth,
            direction=Direction.POSITIVE,
        )

        if self.fillet is not None and pv(self.corner_radius) > 0:
            vertices = {
                "bottom": ("lower_left", "lower_right"),
                "top": ("upper_left", "upper_right"),
            }
            try:
                selected = vertices[self.fillet]
            except KeyError as exc:
                raise ValueError(
                    "Board fillet must be 'top', 'bottom' or None"
                ) from exc
            body = body.fillet(
                self.corner_radius,
                edges=Edges.from_vertices(*selected),
            )

        return body.with_material(
            self.material_name or "LIGHTPLY",
            density_g_cm3=0.55,
            color=self.color or "#CBA36B",
        )
