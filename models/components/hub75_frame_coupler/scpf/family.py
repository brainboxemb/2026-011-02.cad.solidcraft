"""Configured HUB75 frame-coupler family.

The retained SolidCraft source owns the geometry relationships.  One reusable
Forge component definition consumes the four size parameters; thin root models
add the SolidCraft Small/Medium/Large configuration table.
"""

from dataclasses import dataclass

from scpf import (
    Anchor,
    Axis,
    AxisLine,
    Cone,
    cadmath,
    Cylinder,
    Sketch,
    component,
    feature,
)

from models.components.hub75_frame_coupler.scpf.parametric_source import (
    source_circle_centers,
    source_parameters,
    source_profiles,
)
from models.components.hub75_frame_coupler.scpf.source_data import (
    TUBE_EDGE_BASE_PLATE_PROFILES,
    TUBE_EDGE_REAR_REFERENCE_MARK_INDICES,
    TUBE_EDGE_REAR_SUPPORT_PROFILES,
)

SOURCE_RED = "#B80D0A"

_SOURCE_FEATURES = {
    "middle": {
        "base": 65,
        "guide": 67,
        "seam": 79,
        "seam_tip": 80,
        "marks": 145,
        "holes": 153,
    },
    "edge": {
        "base": 87,
        "relief": 100,
        "relief_end": 101,
        "seam": 139,
        "seam_tip": 140,
        "guide_end": 137,
        "marks": 147,
        "holes": 156,
    },
    "corner_left": {
        "base": 92,
        "relief": 104,
        "relief_end": 105,
        "marks": 149,
        "holes": 159,
    },
    "corner_right": {
        "base": 96,
        "relief": 108,
        "relief_end": 109,
        "marks": 151,
        "holes": 162,
    },
}


def _parameters(owner):
    return source_parameters(
        mid_size=owner.mid_size,
        mid_wall=owner.mid_wall,
        mid_base=owner.mid_base,
        mid_guide=owner.mid_guide,
    )


def _source_profile(profile_key, role, p):
    return source_profiles(
        _SOURCE_FEATURES[profile_key][role],
        frame=profile_key,
        values=p,
    )


def _source_centers(profile_key, p):
    return source_circle_centers(
        _SOURCE_FEATURES[profile_key]["holes"],
        frame=profile_key,
        values=p,
    )


def _edge_mount_z(p):
    """Physical local Z of the Edge/Corner mounting-bore axes."""
    return -p["edge_screw_in"]


def _edge_support_z(p):
    """Physical local Z of the bushing support / locator-pad axes."""
    return _edge_mount_z(p) - p["mid_bushing_z"]


def _native_xz_point(point):
    """Convert physical local (X, Z) to SolidCraft native XZ sketch (U, V)."""
    x, z = point
    return (x, -z)


def _add_loop(sketch, loop):
    """Lower retained physical local coordinates through the native XZ frame.

    source_data.py stores the production geometry in physical local (X, Z).
    SolidCraft's native XZ plane uses sketch +V opposite physical +Z, so source
    points are reflected exactly once at this boundary. Primitive cylinders and
    pads remain authored directly in world XYZ.
    """
    contour = sketch.profile(start=_native_xz_point(loop["start"]))
    for segment in loop["segments"]:
        end = _native_xz_point(segment["end"])
        if segment["kind"] == "line":
            contour.line_to(end)
        elif segment["kind"] == "arc":
            contour.arc_center_to(
                end,
                center=_native_xz_point(segment["center"]),
                # Reflection reverses 2D winding.
                clockwise=not segment["clockwise"],
            )
        elif segment["kind"] == "arc_through":
            contour.arc_through_to(
                end,
                through=_native_xz_point(segment["through"]),
            )
        else:
            raise ValueError(f"unsupported source segment {segment['kind']!r}")
    contour.close()


def _profile_solid(*, name, loops, y, distance):
    """Extrude one or more retained source loops.

    Preserve the accepted extraction boundary by lowering each retained loop
    separately and joining the resulting SolidCraft extrusions. Newer Forge
    releases can author multiple profiles in one Sketch, but changing the
    accepted base-family history is outside this tube-interface change.
    """
    result = None
    for index, loop in enumerate(loops, start=1):
        sketch_name = name if len(loops) == 1 else f"{name} {index}"
        with Sketch(name=sketch_name, plane="XZ", offset=y) as sketch:
            _add_loop(sketch, loop)
        part = sketch.extrude(distance)
        result = part if result is None else result + part
    if result is None:
        raise ValueError(f"{name}: source profile contains no closed loops")
    return result


