"""Center HUB75 frame-coupler implementation."""

from dataclasses import dataclass

from scpf import component

from models.components.hub75_frame_coupler.scpf.features import (
    _apply_reference_pattern,
    _guide_clearance,
    _join_tapered_seam_guide,
    _locator_pad,
    _mounting_hole,
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
        base = _profile_solid(
            name="Center base profile",
            loops=_center_base_profiles(p),
            y=-p["mid_datum"],
            distance=-p["mid_base"],
        )
        guide = _multi_profile_solid(
            name="Center guide profiles",
            loops=_center_guide_profiles(p),
            y=-p["mid_datum"] - 0.05,
            distance=p["mid_guide"] + 0.05,
        )
        body = base + guide

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
            profile_key="center",
            steps=8,
        )
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
