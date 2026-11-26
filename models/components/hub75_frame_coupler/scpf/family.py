"""Medium-only HUB75 frame-coupler family.

The physical owner is shared across middle, edge and corner variants.  Geometry
data is extracted from the retained native SolidCraft source.  This first port
keeps the active Medium row fixed; native Small/Medium/Large authoring will
replace that fixed layer after Forge configuration support (#216).
"""

from scpf import Anchor, Axis, Cylinder, Sketch, component

from models.components.hub75_frame_coupler.scpf.source_data import (
    BASE_PROFILES,
    MEDIUM,
    MIDDLE_GUIDE_PROFILES,
    RAIL_RELIEF_PROFILES,
    SEAM_PROFILES,
)

SOURCE_RED = "#B80D0A"


def _add_loop(sketch, loop):
    contour = sketch.profile(start=tuple(loop["start"]))
    for segment in loop["segments"]:
        end = tuple(segment["end"])
        if segment["kind"] == "line":
            contour.line_to(end)
        elif segment["kind"] == "arc":
            contour.arc_center_to(
                end,
                center=tuple(segment["center"]),
                clockwise=segment["clockwise"],
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

        # Phase-1 Medium port: keep the source seam-guide footprint and use a
        # straight 4 mm prism.  Forge #216 is configuration-only; exact native
        # taper adoption can be refined independently without changing ids.
        seam = _profile_solid(
            name="Middle seam guide",
            loops=SEAM_PROFILES["middle"],
            y=-MEDIUM["datum"] - 0.05,
            distance=MEDIUM["key_h"] + 0.05,
        )
        return (body + seam).with_appearance(SOURCE_RED)



def _build_edge_like(*, profile_key, relief_key, screw_x):
    """Shared Medium construction for one left/right corner member."""
    depth = MEDIUM["base"] + MEDIUM["guide"]
    body = _profile_solid(
        name=f"{profile_key} source profile",
        loops=BASE_PROFILES[profile_key],
        y=-MEDIUM["datum"] - MEDIUM["base"],
        distance=depth,
    )

    support_r = MEDIUM["bushing_r"] + MEDIUM["bushing_gap"] + MEDIUM["wall"]
    body = body + _axis_y_cylinder(
        diameter=2.0 * support_r,
        length=depth,
        x=screw_x,
        y=-MEDIUM["datum"] - MEDIUM["base"] + depth / 2.0,
        z=-19.0,
    )

    # The native source uses a shallow loft between two very similar rail
    # clearance profiles. Released Forge v0.19 has no public solid-loft
    # authoring yet, so this Medium baseline uses the source entrance profile
    # as a prismatic guide-depth clearance.
    relief = _profile_solid(
        name=f"{profile_key} rail clearance",
        loops=RAIL_RELIEF_PROFILES[relief_key],
        y=-MEDIUM["datum"],
        distance=MEDIUM["guide"] + 0.05,
    )
    body = body - relief
    body = _guide_clearance(body, x=screw_x, z=-19.0)
    body = _mounting_hole(
        body,
        x=screw_x,
        z=-8.0,
        total_depth=depth,
    )
    body = _locator_pad(body, x=screw_x, z=-19.0)
    return body


@component
class Hub75FrameCouplerEdge:
    """Fixed Medium straight frame-edge coupler."""

    def build(self):
        depth = MEDIUM["base"] + MEDIUM["guide"]
        body = _profile_solid(
            name="Edge source profile",
            loops=BASE_PROFILES["edge"],
            y=-MEDIUM["datum"] - MEDIUM["base"],
            distance=depth,
        )

        support_r = MEDIUM["bushing_r"] + MEDIUM["bushing_gap"] + MEDIUM["wall"]
        for x in (-MEDIUM["screw_x"], MEDIUM["screw_x"]):
            body = body + _axis_y_cylinder(
                diameter=2.0 * support_r,
                length=depth,
                x=x,
                y=-MEDIUM["datum"] - MEDIUM["base"] + depth / 2.0,
                z=-19.0,
            )

        relief = _profile_solid(
            name="Edge rail clearance",
            loops=RAIL_RELIEF_PROFILES["edge"],
            y=-MEDIUM["datum"],
            distance=MEDIUM["guide"] + 0.05,
        )
        body = body - relief

        for x in (-MEDIUM["screw_x"], MEDIUM["screw_x"]):
            body = _guide_clearance(body, x=x, z=-19.0)
            body = _mounting_hole(body, x=x, z=-8.0, total_depth=depth)
            body = _locator_pad(body, x=x, z=-19.0)

        seam = _profile_solid(
            name="Edge seam guide",
            loops=SEAM_PROFILES["edge"],
            y=-MEDIUM["datum"] - 0.05,
            distance=MEDIUM["key_h"] + 0.05,
        )
        return (body + seam).with_appearance(SOURCE_RED)


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
