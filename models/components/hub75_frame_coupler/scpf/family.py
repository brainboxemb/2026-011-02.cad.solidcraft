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
    TUBE_EDGE_BASE_PLATE_PROFILES,
    TUBE_EDGE_REAR_REFERENCE_MARK_INDICES,
    TUBE_EDGE_REAR_SUPPORT_PROFILES,
)

SOURCE_RED = "#B80D0A"


def _edge_mount_z():
    """Physical local Z of the Edge/Corner mounting-bore axes."""
    return -MEDIUM["edge_screw_in"]


def _edge_support_z():
    """Physical local Z of the bushing support / locator-pad axes."""
    return _edge_mount_z() - MEDIUM["bushing_z"]


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
            z=_edge_support_z(),
        )
        body = body + _axis_y_cylinder(
            diameter=2.0 * support_r,
            length=MEDIUM["guide"],
            x=x,
            y=-MEDIUM["datum"] + MEDIUM["guide"] / 2.0,
            z=_edge_support_z(),
        )
    return body


def _cut_edge_like_base(body, *, profile_key, screw_xs):
    """Apply only base-side mounting/pattern cuts."""
    for x in screw_xs:
        body = _mounting_hole(
            body,
            x=x,
            z=_edge_mount_z(),
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
        body = _guide_clearance(body, x=x, z=_edge_support_z())
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
    body = _locator_pad(body, x=screw_x, z=_edge_support_z())
    return body


def _build_edge_body():
    """Shared accepted Medium Edge body before optional tube-interface features."""
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
        body = _locator_pad(body, x=x, z=_edge_support_z())

    return _join_tapered_seam_guide(
        body,
        profile_key="edge",
    )


@component
class Hub75FrameCouplerEdge:
    """Fixed Medium straight frame-edge coupler."""

    def build(self):
        return _build_edge_body().with_appearance(SOURCE_RED)


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


def _xy_loop(sketch, points):
    """Add one fixed source XY loop to a native Sketch."""
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


def _add_edge_tube_interface(body):
    """Active source features #189, #191, #195 and #198."""
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
    body = body - foot_clearance

    rails = _xy_profile_solid(
        name="Z-schuifrails op 40 mm hartafstand",
        loops=[_rail_xy(center_x) for center_x in EDGE_RAIL_CENTERS],
        z=RAIL_PLANE_Z,
        distance=RAIL_HEIGHT,
    )
    body = body + rails

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
    body = body - bow_clearance

    body = body.chamfer(
        RAIL_ENTRY_CHAMFER,
        distance2=RAIL_ENTRY_CHAMFER_SECONDARY,
        edges=_rail_entry_edges(*EDGE_RAIL_CENTERS),
    )

    # Final source features 226–230: replace the earlier suppressed rear/base
    # experiments with the active R5 support, continuous base and the two
    # reference marks re-cut into the newly added rear material.
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

    rear_marks = [
        REFERENCE_MARK_LOOPS["edge"][index]
        for index in TUBE_EDGE_REAR_REFERENCE_MARK_INDICES
    ]
    reference_cut = _multi_profile_solid(
        name="Referentiepatroon op symmetrische rug",
        loops=rear_marks,
        y=-(MEDIUM["datum"] + MEDIUM["base"] + REFERENCE_PATTERN["rear_offset"]),
        distance=REFERENCE_PATTERN["mark_cut_depth"],
    )
    return body - reference_cut


def _add_corner_tube_interface(body, *, side):
    """Active source features #213, #214, #216 and #217/#218."""
    if side == "left":
        rail_center = CORNER_LEFT_RAIL_CENTER
        # Source cutter #214 starts at world X=-182 and runs +364 mm. Relative
        # to the normalized left-corner origin X=-160 its center is +160.
        tube_cutter_center_x = 160.0
    elif side == "right":
        rail_center = CORNER_RIGHT_RAIL_CENTER
        # Relative to the normalized right-corner origin X=+160.
        tube_cutter_center_x = -160.0
    else:
        raise ValueError(f"unsupported corner side {side!r}")

    insertion_clearance = _xy_profile_solid(
        name="Inschuifuitsparing voor hoekschuifklem",
        loops=[
            _rectangle_xy(
                center_x=rail_center,
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
    body = body - tube_clearance

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


@component
class Hub75FrameCouplerEdgeTube:
    """Medium Edge coupler with the final active two-clamp tube interface."""

    def build(self):
        return _add_edge_tube_interface(
            _build_edge_body()
        ).with_appearance(SOURCE_RED)


@component
class Hub75FrameCouplerCornerLeftTube:
    """Medium left Corner coupler with the final active tube interface."""

    def build(self):
        body = _build_edge_like(
            profile_key="corner_left",
            relief_key="corner_left",
            screw_x=MEDIUM["screw_x"],
        )
        return _add_corner_tube_interface(
            body,
            side="left",
        ).with_appearance(SOURCE_RED)


@component
class Hub75FrameCouplerCornerRightTube:
    """Medium right Corner coupler with the final active tube interface."""

    def build(self):
        body = _build_edge_like(
            profile_key="corner_right",
            relief_key="corner_right",
            screw_x=-MEDIUM["screw_x"],
        )
        return _add_corner_tube_interface(
            body,
            side="right",
        ).with_appearance(SOURCE_RED)

