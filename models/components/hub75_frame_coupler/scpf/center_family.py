"""Center HUB75 frame-coupler implementation."""

from dataclasses import dataclass

from scpf import component

from models.components.hub75_frame_coupler.scpf.features import (
    _apply_reference_pattern,
    _axis_y_cylinder,
    _join_tapered_seam_guide,
    _multi_profile_solid,
    _profile_solid,
    _replace_arc_through_with_centers,
)
from models.components.hub75_frame_coupler.scpf.parameters import (
    SOURCE_RED,
    _CONFIGURED_PARAMETERS,
    _ConfiguredCouplerRoot,
    _parameters,
    _source_profile,
)


def _center_base_profiles(p):
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
        _source_profile("center", "base", p),
        centers,
        clockwise,
    )


def _center_guide_profiles(p):
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
        _source_profile("center", "guide", p),
        centers,
        clockwise,
    )




@component(include=_CONFIGURED_PARAMETERS)
@dataclass
class Hub75FrameCouplerCenter:
    """Reusable frame-coupler component at the panel seam midpoint."""

    mid_size: float = 80.0
    mid_wall: float = 4.0
    mid_base: float = 3.0
    mid_guide: float = 6.0
    reference_ticks: bool = False
    reference_holes: bool = False

    def build(self):
        p = _parameters(self)
        datum = p["mid_datum"]
        base_depth = p["mid_base"]
        guide_depth = p["mid_guide"]
        screw_d = p["mid_screw_d"]

        # Start with the accepted symmetric base contour and the four guide
        # regions. A later change may author these from mirrored source geometry;
        # this cleanup deliberately preserves the current history.
        base = _profile_solid(
            name="Center base profile",
            loops=_center_base_profiles(p),
            y=-datum,
            distance=-base_depth,
        )
        guide = _multi_profile_solid(
            name="Center guide profiles",
            loops=_center_guide_profiles(p),
            y=-datum - 0.05,
            distance=guide_depth + 0.05,
        )
        body = base + guide

        # Open the guide around the two panel-bushing positions.
        for x, z in (
            (-p["mid_screw_x"], p["mid_bushing_z"]),
            (p["mid_screw_x"], -p["mid_bushing_z"]),
        ):
            body = body - _axis_y_cylinder(
                diameter=2.0 * (p["mid_bushing_r"] + p["mid_bushing_gap"]),
                length=guide_depth + 0.1,
                x=x,
                y=-datum + guide_depth / 2.0,
                z=z,
            )

        # Drill the two mounting positions. Each position keeps the source
        # bore, short rear relief and deeper tube clearance visible as one step.
        for x in (-p["mid_screw_x"], p["mid_screw_x"]):
            body = body - _axis_y_cylinder(
                diameter=screw_d,
                length=base_depth + 0.2,
                x=x,
                y=-datum - base_depth / 2.0,
                z=0.0,
            )
            body = body - _axis_y_cylinder(
                diameter=screw_d + 0.8,
                length=0.2,
                x=x,
                y=-datum - base_depth + 0.1,
                z=0.0,
            )
            body = body - _axis_y_cylinder(
                diameter=2.0 * (p["mid_tube_r"] + p["mid_tube_gap"]),
                length=p["mid_tube_depth"],
                x=x,
                y=-datum - p["mid_tube_depth"] / 2.0,
                z=0.0,
            )

        # Build the two locator bosses on the diagonal bushing positions.
        for x, z in (
            (-p["mid_screw_x"], p["mid_bushing_z"]),
            (p["mid_screw_x"], -p["mid_bushing_z"]),
        ):
            body = body + _axis_y_cylinder(
                diameter=2.0 * p["mid_pad_r"],
                length=p["mid_pad_h"],
                x=x,
                y=-datum + p["mid_pad_h"] / 2.0,
                z=z,
            )
            body = body + _axis_y_cylinder(
                diameter=2.0 * p["mid_pin_r"],
                length=p["mid_pin_h"],
                x=x,
                y=-datum + p["mid_pad_h"] + p["mid_pin_h"] / 2.0,
                z=z,
            )

        # Join the shallow tapered seam key after the structural features.
        body = _join_tapered_seam_guide(
            body,
            p=p,
            profile_key="center",
            steps=8,
        )

        # Reference marks/holes are optional inspection aids, not base geometry.
        body = _apply_reference_pattern(
            body,
            p=p,
            profile_key="center",
            reference_ticks=self.reference_ticks,
            reference_holes=self.reference_holes,
        )
        return body.with_appearance(SOURCE_RED)


class Hub75FrameCouplerCenterModel(_ConfiguredCouplerRoot):
    component_type = staticmethod(Hub75FrameCouplerCenter)
