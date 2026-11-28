"""Shared parameter/source configuration for HUB75 frame couplers."""

from models.components.hub75_frame_coupler.scpf.parametric_source import (
    source_circle_centers,
    source_parameters,
    source_profiles,
)

SOURCE_RED = "#B80D0A"

_SOURCE_FEATURES = {
    "center": {
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

_CONFIGURED_PARAMETERS = ("mid_size", "mid_wall", "mid_base", "mid_guide")
_PANEL_PIN_FEATURE = "panel_pin_pass_through"


def _parameters(owner):
    """Resolve the retained source graph from the shared configured inputs."""
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


def _component_parameters():
    return {
        "mid_size": 80.0,
        "mid_wall": 4.0,
        "mid_base": 3.0,
        "mid_guide": 6.0,
    }


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