def _multi_profile_solid(*, name, loops, y, distance):
    """Extrude one SolidCraft XZ Sketch containing all retained closed loops."""
    if not loops:
        raise ValueError(f"{name}: source profile contains no closed loops")
    with Sketch(name=name, plane="XZ", offset=y) as sketch:
        for loop in loops:
            _add_loop(sketch, loop)
    return sketch.extrude(distance)


def _axis_y_cylinder(*, diameter, length, x, y, z):
    return Cylinder(
        d=diameter,
        h=length,
        axis=Axis.Y,
        anchor=Anchor.CENTER,
    ).at(x, y, z, anchor=Anchor.CENTER)


def _mounting_hole(body, *, p, x, z, total_depth):
    """Source-derived Ø3.4 mount bore with rear relief and tube clearance."""
    datum = p["mid_datum"]
    base = p["mid_base"]
    screw_d = p["mid_screw_d"]

    body = body - _axis_y_cylinder(
        diameter=screw_d,
        length=total_depth + 0.2,
        x=x,
        y=-datum - base / 2.0 + (total_depth - base) / 2.0,
        z=z,
    )
    body = body - _axis_y_cylinder(
        diameter=screw_d + 0.8,
        length=0.2,
        x=x,
        y=-datum - base + 0.1,
        z=z,
    )
    body = body - _axis_y_cylinder(
        diameter=2.0 * (p["mid_tube_r"] + p["mid_tube_gap"]),
        length=p["mid_tube_depth"],
        x=x,
        y=-datum - p["mid_tube_depth"] / 2.0,
        z=z,
    )
    return body


def _locator_pad(body, *, p, x, z):
    """Source pad + locating pin along the panel-depth Y axis."""
    datum = p["mid_datum"]
    pad_h = p["mid_pad_h"]
    pin_h = p["mid_pin_h"]

    body = body + _axis_y_cylinder(
        diameter=2.0 * p["mid_pad_r"],
        length=pad_h,
        x=x,
        y=-datum + pad_h / 2.0,
        z=z,
    )
    body = body + _axis_y_cylinder(
        diameter=2.0 * p["mid_pin_r"],
        length=pin_h,
        x=x,
        y=-datum + pad_h + pin_h / 2.0,
        z=z,
    )
    return body


def _guide_clearance(body, *, p, x, z):
    guide = p["mid_guide"]
    return body - _axis_y_cylinder(
        diameter=2.0 * (p["mid_bushing_r"] + p["mid_bushing_gap"]),
        length=guide + 0.1,
        x=x,
        y=-p["mid_datum"] + guide / 2.0,
        z=z,
    )


def _interpolate_loop(start, end, t):
    """Interpolate matching source loft sections in the normalized XZ frame."""
    if len(start["segments"]) != len(end["segments"]):
        raise ValueError("source loft sections have different segment counts")

    def point(a, b):
        return [
            a[0] + (b[0] - a[0]) * t,
            a[1] + (b[1] - a[1]) * t,
        ]

    segments = []
    for a, b in zip(start["segments"], end["segments"]):
        if a["kind"] != b["kind"]:
            raise ValueError("source loft sections have different segment kinds")
        row = {
            "kind": a["kind"],
            "end": point(a["end"], b["end"]),
        }
        if a["kind"] == "arc":
            row["center"] = point(a["center"], b["center"])
            row["clockwise"] = a["clockwise"]
        elif a["kind"] == "arc_through":
            row["through"] = point(a["through"], b["through"])
        segments.append(row)
    return {
        "start": point(start["start"], end["start"]),
        "segments": segments,
    }


