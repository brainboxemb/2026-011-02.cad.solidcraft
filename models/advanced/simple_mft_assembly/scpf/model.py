"""Simple MFT assembly with guide rail and two 1 m M8 support rails.

World axes:
    X: left/right across the worktop width
    Y: front/rear across the worktop depth
    Z: up

The two mounting rails run along +X. Their left ends align with the worktop left
edge, so the full 1000 mm rails extend 195 mm beyond the 805 mm worktop on the
right. Both perforation sequences therefore run in the same left-to-right
direction.

The mounting-rail component is locally built along +Y with its C-opening toward
-Z. Two different 120-degree occurrence rotations map local +Y to world +X,
while mapping the opening to opposite outward Y directions.
"""
from scpf import Placement, half

from models.components.simple_mft.scpf.model import SimpleMFT
from models.components.guide_rail.scpf.model import GuideRail
from models.components.guide_rail.scpf.profiles import get_profile
from models.components.mounting_rail_m8.scpf.model import MountingRailM8


class SimpleMFTAssembly:
    worktop_thickness = SimpleMFT.thickness
    guide_rail_length = 800.0

    GUIDE_RAIL_PROFILE = "festool"

    SUPPORT_RAIL_LENGTH = 1000.0
    SUPPORT_RAIL_REPEAT_COUNT = 10
    SUPPORT_RAIL_REPEAT_PITCH = 100.0

    # The 27 mm mounting-rail profile becomes vertical after the support-rail
    # rotations. Put its upper edge at Z=0 so the MFT underside rests on it.
    SUPPORT_RAIL_Z = -MountingRailM8.PROFILE_WIDTH / 2

    # Axis-angle rotations:
    #   local +Y (rail length) -> world +X for BOTH rails;
    #   local -Z (C opening)   -> world +Y / -Y respectively.
    UPPER_RAIL_ROTATION = ((1, 1, -1), 120)
    LOWER_RAIL_ROTATION = ((-1, -1, -1), 120)

    def build(self):
        profile = get_profile(self.GUIDE_RAIL_PROFILE)

        worktop = SimpleMFT(
            thickness=self.worktop_thickness,
        )

        guide_rail = GuideRail(
            length=self.guide_rail_length,
            profile=self.GUIDE_RAIL_PROFILE,
            placement=Placement(
                x=-half(profile.WIDTH),
                z=self.worktop_thickness,
            ),
        )

        worktop_width = float(SimpleMFT.width)
        worktop_depth = float(SimpleMFT.depth)

        rail_x = -worktop_width / 2
        upper_y = worktop_depth / 2
        lower_y = -worktop_depth / 2

        upper_support = MountingRailM8(
            length=self.SUPPORT_RAIL_LENGTH,
            repeat_count=self.SUPPORT_RAIL_REPEAT_COUNT,
            repeat_pitch=self.SUPPORT_RAIL_REPEAT_PITCH,
            placement=Placement(
                x=rail_x,
                y=upper_y,
                z=self.SUPPORT_RAIL_Z,
                rotation=self.UPPER_RAIL_ROTATION,
            ),
        )

        lower_support = MountingRailM8(
            length=self.SUPPORT_RAIL_LENGTH,
            repeat_count=self.SUPPORT_RAIL_REPEAT_COUNT,
            repeat_pitch=self.SUPPORT_RAIL_REPEAT_PITCH,
            placement=Placement(
                x=rail_x,
                y=lower_y,
                z=self.SUPPORT_RAIL_Z,
                rotation=self.LOWER_RAIL_ROTATION,
            ),
        )

        return worktop + guide_rail + upper_support + lower_support


SimpleMFTAssembly()
