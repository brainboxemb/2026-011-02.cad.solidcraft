"""Qualification assembly for the MFT rail corner bracket.

Two short MountingRailM8 pieces meet at 90 degrees with their C-openings facing
outward. The bracket occupies only the inside corner and uses the first two
round perforations on each rail.
"""

from scpf import Placement

from models.components.mft_rail_corner_bracket.scpf.model import (
    MFTRailCornerBracket,
)
from models.components.mounting_rail_m8.scpf.model import MountingRailM8


class MFTRailCornerAssembly:
    rail_length = 150.0
    rail_repeat_count = 1
    rail_repeat_pitch = 100.0

    RAIL_Z = -MountingRailM8.PROFILE_WIDTH / 2

    # Same orientation contracts already used by the Simple MFT frame:
    # X rail: length +X, opening -Y.
    X_RAIL_ROTATION = ((1, 1, -1), 120)
    # Y rail: length +Y, opening -X.
    Y_RAIL_ROTATION = ((0, -1, 0), 90)

    def build(self):
        x_rail = MountingRailM8(
            length=self.rail_length,
            repeat_count=self.rail_repeat_count,
            repeat_pitch=self.rail_repeat_pitch,
            placement=Placement(
                x=0,
                y=0,
                z=self.RAIL_Z,
                rotation=self.X_RAIL_ROTATION,
            ),
        )

        y_rail = MountingRailM8(
            length=self.rail_length,
            repeat_count=self.rail_repeat_count,
            repeat_pitch=self.rail_repeat_pitch,
            placement=Placement(
                x=0,
                y=0,
                z=self.RAIL_Z,
                rotation=self.Y_RAIL_ROTATION,
            ),
        )

        bracket = MFTRailCornerBracket()

        return x_rail + y_rail + bracket


MFTRailCornerAssembly()
