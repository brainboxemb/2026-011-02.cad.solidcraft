"""Shared board geometry plus semantic wooden case parts."""

from scpf import Direction, Edges, Polygon2D, component, pv


class SideBoard:
    thickness = 12.0
    depth = 100.0
    height = 362.0
    x_position = 0.0
    y_position = 0.0
    z_position = 0.0

    def build(self):
        return _build_board(
            width=self.thickness,
            depth=self.depth,
            height=self.height,
            x_position=self.x_position,
            y_position=self.y_position,
            z_position=self.z_position,
            material_name="LIGHTPLY side board",
        )


@component
class LeftBoard(SideBoard):
    pass


@component
class RightBoard(SideBoard):
    pass


@component
class BottomBoard:
    width = 868.0
    depth = 100.0
    thickness = 12.0
    y_position = 0.0
    corner_radius = 4.0

    def build(self):
        return _build_board(
            width=self.width,
            depth=self.depth,
            height=self.thickness,
            y_position=self.y_position,
            corner_radius=self.corner_radius,
            fillet_vertices=("lower_left", "lower_right"),
            material_name="LIGHTPLY bottom",
        )


@component
class RoofBoard:
    width = 868.0
    depth = 120.0
    thickness = 12.0
    y_position = -10.0
    z_position = 362.0
    corner_radius = 4.0

    def build(self):
        return _build_board(
            width=self.width,
            depth=self.depth,
            height=self.thickness,
            y_position=self.y_position,
            z_position=self.z_position,
            corner_radius=self.corner_radius,
            fillet_vertices=("upper_left", "upper_right"),
            material_name="LIGHTPLY roof",
        )


@component
class BackBoard:
    width = 868.0
    height = 374.0
    thickness = 9.0
    y_position = 100.0

    def build(self):
        return _build_board(
            width=self.width,
            depth=self.thickness,
            height=self.height,
            y_position=self.y_position,
            material_name="LIGHTPLY rear",
            color="#A87D4D",
        )


def _build_board(
    width, depth, height, *,
    x_position=0.0,
    y_position=0.0,
    z_position=0.0,
    corner_radius=0.0,
    fillet_vertices=(),
    material_name="LIGHTPLY",
    density_g_cm3=0.55,
    color="#CBA36B",
):
    """Build one rectangular XZ board from a world-Y datum plane."""
    half = width / 2
    center = width * 0 + x_position
    left = center - half
    right = center + half
    bottom = z_position
    top = bottom + height
    profile = Polygon2D([
        ("lower_left", (left, bottom)),
        ("lower_right", (right, bottom)),
        ("upper_right", (right, top)),
        ("upper_left", (left, top)),
    ], plane="XZ", world=True).at(y=y_position)
    body = profile.extrude(
        depth,
        direction=Direction.POSITIVE,
    )
    if fillet_vertices and pv(corner_radius) > 0:
        body = body.fillet(
            corner_radius,
            edges=Edges.from_vertices(*fillet_vertices),
        )
    return body.with_material(
        material_name,
        density_g_cm3=density_g_cm3,
        color=color,
    )