def _cut_tapered_rail_relief(body, *, p, profile_key, steps=12):
    """Approximate the native two-section cut loft without leaving phase-1 fins.

    Forge v0.19 has no public solid-loft feature.  The source loft is shallow:
    its two XZ sections are 6.05 mm apart and differ only slightly.  Twelve
    overlapping source-interpolated slices retain both native sections and
    remove the visible prismatic fin/lip artifact from the earlier baseline.
    """
    starts = _source_profile(profile_key, "relief", p)
    ends = _source_profile(profile_key, "relief_end", p)
    if len(starts) != 1 or len(ends) != 1:
        raise ValueError("rail relief expects one source loop per loft section")

    depth = p["mid_guide"] + 0.05
    slice_depth = depth / steps
    for index in range(steps):
        # Use the far section of each thin slice.  The native cut grows
        # slightly toward insertion depth; using the midpoint left a hairline
        # residual fin at the final face in Edge/Corner previews.
        t = (index + 1.0) / steps
        loop = _interpolate_loop(starts[0], ends[0], t)
        relief = _profile_solid(
            name=f"{profile_key} rail relief slice {index + 1}",
            loops=[loop],
            y=-p["mid_datum"] + index * slice_depth,
            distance=slice_depth + 0.01,
        )
        body = body - relief
    return body



def _join_tapered_seam_guide(body, *, p, profile_key, steps=16):
    """Approximate the native seam-guide loft using exact foot/tip sections."""
    starts = _source_profile(profile_key, "seam", p)
    ends = _source_profile(profile_key, "seam_tip", p)
    if len(starts) != 1 or len(ends) != 1:
        raise ValueError("seam guide expects one source loop per loft section")

    depth = p["mid_key_h"] + 0.05
    slice_depth = depth / steps
    for index in range(steps):
        # Use the far/end section of each slice. This under-approximates the
        # true taper very slightly and avoids the broad-foot fins created by
        # the former straight prism.
        t = (index + 1.0) / steps
        loop = _interpolate_loop(starts[0], ends[0], t)
        part = _profile_solid(
            name=f"{profile_key} seam guide slice {index + 1}",
            loops=[loop],
            y=-p["mid_datum"] - 0.05 + index * slice_depth,
            distance=slice_depth + 0.01,
        )
        body = body + part
    return body


def _replace_arc_through_with_centers(loops, centers, clockwise):
    """Replace source three-point arcs while preserving source loop topology."""
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
        if arc_index != len(centers[loop_index]):
            raise ValueError(
                f"loop {loop_index}: expected {len(centers[loop_index])} arcs, "
                f"found {arc_index}"
            )
        converted.append({"start": loop["start"], "segments": segments})
    return converted


def _middle_base_profiles(p):
    inner_x = p["mid_ix"] + p["mid_wall"] + p["mid_inner_r"]
    inner_z = p["mid_iz"] + p["mid_wall"] + p["mid_inner_r"]
    centers = ((
        (-p["mid_Ox"], p["mid_oe"]),
        (p["mid_Ox"], p["mid_oe"]),
        (inner_x, inner_z),
        (p["mid_oe"], p["mid_Oz"]),
        (p["mid_oe"], -p["mid_Oz"]),
        (inner_x, -inner_z),
        (p["mid_Ox"], -p["mid_oe"]),
        (-p["mid_Ox"], -p["mid_oe"]),
        (-inner_x, -inner_z),
        (-p["mid_oe"], -p["mid_Oz"]),
        (-p["mid_oe"], p["mid_Oz"]),
        (-inner_x, inner_z),
    ),)
    clockwise = ((
        True, True, False, True, True, False,
        True, True, False, True, True, False,
    ),)
    return _replace_arc_through_with_centers(
        _source_profile("middle", "base", p),
        centers,
        clockwise,
    )


