"""Corner HUB75 frame-coupler implementation and tube variants."""

from dataclasses import dataclass

from scpf import component

from models.components.hub75_frame_coupler.scpf.features import (
    CLAMP_FOOT_CLEARANCE_WIDTH,
    CLAMP_FOOT_CLEARANCE_Y_REAR,
    CLAMP_FOOT_CLEARANCE_Z,
    CORNER_CLAMP_FOOT_CLEARANCE_Y_FRONT,
    CORNER_LEFT_RAIL_CENTER,
    CORNER_RIGHT_RAIL_CENTER,
    RAIL_ENTRY_CHAMFER,
    RAIL_ENTRY_CHAMFER_SECONDARY,
    RAIL_HEIGHT,
    RAIL_PLANE_Z,
    TUBE_AXIS_Y,
    TUBE_AXIS_Z,
    TUBE_CLEARANCE_DIAMETER,
    TUBE_CLEARANCE_LENGTH,
    _add_receiver_interface,
    _axis_x_cylinder,
    _cut_edge_like_base,
    _cut_panel_pin_pass_through,
    _cut_tapered_rail_relief,
    _edge_like_stock,
    _edge_support_z,
    _guide_clearance,
    _locator_pad,
    _rail_entry_edges,
    _rail_xy,
    _rectangle_xy,
    _xy_profile_solid,
)
from models.components.hub75_frame_coupler.scpf.parameters import (
    SOURCE_RED,
    _CONFIGURED_PARAMETERS,
    _ConfiguredCouplerRoot,
    _parameters,
)


