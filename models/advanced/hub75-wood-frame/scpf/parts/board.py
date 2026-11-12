"""Shared board geometry plus semantic wooden case parts."""

from scpf import Direction, Edges, Polygon2D, component, pv


class Board:
    """One rectangular board extruded symmetrically through local Y."""

    def __init__(
        self, width, depth, height, *,
        z_position=0.0,
        corner_radius=0.0,
        fillet_vertices=(),
        material_name="LIGHTPLY",
        density_g_cm3=0.55,
        color="#CBA36B",
    ):
        self.width = width
        self.depth = depth
        self.height = height
        self.z_position = z_position
        self.corner_radius = corner_radius
        self.fillet_vertices = tuple(fillet_vertices)
        self.material_name = material_name
        self.density_g_cm3 = density_g_cm3
        self.color = color

    def build(self):
        half = self.width / 2
        bottom = self.z_position
        top = bottom + self.height
        profile = Polygon2D([
            ("lower_left", (-half, bottom)),
            ("lower_right", (half, bottom)),
            ("upper_right", (half, top)),
            ("upper_left", (-half, top)),
        ], plane="XZ", world=True)
        body = profile.extrude(
            self.depth,
            direction=Direction.SYMMETRIC,
        )
        if self.fillet_vertices and pv(self.corner_radius) > 0:
            body = body.fillet(
                self.corner_radius,
                edges=Edges.from_vertices(*self.fillet_vertices),
            )
        return body.with_material(
            self.material_name,
            density_g_cm3=self.density_g_cm3,
            color=self.color,
        )


class SideBoard:
    thickness = 12.0
    depth = 100.0
    height = 362.0

    def build(self):
        return Board(
            width=self.thickness,
            depth=self.depth,
            height=self.height,
            material_name="LIGHTPLY side board",
        ).build()


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
    corner_radius = 4.0

    def build(self):
        return Board(
            width=self.width,
            depth=self.depth,
            height=self.thickness,
            corner_radius=self.corner_radius,
            fillet_vertices=("lower_left", "lower_right"),
            material_name="LIGHTPLY bottom",
        ).build()


@component
class RoofBoard:
    width = 868.0
    depth = 120.0
    thickness = 12.0
    z_position = 362.0
    corner_radius = 4.0

    def build(self):
        return Board(
            width=self.width,
            depth=self.depth,
            height=self.thickness,
            z_position=self.z_position,
            corner_radius=self.corner_radius,
            fillet_vertices=("upper_left", "upper_right"),
            material_name="LIGHTPLY roof",
        ).build()


@component
class BackBoard:
    width = 868.0
    height = 374.0
    thickness = 9.0

    def build(self):
        return Board(
            width=self.width,
            depth=self.thickness,
            height=self.height,
            material_name="LIGHTPLY rear",
            color="#A87D4D",
        ).build()