def _middle_guide_profiles(p):
    inner_x = p["mid_ix"] + p["mid_wall"] + p["mid_inner_r"]
    inner_z = p["mid_iz"] + p["mid_wall"] + p["mid_inner_r"]
    centers = (
        (
            (-p["mid_Cx"], -p["mid_Gz"]),
            (-p["mid_oe"], -p["mid_Oz"]),
            (-inner_x, -inner_z),
            (-p["mid_Ox"], -p["mid_oe"]),
            (-p["mid_Gx"], -p["mid_Cz"]),
            (-p["mid_jx"], -p["mid_jz"]),
        ),
        (
            (-p["mid_Cx"], p["mid_Gz"]),
            (-p["mid_oe"], p["mid_Oz"]),
            (-inner_x, inner_z),
            (-p["mid_Ox"], p["mid_oe"]),
            (-p["mid_Gx"], p["mid_Cz"]),
            (-p["mid_jx"], p["mid_jz"]),
        ),
        (
            (p["mid_Cx"], -p["mid_Gz"]),
            (p["mid_oe"], -p["mid_Oz"]),
            (inner_x, -inner_z),
            (p["mid_Ox"], -p["mid_oe"]),
            (p["mid_Gx"], -p["mid_Cz"]),
            (p["mid_jx"], -p["mid_jz"]),
        ),
        (
            (p["mid_Cx"], p["mid_Gz"]),
            (p["mid_oe"], p["mid_Oz"]),
            (inner_x, inner_z),
            (p["mid_Ox"], p["mid_oe"]),
            (p["mid_Gx"], p["mid_Cz"]),
            (p["mid_jx"], p["mid_jz"]),
        ),
    )
    clockwise = (
        (False, False, True, False, False, False),
        (True, True, False, True, True, True),
        (True, True, False, True, True, True),
        (False, False, True, False, False, False),
    )
    return _replace_arc_through_with_centers(
        _source_profile("middle", "guide", p),
        centers,
        clockwise,
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

def _reference_pattern_y_rear(p):
    return (
        -p["mid_datum"]
        - p["mid_base"]
        - 0.05
    )


def _cut_reference_ticks(body, *, p, profile_key):
    """Cut the optional native reference tick/stripe pattern."""
    y_rear = _reference_pattern_y_rear(p)
    for index, loop in enumerate(_source_profile(profile_key, "marks", p), start=1):
        mark = _profile_solid(
            name=f"{profile_key} reference mark {index}",
            loops=[loop],
            y=y_rear,
            distance=cadmath.min(p["ref_mark_depth"], p["mid_base"] - 0.2) + 0.05,
        )
        body = body - mark
    return body


def _cut_reference_holes(body, *, p, profile_key):
    """Cut the optional blind tapered reference-hole pattern."""
    y_rear = _reference_pattern_y_rear(p)
    straight = p["ref_straight_h"] + 0.05
    tip = p["ref_tip_h"]
    for x, z in _source_centers(profile_key, p):
        body = body - _axis_y_cylinder(
            diameter=p["ref_d"],
            length=straight,
            x=x,
            y=y_rear + straight / 2.0,
            z=z,
        )
        body = body - Cone(
            d=p["ref_d"],
            top_d=p["ref_tip_d"],
            h=tip,
            axis=Axis.Y,
            anchor=Anchor.CENTER,
        ).at(
            x,
            y_rear + straight + tip / 2.0,
            z,
            anchor=Anchor.CENTER,
        )
    return body


def _apply_reference_pattern(
    body,
    *,
    p,
    profile_key,
    reference_ticks=True,
    reference_holes=True,
):
    """Apply independently optional native reference features."""
    if reference_ticks:
        body = _cut_reference_ticks(body, p=p, profile_key=profile_key)
    if reference_holes:
        body = _cut_reference_holes(body, p=p, profile_key=profile_key)
    return body


_CONFIGURED_PARAMETERS = ("mid_size", "mid_wall", "mid_base", "mid_guide")
_PANEL_PIN_FEATURE = "panel_pin_pass_through"


def _component_parameters():
    return {
        "mid_size": 80.0,
        "mid_wall": 4.0,
        "mid_base": 3.0,
        "mid_guide": 6.0,
    }


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerMiddle:
    """Reusable frame-coupler component at the panel seam midpoint."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = True
    reference_holes: bool = True

    def build(self):
        p = _parameters(self)
        base = _profile_solid(
            name="Middle base profile",
            loops=_middle_base_profiles(p),
            y=-p["mid_datum"],
            distance=-p["mid_base"],
        )
        body = base
        for index, loop in enumerate(_middle_guide_profiles(p), start=1):
            guide = _profile_solid(
                name=f"Middle guide profile {index}",
                loops=[loop],
                y=-p["mid_datum"] - 0.05,
                distance=p["mid_guide"] + 0.05,
            )
            body = body + guide

        for x, z in (
            (-p["mid_screw_x"], p["mid_bushing_z"]),
            (p["mid_screw_x"], -p["mid_bushing_z"]),
        ):
            body = _guide_clearance(body, p=p, x=x, z=z)

        for x in (-p["mid_screw_x"], p["mid_screw_x"]):
            body = _mounting_hole(
                body,
                p=p,
                x=x,
                z=0.0,
                total_depth=p["mid_base"],
            )

        body = _locator_pad(
            body,
            p=p,
            x=-p["mid_screw_x"],
            z=p["mid_bushing_z"],
        )
        body = _locator_pad(
            body,
            p=p,
            x=p["mid_screw_x"],
            z=-p["mid_bushing_z"],
        )

        body = _join_tapered_seam_guide(
            body,
            p=p,
            profile_key="middle",
        )
        body = _apply_reference_pattern(
            body,
            p=p,
            profile_key="middle",
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        return body.with_appearance(SOURCE_RED)


def _edge_like_stock(*, p, profile_key, screw_xs):
    """Create configured base + guide/support volumes before any cuts."""
    profiles = _source_profile(profile_key, "base", p)
    body = _profile_solid(
        name=f"{profile_key} base profile",
        loops=profiles,
        y=-p["mid_datum"],
        distance=-p["mid_base"],
    )
    guide = _profile_solid(
        name=f"{profile_key} guide stock",
        loops=profiles,
        y=-p["mid_datum"],
        distance=p["mid_guide"],
    )
    body = body + guide

    support_r = p["mid_bushing_r"] + p["mid_bushing_gap"] + p["mid_wall"]
    for x in screw_xs:
        body = body + _axis_y_cylinder(
            diameter=2.0 * support_r,
            length=p["mid_base"],
            x=x,
            y=-p["mid_datum"] - p["mid_base"] / 2.0,
            z=_edge_support_z(p),
        )
        body = body + _axis_y_cylinder(
            diameter=2.0 * support_r,
            length=p["mid_guide"],
            x=x,
            y=-p["mid_datum"] + p["mid_guide"] / 2.0,
            z=_edge_support_z(p),
        )
    return body


def _cut_edge_like_base(
    body,
    *,
    p,
    profile_key,
    screw_xs,
    reference_ticks=True,
    reference_holes=True,
):
    """Apply mounting bores plus independently optional reference cuts."""
    for x in screw_xs:
        body = _mounting_hole(
            body,
            p=p,
            x=x,
            z=_edge_mount_z(p),
            total_depth=p["mid_base"],
        )
    return _apply_reference_pattern(
        body,
        p=p,
        profile_key=profile_key,
        reference_ticks=reference_ticks,
        reference_holes=reference_holes,
    )


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


def _cut_edge_like_guide(body, *, p, relief_key, screw_xs, edge=False):
    """Apply only panel-side guide/relief cuts."""
    body = _cut_tapered_rail_relief(
        body,
        p=p,
        profile_key=relief_key,
    )
    if edge:
        body = _cut_edge_guide_end_rounding(body, p=p)
    for x in screw_xs:
        body = _guide_clearance(body, p=p, x=x, z=_edge_support_z(p))
    return body


def _build_edge_like(
    *,
    p,
    profile_key,
    relief_key,
    screw_x,
    reference_ticks=True,
    reference_holes=True,
):
    """Shared configured construction for one left/right corner member."""
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
    body = _cut_edge_like_guide(
        body,
        p=p,
        relief_key=relief_key,
        screw_xs=screw_xs,
    )
    return _locator_pad(body, p=p, x=screw_x, z=_edge_support_z(p))


def _build_edge_body(*, p, reference_ticks=True, reference_holes=True):
    """Shared configured Edge body before optional tube-interface features."""
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
    body = _cut_edge_like_guide(
        body,
        p=p,
        relief_key="edge",
        screw_xs=screw_xs,
        edge=True,
    )

    for x in screw_xs:
        body = _locator_pad(body, p=p, x=x, z=_edge_support_z(p))

    return _join_tapered_seam_guide(
        body,
        p=p,
        profile_key="edge",
    )


def _cut_panel_pin_pass_through(body, p):
    """Author the exact stepped shifted-axis revolve as one named cut feature."""
    axis_x = -p["mid_screw_x"] + 3.0
    axis_z = _edge_mount_z(p) - 42.0
    relief_r = p["edge_pin_r"] + p["mid_screw_relief_r"]
    core_r = p["edge_pin_r"]

    rear = -p["mid_datum"] - p["mid_base"] - 0.1
    rear_step = -p["mid_datum"] - p["mid_base"] + p["mid_screw_relief_d"]
    front_step = -p["mid_datum"] - p["mid_screw_relief_d"]
    front = -p["mid_datum"] + 0.025

    with Sketch(
        name="Panel-pin pass-through section",
        plane="XY",
        offset=axis_z,
    ) as sketch:
        start = (axis_x, rear)
        contour = sketch.profile(start=start)
        contour.line_to((axis_x + relief_r, rear))
        contour.line_to((axis_x + relief_r, rear_step))
        contour.line_to((axis_x + core_r, rear_step))
        contour.line_to((axis_x + core_r, front_step))
        contour.line_to((axis_x + relief_r, front_step))
        contour.line_to((axis_x + relief_r, front))
        contour.line_to((axis_x, front))
        contour.line_to(start)
        contour.close()

    with feature(_PANEL_PIN_FEATURE, suppressed=True):
        body = body - sketch.revolve(
            axis=AxisLine(Axis.Y, origin=(axis_x, 0, axis_z)),
        )
    return body


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerEdge:
    """Reusable straight frame-edge coupler."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = True
    reference_holes: bool = True

    def build(self):
        p = _parameters(self)
        body = _build_edge_body(
            p=p,
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        body = _cut_panel_pin_pass_through(body, p)
        return body.with_appearance(SOURCE_RED)


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerCornerLeft:
    """Reusable left frame-corner coupler."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = True
    reference_holes: bool = True

    def build(self):
        p = _parameters(self)
        return _build_edge_like(
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
    reference_ticks: bool = True
    reference_holes: bool = True

    def build(self):
        p = _parameters(self)
        body = _build_edge_like(
            p=p,
            profile_key="corner_right",
            relief_key="corner_right",
            screw_x=-p["mid_screw_x"],
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        body = _cut_panel_pin_pass_through(body, p)
        return body.with_appearance(SOURCE_RED)


class _ConfiguredCouplerRoot:
    """Shared root model for one configured reusable coupler occurrence."""

    suppress_panel_pin = False

    mid_size = 80.0
    mid_wall = 4.0
    mid_base = 3.0
    mid_guide = 6.0

    def build(self):
        child = self.component_type(
            mid_size=self.mid_size,
            mid_wall=self.mid_wall,
            mid_base=self.mid_base,
            mid_guide=self.mid_guide,
        )
        columns = [
            self.mid_size,
            self.mid_wall,
            self.mid_base,
            self.mid_guide,
        ]
        rows = {
            "Small": ["60 mm", "2 mm", "2 mm", "4 mm"],
            "Medium": ["80 mm", "4 mm", "3 mm", "6 mm"],
            "Large": ["100 mm", "6 mm", "4 mm", "10 mm"],
        }
        if self.suppress_panel_pin:
            columns.append(child.feature(_PANEL_PIN_FEATURE))
            rows["Small"].append(True)
            rows["Medium"].append(True)
            rows["Large"].append(False)

        child.configure(
            active="Medium",
            columns=tuple(columns),
            rows={name: tuple(values) for name, values in rows.items()},
        )
        return child


class Hub75FrameCouplerMiddleModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerMiddle)


class Hub75FrameCouplerEdgeModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerEdge)
    suppress_panel_pin = True


class Hub75FrameCouplerCornerLeftModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerLeft)


class Hub75FrameCouplerCornerRightModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerRight)
    suppress_panel_pin = True


# Final active tube-interface geometry from the retained SolidCraft assembly.
#
# The source authors these features on the top Edge/Corner occurrences at
# world Z=320. This owner is normalized around that datum, so the authored
# sketch offsets 321.8 / 322 / 323.55 become local Z=1.8 / 2 / 3.55.
TUBE_AXIS_Y = -6.0
TUBE_AXIS_Z = 10.0
TUBE_CLEARANCE_DIAMETER = 10.5
TUBE_CLEARANCE_LENGTH = 364.0

EDGE_RAIL_CENTERS = (-20.0, 20.0)
CORNER_LEFT_RAIL_CENTER = 7.0
CORNER_RIGHT_RAIL_CENTER = -7.0

RAIL_REAR_Y = -16.0
RAIL_NECK_Y = -14.75
RAIL_FLANK_Y = -13.75
RAIL_FRONT_Y = -13.35
RAIL_HALF_TOP = 2.45
RAIL_HALF_FLANK = 3.3

RAIL_PLANE_Z = 2.0
RAIL_HEIGHT = 14.75
RAIL_ENTRY_CHAMFER = 0.18
RAIL_ENTRY_CHAMFER_SECONDARY = 0.65

CLAMP_FOOT_CLEARANCE_Z = 1.8
CLAMP_FOOT_CLEARANCE_DEPTH = 3.0
CLAMP_FOOT_CLEARANCE_WIDTH = 12.5
CLAMP_FOOT_CLEARANCE_Y_REAR = -15.05
EDGE_CLAMP_FOOT_CLEARANCE_Y_FRONT = -11.4
CORNER_CLAMP_FOOT_CLEARANCE_Y_FRONT = -8.4

CLAMP_BOW_CLEARANCE_Z = 3.55
CLAMP_BOW_CLEARANCE_DEPTH = 0.45
CLAMP_BOW_CLEARANCE_WIDTH = 12.4
CLAMP_BOW_CLEARANCE_Y_REAR = -9.1
CLAMP_BOW_CLEARANCE_Y_FRONT = -8.4

# Alternate female receiver interface from the newly supplied total-model source.
DOVE_FIT = 0.2
RECEIVER_SUPPORT_Z = 1.2
RECEIVER_SUPPORT_HEIGHT = 15.55
RECEIVER_SUPPORT_WIDTH = 16.0
RECEIVER_SUPPORT_Y_REAR = TUBE_AXIS_Y - 11.0
RECEIVER_SUPPORT_Y_FRONT = TUBE_AXIS_Y - 6.95

RECEIVER_GROOVE_Z = 1.8
RECEIVER_GROOVE_DEPTH = 18.7
RECEIVER_HEAD_HALF = 6.0 + DOVE_FIT
RECEIVER_NECK_HALF = 5.4 + DOVE_FIT
RECEIVER_REAR_Y = TUBE_AXIS_Y - 9.1
RECEIVER_REAR_LAND_Y = TUBE_AXIS_Y - 8.05
RECEIVER_FLANK_REAR_Y = TUBE_AXIS_Y - 7.45
RECEIVER_FLANK_FRONT_Y = TUBE_AXIS_Y - 7.05
RECEIVER_FRONT_LAND_Y = TUBE_AXIS_Y - 6.45
RECEIVER_FRONT_Y = TUBE_AXIS_Y + 6.0


def _xy_loop(sketch, points):
    """Add one fixed source XY loop to a Forge Sketch."""
    contour = sketch.profile(start=points[0])
    for point in points[1:]:
        contour.line_to(point)
    contour.line_to(points[0])
    contour.close()


def _xy_profile_solid(*, name, loops, z, distance):
    """Extrude one or more disconnected active source profiles in one Sketch."""
    with Sketch(name=name, plane="XY", offset=z) as sketch:
        for points in loops:
            _xy_loop(sketch, points)
    return sketch.extrude(distance)


def _rectangle_xy(*, center_x, width, y_rear, y_front):
    half = width / 2.0
    return [
        (center_x - half, y_rear),
        (center_x + half, y_rear),
        (center_x + half, y_front),
        (center_x - half, y_front),
    ]


def _rail_xy(center_x):
    """One source Z-slide rail profile translated to its local X datum."""
    return [
        (center_x - RAIL_HALF_TOP, RAIL_REAR_Y),
        (center_x + RAIL_HALF_TOP, RAIL_REAR_Y),
        (center_x + RAIL_HALF_TOP, RAIL_NECK_Y),
        (center_x + RAIL_HALF_FLANK, RAIL_FLANK_Y),
        (center_x + RAIL_HALF_FLANK, RAIL_FRONT_Y),
        (center_x - RAIL_HALF_FLANK, RAIL_FRONT_Y),
        (center_x - RAIL_HALF_FLANK, RAIL_FLANK_Y),
        (center_x - RAIL_HALF_TOP, RAIL_NECK_Y),
    ]


def _rail_entry_edges(*centers):
    """Derive the five source chamfer picks per rail from its authored profile."""
    picks = []
    top_z = RAIL_PLANE_Z + RAIL_HEIGHT
    for center_x in centers:
        points = _rail_xy(center_x)
        # Native source features #198/#217/#218 select the top edges created by
        # profile segments l3..l7. Midpoints are stable authoring picks.
        for index in range(2, 7):
            a = points[index]
            b = points[(index + 1) % len(points)]
            picks.append(
                (
                    (a[0] + b[0]) / 2.0,
                    (a[1] + b[1]) / 2.0,
                    top_z,
                )
            )
    return picks


def _axis_x_cylinder(*, diameter, length, x, y, z):
    return Cylinder(
        d=diameter,
        h=length,
        axis=Axis.X,
        anchor=Anchor.CENTER,
    ).at(x, y, z, anchor=Anchor.CENTER)


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


def _add_edge_tube_rear_support(body, *, p, reference_ticks=True):
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


def _receiver_xy(center_x):
    """Source feature #236 receiver profile translated to one clamp center."""
    h = RECEIVER_HEAD_HALF
    n = RECEIVER_NECK_HALF
    return [
        (center_x - h, RECEIVER_REAR_Y),
        (center_x + h, RECEIVER_REAR_Y),
        (center_x + h, RECEIVER_REAR_LAND_Y),
        (center_x + n, RECEIVER_FLANK_REAR_Y),
        (center_x + n, RECEIVER_FLANK_FRONT_Y),
        (center_x + h, RECEIVER_FRONT_LAND_Y),
        (center_x + h, RECEIVER_FRONT_Y),
        (center_x - h, RECEIVER_FRONT_Y),
        (center_x - h, RECEIVER_FRONT_LAND_Y),
        (center_x - n, RECEIVER_FLANK_FRONT_Y),
        (center_x - n, RECEIVER_FLANK_REAR_Y),
        (center_x - h, RECEIVER_REAR_LAND_Y),
    ]


def _add_receiver_interface(body, *centers):
    """Active source features #234-237 for one or more male-clamp receivers."""
    support = _xy_profile_solid(
        name="Voeten voor ontvangende zwaluwstaarten",
        loops=[
            _rectangle_xy(
                center_x=center_x,
                width=RECEIVER_SUPPORT_WIDTH,
                y_rear=RECEIVER_SUPPORT_Y_REAR,
                y_front=RECEIVER_SUPPORT_Y_FRONT,
            )
            for center_x in centers
        ],
        z=RECEIVER_SUPPORT_Z,
        distance=RECEIVER_SUPPORT_HEIGHT,
    )
    body = body + support

    grooves = _xy_profile_solid(
        name="Zwaluwstaartprofielen met speling",
        loops=[_receiver_xy(center_x) for center_x in centers],
        z=RECEIVER_GROOVE_Z,
        distance=RECEIVER_GROOVE_DEPTH,
    )
    return body - grooves


def _add_edge_tube_interface(body, *, p, reference_ticks=True):
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


def _add_edge_tube_receiver_interface(body, *, p, reference_ticks=True):
    """Alternate source interface with female receivers instead of rails."""
    body = _cut_edge_tube_foot_clearance(body)
    body = _cut_edge_tube_bow_clearance(body)
    body = _add_edge_tube_rear_support(
        body,
        p=p,
        reference_ticks=reference_ticks,
    )
    return _add_receiver_interface(body, *EDGE_RAIL_CENTERS)


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
class Hub75FrameCouplerEdgeTube:
    """Configured Edge coupler with the final active two-clamp tube interface."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = True
    reference_holes: bool = True

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
class Hub75FrameCouplerCornerLeftTube:
    """Configured left Corner coupler with the final active tube interface."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = True
    reference_holes: bool = True

    def build(self):
        p = _parameters(self)
        body = _build_edge_like(
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
    reference_ticks: bool = True
    reference_holes: bool = True

    def build(self):
        p = _parameters(self)
        body = _build_edge_like(
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
class Hub75FrameCouplerEdgeTubeReceiver:
    """Configured Edge tube coupler with two female dovetail receivers."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = True
    reference_holes: bool = True

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


@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerCornerLeftTubeReceiver:
    """Configured left Corner tube coupler with one female dovetail receiver."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = True
    reference_holes: bool = True

    def build(self):
        p = _parameters(self)
        body = _build_edge_like(
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
    reference_ticks: bool = True
    reference_holes: bool = True

    def build(self):
        p = _parameters(self)
        body = _build_edge_like(
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

class Hub75FrameCouplerEdgeTubeModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerEdgeTube)
    suppress_panel_pin = True


class Hub75FrameCouplerCornerLeftTubeModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerLeftTube)


class Hub75FrameCouplerCornerRightTubeModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerRightTube)
    suppress_panel_pin = True


class Hub75FrameCouplerEdgeTubeReceiverModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerEdgeTubeReceiver)
    suppress_panel_pin = True


class Hub75FrameCouplerCornerLeftTubeReceiverModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerLeftTubeReceiver)


class Hub75FrameCouplerCornerRightTubeReceiverModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCornerRightTubeReceiver)
    suppress_panel_pin = True