def _build_corner_body(
    *,
    p,
    profile_key,
    relief_key,
    screw_x,
    reference_ticks=False,
    reference_holes=False,
):
    """Build one configured left/right Corner body."""
    screw_xs = (screw_x,)

    body = _edge_like_stock(
        p=p,
        profile_key=profile_key,
        screw_xs=screw_xs,
    )
    body = _cut_edge_like_base(
        body,
        p=p,
        profile_key=profile_key,
        screw_xs=screw_xs,
        reference_ticks=reference_ticks,
        reference_holes=reference_holes,
    )
    body = _cut_tapered_rail_relief(
        body,
        p=p,
        profile_key=relief_key,
    )
    for x in screw_xs:
        body = _guide_clearance(body, p=p, x=x, z=_edge_support_z(p))

    return _locator_pad(body, p=p, x=screw_x, z=_edge_support_z(p))


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerCornerLeft:
    """Reusable left frame-corner coupler."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = False
    reference_holes: bool = False

    def build(self):
        p = _parameters(self)
        return _build_corner_body(
            p=p,
            profile_key="corner_left",
            relief_key="corner_left",
            screw_x=p["mid_screw_x"],
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        ).with_appearance(SOURCE_RED)


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerCornerRight:
    """Reusable right frame-corner coupler."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = False
    reference_holes: bool = False

    def build(self):
        p = _parameters(self)
        body = _build_corner_body(
            p=p,
            profile_key="corner_right",
            relief_key="corner_right",
            screw_x=-p["mid_screw_x"],
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        body = _cut_panel_pin_pass_through(body, p)
        return body.with_appearance(SOURCE_RED)


def _corner_tube_base(body, *, side):
    """Shared Corner insertion/tube clearances before selecting an interface."""
    if side == "left":
        interface_center = CORNER_LEFT_RAIL_CENTER
        tube_cutter_center_x = 160.0
    elif side == "right":
        interface_center = CORNER_RIGHT_RAIL_CENTER
        tube_cutter_center_x = -160.0
    else:
        raise ValueError(f"unsupported corner side {side!r}")

    insertion_clearance = _xy_profile_solid(
        name="Inschuifuitsparing voor hoekschuifklem",
        loops=[
            _rectangle_xy(
                center_x=interface_center,
                width=CLAMP_FOOT_CLEARANCE_WIDTH,
                y_rear=CLAMP_FOOT_CLEARANCE_Y_REAR,
                y_front=CORNER_CLAMP_FOOT_CLEARANCE_Y_FRONT,
            )
        ],
        z=CLAMP_FOOT_CLEARANCE_Z,
        distance=18.2,
    )
    body = body - insertion_clearance

    tube_clearance = _axis_x_cylinder(
        diameter=TUBE_CLEARANCE_DIAMETER,
        length=TUBE_CLEARANCE_LENGTH,
        x=tube_cutter_center_x,
        y=TUBE_AXIS_Y,
        z=TUBE_AXIS_Z,
    )
    return body - tube_clearance, interface_center


def _add_corner_tube_interface(body, *, side):
    """Existing active Corner rail interface #213/#214/#216/#217/#218."""
    body, rail_center = _corner_tube_base(body, side=side)

    rail = _xy_profile_solid(
        name="Zwaluwstaartrail voor hoekschuifklem",
        loops=[_rail_xy(rail_center)],
        z=RAIL_PLANE_Z,
        distance=RAIL_HEIGHT,
    )
    body = body + rail

    return body.chamfer(
        RAIL_ENTRY_CHAMFER,
        distance2=RAIL_ENTRY_CHAMFER_SECONDARY,
        edges=_rail_entry_edges(rail_center),
    )


def _add_corner_tube_receiver_interface(body, *, side):
    """Alternate Corner interface #234-237 using one female receiver."""
    body, center = _corner_tube_base(body, side=side)
    return _add_receiver_interface(body, center)


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerCornerLeftTube:
    """Configured left Corner coupler with the final active tube interface."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = False
    reference_holes: bool = False

    def build(self):
        p = _parameters(self)
        body = _build_corner_body(
            p=p,
            profile_key="corner_left",
            relief_key="corner_left",
            screw_x=p["mid_screw_x"],
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        return _add_corner_tube_interface(
            body,
            side="left",
        ).with_appearance(SOURCE_RED)


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerCornerRightTube:
    """Configured right Corner coupler with the final active tube interface."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = False
    reference_holes: bool = False

    def build(self):
        p = _parameters(self)
        body = _build_corner_body(
            p=p,
            profile_key="corner_right",
            relief_key="corner_right",
            screw_x=-p["mid_screw_x"],
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        body = _cut_panel_pin_pass_through(body, p)
        return _add_corner_tube_interface(
            body,
            side="right",
        ).with_appearance(SOURCE_RED)



@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerCornerLeftTubeReceiver:
    """Configured left Corner tube coupler with one female dovetail receiver."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = False
    reference_holes: bool = False

    def build(self):
        p = _parameters(self)
        body = _build_corner_body(
            p=p,
            profile_key="corner_left",
            relief_key="corner_left",
            screw_x=p["mid_screw_x"],
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        return _add_corner_tube_receiver_interface(
            body,
            side="left",
        ).with_appearance(SOURCE_RED)


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerCornerRightTubeReceiver:
    """Configured right Corner tube coupler with one female dovetail receiver."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = False
    reference_holes: bool = False

    def build(self):
        p = _parameters(self)
        body = _build_corner_body(
            p=p,
            profile_key="corner_right",
            relief_key="corner_right",
            screw_x=-p["mid_screw_x"],
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        body = _cut_panel_pin_pass_through(body, p)
        return _add_corner_tube_receiver_interface(
            body,
            side="right",
        ).with_appearance(SOURCE_RED)


class Hub75FrameCouplerCornerLeftModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerLeft)


class Hub75FrameCouplerCornerRightModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerRight)
    suppress_panel_pin = True

class Hub75FrameCouplerCornerLeftTubeModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerLeftTube)


class Hub75FrameCouplerCornerRightTubeModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerRightTube)
    suppress_panel_pin = True

class Hub75FrameCouplerCornerLeftTubeReceiverModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerLeftTubeReceiver)


class Hub75FrameCouplerCornerRightTubeReceiverModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerRightTubeReceiver)
    suppress_panel_pin = True
