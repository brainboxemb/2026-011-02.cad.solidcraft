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
        """Topology-backed corner frames on the four vertical board edges.

        The pick coordinates select native SolidCraft topology only. SolidCraft
        keeps the selected edge/corner by name, so these anchors follow width,
        depth, height and position changes in the saved design.

        The frame Z axis is deliberately vertical:
          bottom anchors: +Z
          top anchors:    -Z
        Left/right X points inward from the outside edge. Assemblies can then
        use a native joint offset along Z without freezing a world coordinate.
        """
        width = pv(self.width)
        depth = pv(self.depth)
        height = pv(self.height)
        cx = pv(self.x_position)
        y0 = pv(self.y_position)
        z0 = pv(self.z_position)

        xmin = cx - width / 2
        xmax = cx + width / 2
        xmid = cx
        y1 = y0 + depth
        z1 = z0 + height
        zmid = (z0 + z1) / 2

        def vertical(x, y, z, frame_z, frame_x):
            return AnchorTopology(
                edge=(x, y, zmid),
                on=(xmid, y, zmid),
                corner=(x, y, z),
                z=frame_z,
                x=frame_x,
            )

        return {
            "front_bottom_left_vertical": vertical(
                xmin, y0, z0, (0, 0, 1), (1, 0, 0)
            ),
            "front_top_left_vertical": vertical(
                xmin, y0, z1, (0, 0, -1), (1, 0, 0)
            ),
            "front_bottom_right_vertical": vertical(
                xmax, y0, z0, (0, 0, 1), (-1, 0, 0)
            ),
            "front_top_right_vertical": vertical(
                xmax, y0, z1, (0, 0, -1), (-1, 0, 0)
            ),
            "back_bottom_left_vertical": vertical(
                xmin, y1, z0, (0, 0, 1), (1, 0, 0)
            ),
            "back_top_left_vertical": vertical(
                xmin, y1, z1, (0, 0, -1), (1, 0, 0)
            ),
            "back_bottom_right_vertical": vertical(
                xmax, y1, z0, (0, 0, 1), (-1, 0, 0)
            ),
            "back_top_right_vertical": vertical(
                xmax, y1, z1, (0, 0, -1), (-1, 0, 0)
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
