"""Medium-only HUB75 frame-coupler family.

The physical owner is shared across middle, edge and corner variants.  Geometry
data is extracted from the retained native SolidCraft source.  This first port
keeps the active Medium row fixed; native Small/Medium/Large authoring will
replace that fixed layer after Forge configuration support (#216).
"""

from scpf import Anchor, Axis, Cone, Cylinder, Sketch, component

from models.components.hub75_frame_coupler.scpf.source_data import (
    BASE_PROFILES,
    MEDIUM,
    MIDDLE_GUIDE_PROFILES,
    RAIL_RELIEF_PROFILES,
    RAIL_RELIEF_END_PROFILES,
    REFERENCE_HOLE_CENTERS,
    REFERENCE_MARK_LOOPS,
    REFERENCE_PATTERN,
    SEAM_PROFILES,
    SEAM_TIP_PROFILES,
    EDGE_GUIDE_END_CUTS,
)

SOURCE_RED = "#B80D0A"


def _native_xz_point(point):
    """Lower physical local XZ coordinates to SolidCraft native XZ sketch UV.

    SolidCraft's native XZ origin plane uses sketch +V toward world -Z.
    source_data.py stores physical local (X, Z), so every source-derived sketch
    point must reflect Z once at this boundary.  Keeping this conversion here
    lets primitives continue to use ordinary world XYZ coordinates.
    """
    x, z = point
    return (x, -z)


def _add_loop(sketch, loop):
    contour = sketch.profile(start=_native_xz_point(loop["start"]))
    for segment in loop["segments"]:
        end = _native_xz_point(segment["end"])
        if segment["kind"] == "line":
            contour.line_to(end)
        elif segment["kind"] == "arc":
            contour.arc_center_to(
                end,
                center=_native_xz_point(segment["center"]),
                # A reflection reverses 2D winding.
                clockwise=not segment["clockwise"],
            )
        else:
            raise ValueError(f"unsupported source segment {segment['kind']!r}")
    contour.close()


