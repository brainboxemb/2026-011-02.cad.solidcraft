"""Edge HUB75 frame-coupler implementation and tube variants."""

from dataclasses import dataclass

from scpf import cadmath, component

from models.components.hub75_frame_coupler.scpf.features import (
    CLAMP_BOW_CLEARANCE_DEPTH,
    CLAMP_BOW_CLEARANCE_WIDTH,
    CLAMP_BOW_CLEARANCE_Y_FRONT,
    CLAMP_BOW_CLEARANCE_Y_REAR,
    CLAMP_BOW_CLEARANCE_Z,
    CLAMP_FOOT_CLEARANCE_DEPTH,
    CLAMP_FOOT_CLEARANCE_WIDTH,
    CLAMP_FOOT_CLEARANCE_Y_REAR,
    CLAMP_FOOT_CLEARANCE_Z,
    EDGE_CLAMP_FOOT_CLEARANCE_Y_FRONT,
    EDGE_RAIL_CENTERS,
    RAIL_ENTRY_CHAMFER,
    RAIL_ENTRY_CHAMFER_SECONDARY,
    RAIL_HEIGHT,
    RAIL_PLANE_Z,
    _add_receiver_interface,
    _cut_edge_like_base,
    _cut_panel_pin_pass_through,
    _cut_tapered_rail_relief,
    _edge_like_stock,
    _edge_support_z,
    _guide_clearance,
    _join_tapered_seam_guide,
    _locator_pad,
    _multi_profile_solid,
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
from models.components.hub75_frame_coupler.scpf.source_data import (
    TUBE_EDGE_BASE_PLATE_PROFILES,
    TUBE_EDGE_REAR_REFERENCE_MARK_INDICES,
    TUBE_EDGE_REAR_SUPPORT_PROFILES,
)


def _edge_guide_end_profiles(p):
    """Return the retained six Edge end cuts with exact symbolic arc centers."""
    loops = _source_profile("edge", "guide_end", p)

    u = p["edge_end_u"]
    run = p["edge_end_run"]
    g = p["edge_end_g"]
    outer_offset = p["edge_or"] - p["mid_wall"]
    inner_level = p["edge_end_inner"] + p["mid_fit"]
    ix = p["mid_ix"]
    rear_level = p["mid_fit"] - p["edge_end_rear"]

    centers = (
        ((-u, -(inner_level - outer_offset)), (-(u + run), -(inner_level + g))),
        ((u, -(inner_level - outer_offset)), ((u + run), -(inner_level + g))),
        ((-(ix - outer_offset), -u), (-(ix + g), -(u + run))),
        (((ix - outer_offset), -u), ((ix + g), -(u + run))),
        ((-u, rear_level - outer_offset), (-(u + run), rear_level + g)),
        ((u, rear_level - outer_offset), ((u + run), rear_level + g)),
    )
    clockwise = (
        (False, True),
        (True, False),
        (True, False),
        (False, True),
        (True, False),
        (False, True),
    )

    converted = []
    for loop_index, loop in enumerate(loops):
        arc_index = 0
        segments = []
        for segment in loop["segments"]:
            if segment["kind"] != "arc_through":
                segments.append(segment)
                continue
            row = dict(segment)
            row["kind"] = "arc"
            row.pop("through", None)
            row["center"] = centers[loop_index][arc_index]
            row["clockwise"] = clockwise[loop_index][arc_index]
            arc_index += 1
            segments.append(row)
        converted.append({"start": loop["start"], "segments": segments})
    return converted


def _cut_edge_guide_end_rounding(body, *, p):
    """Apply native Edge guide-end rounding cut from features 137–138."""
    for index, loop in enumerate(_edge_guide_end_profiles(p), start=1):
        cut = _profile_solid(
            name=f"Edge guide-end rounding {index}",
            loops=[loop],
            y=-p["mid_datum"],
            distance=p["mid_guide"],
        )
        body = body - cut
    return body



def _clip_edge_to_top_t(body, *, p):
    """Apply the historical/native TOP-edge T window to the rounded plus."""
    bar_top = p["mid_wall"] + p["mid_fit"] - p["edge_end_rear"]
    clip_z = bar_top + 1.0

    half_width = p["mid_size"] / 2.0 + 10.0
    top = p["mid_size"] + 40.0
    loop = {
        "start": [-half_width, clip_z],
        "segments": [
            {"kind": "line", "end": [half_width, clip_z]},
            {"kind": "line", "end": [half_width, top]},
            {"kind": "line", "end": [-half_width, top]},
            {"kind": "line", "end": [-half_width, clip_z]},
        ],
    }
    cutter = _profile_solid(
        name="Edge outside-stem T clip",
        loops=[loop],
        y=-p["mid_datum"] - p["mid_base"] - 1.0,
        distance=p["mid_base"] + p["mid_guide"] + 2.0,
    )
    return body - cutter


def _build_edge_body(*, p, reference_ticks=False, reference_holes=False):
    """Build the configured Edge body before optional tube-interface features."""
    screw_xs = (-p["mid_screw_x"], p["mid_screw_x"])

    body = _edge_like_stock(
        p=p,
        profile_key="edge",
        screw_xs=screw_xs,
    )
    body = _clip_edge_to_top_t(body, p=p)
    body = _cut_edge_like_base(
        body,
        p=p,
        profile_key="edge",
        screw_xs=screw_xs,
        reference_ticks=reference_ticks,
        reference_holes=reference_holes,
    )

    body = _cut_tapered_rail_relief(
        body,
        p=p,
        profile_key="edge",
    )
    body = _cut_edge_guide_end_rounding(body, p=p)
    for x in screw_xs:
        body = _guide_clearance(body, p=p, x=x, z=_edge_support_z(p))

    for x in screw_xs:
        body = _locator_pad(body, p=p, x=x, z=_edge_support_z(p))

    return _join_tapered_seam_guide(
        body,
        p=p,
        profile_key="edge",
    )


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerEdge:
    """Reusable straight frame-edge coupler."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = False
    reference_holes: bool = False

    def build(self):
        p = _parameters(self)
        body = _build_edge_body(
            p=p,
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        body = _cut_panel_pin_pass_through(body, p)
        return body.with_appearance(SOURCE_RED)



def _cut_edge_tube_foot_clearance(body):
    """Feature #189 shared by both Edge tube-interface families."""
    foot_clearance = _xy_profile_solid(
        name="Vrijloop voor naar binnen geplaatste klemmen",
        loops=[
            _rectangle_xy(
                center_x=center_x,
                width=CLAMP_FOOT_CLEARANCE_WIDTH,
                y_rear=CLAMP_FOOT_CLEARANCE_Y_REAR,
                y_front=EDGE_CLAMP_FOOT_CLEARANCE_Y_FRONT,
            )
            for center_x in EDGE_RAIL_CENTERS
        ],
        z=CLAMP_FOOT_CLEARANCE_Z,
        distance=CLAMP_FOOT_CLEARANCE_DEPTH,
    )
    return body - foot_clearance


def _cut_edge_tube_bow_clearance(body):
    """Feature #195 shared by both Edge tube-interface families."""
    bow_clearance = _xy_profile_solid(
        name="Vrijloop voor klemboog aan de binnenzijde",
        loops=[
            _rectangle_xy(
                center_x=center_x,
                width=CLAMP_BOW_CLEARANCE_WIDTH,
                y_rear=CLAMP_BOW_CLEARANCE_Y_REAR,
                y_front=CLAMP_BOW_CLEARANCE_Y_FRONT,
            )
            for center_x in EDGE_RAIL_CENTERS
        ],
        z=CLAMP_BOW_CLEARANCE_Z,
        distance=CLAMP_BOW_CLEARANCE_DEPTH,
    )
    return body - bow_clearance


def _add_edge_tube_rear_support(body, *, p, reference_ticks=False):
    """Final active Edge rear support/base/reference chain #226-230."""
    rear_support = _multi_profile_solid(
        name="Symmetrische bulten met R5-overgangen",
        loops=TUBE_EDGE_REAR_SUPPORT_PROFILES,
        y=-17.5,
        distance=2.45,
    )
    body = body + rear_support

    base_plate = _multi_profile_solid(
        name="Doorgetrokken basisplaat rondom de twee klemmen",
        loops=TUBE_EDGE_BASE_PLATE_PROFILES,
        y=-15.15,
        distance=3.9,
    )
    body = body + base_plate

    if reference_ticks:
        rear_marks = [
            _source_profile("edge", "marks", p)[index]
            for index in TUBE_EDGE_REAR_REFERENCE_MARK_INDICES
        ]
        reference_cut = _multi_profile_solid(
            name="Referentiepatroon op symmetrische rug",
            loops=rear_marks,
            y=-(p["mid_datum"] + p["mid_base"] + 0.05),
            distance=cadmath.min(p["ref_mark_depth"], p["mid_base"] - 0.2) + 0.05,
        )
        body = body - reference_cut
    return body



def _add_edge_tube_interface(body, *, p, reference_ticks=False):
    """Existing active rail interface #189/#191/#195/#198 plus #226-230."""
    body = _cut_edge_tube_foot_clearance(body)

    rails = _xy_profile_solid(
        name="Z-schuifrails op 40 mm hartafstand",
        loops=[_rail_xy(center_x) for center_x in EDGE_RAIL_CENTERS],
        z=RAIL_PLANE_Z,
        distance=RAIL_HEIGHT,
    )
    body = body + rails

    body = _cut_edge_tube_bow_clearance(body)

    body = body.chamfer(
        RAIL_ENTRY_CHAMFER,
        distance2=RAIL_ENTRY_CHAMFER_SECONDARY,
        edges=_rail_entry_edges(*EDGE_RAIL_CENTERS),
    )
    return _add_edge_tube_rear_support(
        body,
        p=p,
        reference_ticks=reference_ticks,
    )


def _add_edge_tube_receiver_interface(body, *, p, reference_ticks=False):
    """Alternate source interface with female receivers instead of rails."""
    body = _cut_edge_tube_foot_clearance(body)
    body = _cut_edge_tube_bow_clearance(body)
    body = _add_edge_tube_rear_support(
        body,
        p=p,
        reference_ticks=reference_ticks,
    )
    return _add_receiver_interface(body, *EDGE_RAIL_CENTERS)


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerEdgeTube:
    """Configured Edge coupler with the final active two-clamp tube interface."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = False
    reference_holes: bool = False

    def build(self):
        p = _parameters(self)
        body = _build_edge_body(
            p=p,
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        body = _cut_panel_pin_pass_through(body, p)
        return _add_edge_tube_interface(
            body,
            p=p,
            reference_ticks=self.reference_ticks,
        ).with_appearance(SOURCE_RED)




@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerEdgeTubeReceiver:
    """Configured Edge tube coupler with two female dovetail receivers."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = False
    reference_holes: bool = False

    def build(self):
        p = _parameters(self)
        body = _build_edge_body(
            p=p,
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        body = _cut_panel_pin_pass_through(body, p)
        return _add_edge_tube_receiver_interface(
            body,
            p=p,
            reference_ticks=self.reference_ticks,
        ).with_appearance(SOURCE_RED)



class Hub75FrameCouplerEdgeModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerEdge)
    suppress_panel_pin = True

class Hub75FrameCouplerEdgeTubeModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerEdgeTube)
    suppress_panel_pin = True


class Hub75FrameCouplerEdgeTubeReceiverModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerEdgeTubeReceiver)
    suppress_panel_pin = True
