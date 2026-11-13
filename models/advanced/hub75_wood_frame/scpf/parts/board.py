"""Generic rectangular wooden board component."""

from scpf import AnchorTopology, Direction, Edges, Polygon2D, component, pv


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

    def anchors(self):
        """Topology-backed top/bottom corner datums for assembly joints.

        These picks deliberately use the horizontal top/bottom face as the
        anchor face. Its normal is therefore vertical, so a native joint gap
        can express an associative vertical offset from the side board.
        """
        width = pv(self.width)
        depth = pv(self.depth)
        height = pv(self.height)
        center_x = pv(self.x_position)
        front = pv(self.y_position)
        rear = front + depth
        bottom = pv(self.z_position)
        top = bottom + height

        left = center_x - width / 2
        right = center_x + width / 2
        mid_y = (front + rear) / 2

        def corner_anchor(*, z, y, x, top_face, left_side):
            return AnchorTopology(
                edge=(center_x, y, z),
                on=(center_x, mid_y, z),
                corner=(x, y, z),
                z=(0, 0, 1 if top_face else -1),
                x=(1 if left_side else -1, 0, 0),
            )

        return {
            "bottom_front_left": corner_anchor(
                z=bottom, y=front, x=left,
                top_face=False, left_side=True,
            ),
            "bottom_front_right": corner_anchor(
                z=bottom, y=front, x=right,
                top_face=False, left_side=False,
            ),
            "bottom_back_left": corner_anchor(
                z=bottom, y=rear, x=left,
                top_face=False, left_side=True,
            ),
            "bottom_back_right": corner_anchor(
                z=bottom, y=rear, x=right,
                top_face=False, left_side=False,
            ),
            "top_front_left": corner_anchor(
                z=top, y=front, x=left,
                top_face=True, left_side=True,
            ),
            "top_front_right": corner_anchor(
                z=top, y=front, x=right,
                top_face=True, left_side=False,
            ),
            "top_back_left": corner_anchor(
                z=top, y=rear, x=left,
                top_face=True, left_side=True,
            ),
            "top_back_right": corner_anchor(
                z=top, y=rear, x=right,
                top_face=True, left_side=False,
            ),
        }

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
