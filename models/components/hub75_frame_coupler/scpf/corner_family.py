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
    _apply_reference_pattern,
    _axis_x_cylinder,
    _axis_y_cylinder,
    _cut_panel_pin_pass_through,
    _cut_tapered_rail_relief,
    _profile_solid,
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
    _source_profile,
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
    datum = p["mid_datum"]
    base_depth = p["mid_base"]
    guide_depth = p["mid_guide"]
    mount_z = -p["edge_screw_in"]
    support_z = mount_z - p["mid_bushing_z"]
    support_r = p["mid_bushing_r"] + p["mid_bushing_gap"] + p["mid_wall"]

    # Extrude the retained Corner outline in both directions around the panel
    # datum, then reinforce the single mounting/bushing position.
    profiles = _source_profile(profile_key, "base", p)
    body = _profile_solid(
        name=f"{profile_key} base profile",
        loops=profiles,
        y=-datum,
        distance=-base_depth,
    )
    guide = _profile_solid(
        name=f"{profile_key} guide stock",
        loops=profiles,
        y=-datum,
        distance=guide_depth,
    )
    body = body + guide
    body = body + _axis_y_cylinder(
        diameter=2.0 * support_r,
        length=base_depth,
        x=screw_x,
        y=-datum - base_depth / 2.0,
        z=support_z,
    )
    body = body + _axis_y_cylinder(
        diameter=2.0 * support_r,
        length=guide_depth,
        x=screw_x,
        y=-datum + guide_depth / 2.0,
        z=support_z,
    )

    # Drill the Corner mounting position: screw bore, rear relief and the
    # deeper tube clearance remain visible as one construction stage.
    body = body - _axis_y_cylinder(
        diameter=p["mid_screw_d"],
        length=base_depth + 0.2,
        x=screw_x,
        y=-datum - base_depth / 2.0 + (base_depth - base_depth) / 2.0,
        z=mount_z,
    )
    body = body - _axis_y_cylinder(
        diameter=p["mid_screw_d"] + 0.8,
        length=0.2,
        x=screw_x,
        y=-datum - base_depth + 0.1,
        z=mount_z,
    )
    body = body - _axis_y_cylinder(
        diameter=2.0 * (p["mid_tube_r"] + p["mid_tube_gap"]),
        length=p["mid_tube_depth"],
        x=screw_x,
        y=-datum - p["mid_tube_depth"] / 2.0,
        z=mount_z,
    )

    # Optional reference marks/holes belong to the rear face of the base.
    body = _apply_reference_pattern(
        body,
        p=p,
        profile_key=profile_key,
        reference_ticks=reference_ticks,
        reference_holes=reference_holes,
    )

    # Shape the rail-side guide before opening the bushing clearance.
    body = _cut_tapered_rail_relief(
        body,
        p=p,
        profile_key=relief_key,
    )
    body = body - _axis_y_cylinder(
        diameter=2.0 * (p["mid_bushing_r"] + p["mid_bushing_gap"]),
        length=guide_depth + 0.1,
        x=screw_x,
        y=-datum + guide_depth / 2.0,
        z=support_z,
    )

    # Finish with the locating boss and pin on the panel side.
    body = body + _axis_y_cylinder(
        diameter=2.0 * p["mid_pad_r"],
        length=p["mid_pad_h"],
        x=screw_x,
        y=-datum + p["mid_pad_h"] / 2.0,
        z=support_z,
    )
    body = body + _axis_y_cylinder(
        diameter=2.0 * p["mid_pin_r"],
        length=p["mid_pin_h"],
        x=screw_x,
        y=-datum + p["mid_pad_h"] + p["mid_pin_h"] / 2.0,
        z=support_z,
    )
    return body


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