def _profile_solid(*, name, loops, y, distance):
    """Extrude one or more retained source loops.

    Forge v0.19 requires one closed profile per standalone Sketch, while the
    native SolidCraft source may store several disconnected profiles in one
    sketch. Preserve that source shape by lowering each loop separately and
    joining the resulting native extrusions.
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


def _axis_y_cylinder(*, diameter, length, x, y, z):
    return Cylinder(
        d=diameter,
        h=length,
        axis=Axis.Y,
        anchor=Anchor.CENTER,
    ).at(x, y, z, anchor=Anchor.CENTER)


def _mounting_hole(body, *, x, z, total_depth):
    """Source-derived Ø3.4 mount bore with rear relief and tube clearance."""
    datum = MEDIUM["datum"]
    base = MEDIUM["base"]
    screw_d = MEDIUM["screw_d"]

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
        diameter=2.0 * (MEDIUM["tube_r"] + MEDIUM["tube_gap"]),
        length=MEDIUM["tube_depth"],
        x=x,
        y=-datum - MEDIUM["tube_depth"] / 2.0,
        z=z,
    )
    return body


def _locator_pad(body, *, x, z):
    """Source Medium pad + locating pin along the panel-depth Y axis."""
    datum = MEDIUM["datum"]
    pad_h = MEDIUM["pad_h"]
    pin_h = MEDIUM["pin_h"]

    body = body + _axis_y_cylinder(
        diameter=2.0 * MEDIUM["pad_r"],
        length=pad_h,
        x=x,
        y=-datum + pad_h / 2.0,
        z=z,
    )
    body = body + _axis_y_cylinder(
        diameter=2.0 * MEDIUM["pin_r"],
        length=pin_h,
        x=x,
        y=-datum + pad_h + pin_h / 2.0,
        z=z,
    )
    return body


def _guide_clearance(body, *, x, z):
    guide = MEDIUM["guide"]
    return body - _axis_y_cylinder(
        diameter=2.0 * (MEDIUM["bushing_r"] + MEDIUM["bushing_gap"]),
        length=guide + 0.1,
        x=x,
        y=-MEDIUM["datum"] + guide / 2.0,
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
        segments.append(row)
    return {
        "start": point(start["start"], end["start"]),
        "segments": segments,
    }


def _cut_tapered_rail_relief(body, *, profile_key, steps=12):
    """Approximate the native two-section cut loft without leaving phase-1 fins.

    Forge v0.19 has no public solid-loft feature.  The source loft is shallow:
    its two XZ sections are 6.05 mm apart and differ only slightly.  Twelve
    overlapping source-interpolated slices retain both native sections and
    remove the visible prismatic fin/lip artifact from the earlier baseline.
    """
    starts = RAIL_RELIEF_PROFILES[profile_key]
    ends = RAIL_RELIEF_END_PROFILES[profile_key]
    if len(starts) != 1 or len(ends) != 1:
        raise ValueError("rail relief expects one source loop per loft section")

    depth = MEDIUM["guide"] + 0.05
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
            y=-MEDIUM["datum"] + index * slice_depth,
            distance=slice_depth + 0.01,
        )
        body = body - relief
    return body



def _join_tapered_seam_guide(body, *, profile_key, steps=16):
    """Approximate the native seam-guide loft using exact foot/tip sections."""
    starts = SEAM_PROFILES[profile_key]
    ends = SEAM_TIP_PROFILES[profile_key]
    if len(starts) != 1 or len(ends) != 1:
        raise ValueError("seam guide expects one source loop per loft section")

    depth = MEDIUM["key_h"] + 0.05
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
            y=-MEDIUM["datum"] - 0.05 + index * slice_depth,
            distance=slice_depth + 0.01,
        )
        body = body + part
    return body


def _cut_edge_guide_end_rounding(body):
    """Apply native Edge guide-end rounding cut from features 137–138."""
    for index, loop in enumerate(EDGE_GUIDE_END_CUTS, start=1):
        cut = _profile_solid(
            name=f"Edge guide-end rounding {index}",
            loops=[loop],
            y=-MEDIUM["datum"],
            distance=MEDIUM["guide"],
        )
        body = body - cut
    return body

def _apply_reference_pattern(body, *, profile_key):
    """Cut the native reference ticks and blind tapered reference-hole pattern."""
    y_rear = (
        -MEDIUM["datum"]
        - MEDIUM["base"]
        - REFERENCE_PATTERN["rear_offset"]
    )

    for index, loop in enumerate(REFERENCE_MARK_LOOPS[profile_key], start=1):
        mark = _profile_solid(
            name=f"{profile_key} reference mark {index}",
            loops=[loop],
            y=y_rear,
            distance=REFERENCE_PATTERN["mark_cut_depth"],
        )
        body = body - mark

    straight = REFERENCE_PATTERN["straight_h"] + REFERENCE_PATTERN["rear_offset"]
    tip = REFERENCE_PATTERN["tip_h"]
    for x, z in REFERENCE_HOLE_CENTERS[profile_key]:
        body = body - _axis_y_cylinder(
            diameter=REFERENCE_PATTERN["hole_d"],
            length=straight,
            x=x,
            y=y_rear + straight / 2.0,
            z=z,
        )
        body = body - Cone(
            d=REFERENCE_PATTERN["hole_d"],
            top_d=REFERENCE_PATTERN["tip_d"],
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


@component
class Hub75FrameCouplerMiddle:
    """Fixed Medium source variant at the panel seam midpoint."""

    def build(self):
        base = _profile_solid(
            name="Middle base profile",
            loops=BASE_PROFILES["middle"],
            y=-MEDIUM["datum"],
            distance=-MEDIUM["base"],
        )
        body = base
        for index, loop in enumerate(MIDDLE_GUIDE_PROFILES, start=1):
            guide = _profile_solid(
                name=f"Middle guide profile {index}",
                loops=[loop],
                y=-MEDIUM["datum"] - 0.05,
                distance=MEDIUM["guide"] + 0.05,
            )
            body = body + guide

        for x, z in ((-MEDIUM["screw_x"], MEDIUM["bushing_z"]),
                     (MEDIUM["screw_x"], -MEDIUM["bushing_z"])):
            body = _guide_clearance(body, x=x, z=z)

        for x in (-MEDIUM["screw_x"], MEDIUM["screw_x"]):
            body = _mounting_hole(
                body,
                x=x,
                z=0.0,
                total_depth=MEDIUM["base"],
            )

        body = _locator_pad(
            body,
            x=-MEDIUM["screw_x"],
            z=MEDIUM["bushing_z"],
        )
        body = _locator_pad(
            body,
            x=MEDIUM["screw_x"],
            z=-MEDIUM["bushing_z"],
        )

        body = _join_tapered_seam_guide(
            body,
            profile_key="middle",
        )
        body = _apply_reference_pattern(body, profile_key="middle")
        return body.with_appearance(SOURCE_RED)



def _edge_like_stock(*, profile_key, screw_xs):
    """Create raw 3 mm base + 6 mm guide/support volumes before any cuts."""
    body = _profile_solid(
        name=f"{profile_key} base profile",
        loops=BASE_PROFILES[profile_key],
        y=-MEDIUM["datum"],
        distance=-MEDIUM["base"],
    )
    guide = _profile_solid(
        name=f"{profile_key} guide stock",
        loops=BASE_PROFILES[profile_key],
        y=-MEDIUM["datum"],
        distance=MEDIUM["guide"],
    )
    body = body + guide

    support_r = MEDIUM["bushing_r"] + MEDIUM["bushing_gap"] + MEDIUM["wall"]
    for x in screw_xs:
        body = body + _axis_y_cylinder(
            diameter=2.0 * support_r,
            length=MEDIUM["base"],
            x=x,
            y=-MEDIUM["datum"] - MEDIUM["base"] / 2.0,
            z=-19.0,
        )
        body = body + _axis_y_cylinder(
            diameter=2.0 * support_r,
            length=MEDIUM["guide"],
            x=x,
            y=-MEDIUM["datum"] + MEDIUM["guide"] / 2.0,
            z=-19.0,
        )
    return body


def _cut_edge_like_base(body, *, profile_key, screw_xs):
    """Apply only base-side mounting/pattern cuts."""
    for x in screw_xs:
        body = _mounting_hole(
            body,
            x=x,
            z=-8.0,
            total_depth=MEDIUM["base"],
        )
    return _apply_reference_pattern(body, profile_key=profile_key)


def _clip_edge_to_top_t(body):
    """Apply the historical/native TOP-edge T window to the rounded plus.

    Native feature 89 starts at absolute Z = panel_h - edge_outer_z + 1 mm.
    After subtracting the nominal edge datum panel_h, the local cut starts at
    -edge_outer_z + 1 mm (3.855 mm for Medium), not edge_outer_z + 1 mm.
    """
    bar_top = (
        MEDIUM["wall"]
        + MEDIUM["fit"]
        - MEDIUM["edge_end_rear"]
    )
    clip_z = bar_top + 1.0

    # Forge v0.19 cannot lower a placed Box as a cutter. Express the exact
    # same half-space window as an XZ sketch extruded across base+guide depth.
    half_width = MEDIUM["size"] / 2.0 + 10.0
    top = MEDIUM["size"] + 40.0
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
        y=-MEDIUM["datum"] - MEDIUM["base"] - 1.0,
        distance=MEDIUM["base"] + MEDIUM["guide"] + 2.0,
    )
    return body - cutter


def _cut_edge_like_guide(body, *, relief_key, screw_xs, edge=False):
    """Apply only panel-side guide/relief cuts."""
    body = _cut_tapered_rail_relief(
        body,
        profile_key=relief_key,
    )
    if edge:
        body = _cut_edge_guide_end_rounding(body)
    for x in screw_xs:
        body = _guide_clearance(body, x=x, z=-19.0)
    return body


def _build_edge_like(*, profile_key, relief_key, screw_x):
    """Shared Medium construction for one left/right corner member."""
    screw_xs = (screw_x,)
    body = _edge_like_stock(
        profile_key=profile_key,
        screw_xs=screw_xs,
    )
    body = _cut_edge_like_base(
        body,
        profile_key=profile_key,
        screw_xs=screw_xs,
    )
    body = _cut_edge_like_guide(
        body,
        relief_key=relief_key,
        screw_xs=screw_xs,
    )
    body = _locator_pad(body, x=screw_x, z=-19.0)
    return body


@component
class Hub75FrameCouplerEdge:
    """Fixed Medium straight frame-edge coupler."""

    def build(self):
        screw_xs = (-MEDIUM["screw_x"], MEDIUM["screw_x"])
        body = _edge_like_stock(
            profile_key="edge",
            screw_xs=screw_xs,
        )
        body = _clip_edge_to_top_t(body)
        body = _cut_edge_like_base(
            body,
            profile_key="edge",
            screw_xs=screw_xs,
        )
        body = _cut_edge_like_guide(
            body,
            relief_key="edge",
            screw_xs=screw_xs,
            edge=True,
        )

        for x in screw_xs:
            body = _locator_pad(body, x=x, z=-19.0)

        body = _join_tapered_seam_guide(
            body,
            profile_key="edge",
        )
        return body.with_appearance(SOURCE_RED)


@component
class Hub75FrameCouplerCornerLeft:
    """Fixed Medium left frame-corner coupler."""

    def build(self):
        return _build_edge_like(
            profile_key="corner_left",
            relief_key="corner_left",
            screw_x=MEDIUM["screw_x"],
        ).with_appearance(SOURCE_RED)


@component
class Hub75FrameCouplerCornerRight:
    """Fixed Medium right frame-corner coupler."""

    def build(self):
        # Native Medium suppresses the right-corner panel-pin pass-through.
        return _build_edge_like(
            profile_key="corner_right",
            relief_key="corner_right",
            screw_x=-MEDIUM["screw_x"],
        ).with_appearance(SOURCE_RED)
