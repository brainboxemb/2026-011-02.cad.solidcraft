"""Simple MFT assembly with guide rail and a three-sided M8 support frame.

World axes:
    X: left/right across the worktop width
    Y: front/rear across the worktop depth
    Z: up

The two long mounting rails run along +X and a shorter rail closes the left
side between them. The long rails are shifted one 18 mm profile-depth to the
right so the left cross rail can meet them without overlapping their channel
ends. Both long perforation sequences run in the same left-to-right direction.

The mounting-rail component is locally built along +Y with its C-opening toward
+Z. Two different 120-degree occurrence rotations map local +Y to world +X,
while mapping the opening to opposite outward Y directions.
"""
from scpf import Anchor, Box, Placement, component, half

from models.components.simple_mft.scpf.model import SimpleMFT
from models.components.guide_rail.scpf.model import GuideRail
from models.components.guide_rail.scpf.profiles import get_profile
from models.components.mounting_rail_m8.scpf.model import MountingRailM8
from models.components.flex_bench_dog.scpf.model import FlexBenchDog


@component(include="*")
class SimpleMFTRightExtension:
    width = 195.0
    depth = 555.0
    thickness = 18.0

    def build(self):
        return Box(
            self.width,
            self.depth,
            self.thickness,
            anchor=Anchor.BOTTOM,
        ).with_material(
            "MDF",
            density_g_cm3=0.70,
            color="#C8A46A",
        )


class SimpleMFTAssembly:
    worktop_thickness = SimpleMFT.thickness
    guide_rail_length = 800.0

    GUIDE_RAIL_PROFILE = "festool"
    GUIDE_RAIL_X_SHIFT = 414.0

    SUPPORT_RAIL_LENGTH = 1000.0
    SUPPORT_RAIL_REPEAT_COUNT = 10
    SUPPORT_RAIL_REPEAT_PITCH = 100.0

    LEFT_RAIL_REPEAT_COUNT = 5

    # Shift the two long rails one profile depth to the right. The left cross
    # rail occupies that 18 mm X strip and runs between the inner edges of the
    # long rails, keeping the channel ends accessible instead of overlapping.
    SUPPORT_RAIL_X_OFFSET = MountingRailM8.PROFILE_HEIGHT

    LEFT_RAIL_ROTATION = ((0, -1, 0), 90)

    # The 27 mm mounting-rail profile becomes vertical after the support-rail
    # rotations. Put its upper edge at Z=0 so the MFT underside rests on it.
    SUPPORT_RAIL_Z = -MountingRailM8.PROFILE_WIDTH / 2

    # The local +Z profile depth becomes the outward world-Y direction.
    # Inset each rail by the full 18 mm profile depth so its outer face is
    # flush with the corresponding worktop edge and the complete rail sits
    # underneath the plate instead of just outside it.
    SUPPORT_RAIL_INSET = MountingRailM8.PROFILE_HEIGHT

    # Axis-angle rotations:
    #   local +Y (rail length) -> world +X for BOTH rails;
    #   local +Z (C opening)   -> world +Y / -Y respectively.
    UPPER_RAIL_ROTATION = ((-1, -1, -1), 120)
    LOWER_RAIL_ROTATION = ((1, 1, -1), 120)

    def build(self):
        profile = get_profile(self.GUIDE_RAIL_PROFILE)

        worktop = SimpleMFT(
            thickness=self.worktop_thickness,
        )

        guide_rail = GuideRail(
            length=self.guide_rail_length,
            profile=self.GUIDE_RAIL_PROFILE,
            placement=Placement(
                x=self.GUIDE_RAIL_X_SHIFT - half(profile.WIDTH),
                z=self.worktop_thickness,
            ),
        )

        worktop_width = float(SimpleMFT.width)
        worktop_depth = float(SimpleMFT.depth)
        dog_hole_pitch = float(SimpleMFT.hole_pitch)

        # Place one reusable bench dog in the rightmost hole of the centre row.
        # The dog model uses its local Z=0 as the worktop top surface datum.
        rightmost_dog = FlexBenchDog(
            placement=Placement(
                x=4 * dog_hole_pitch,
                y=0,
                z=self.worktop_thickness,
            ),
        )

        extension_width = self.SUPPORT_RAIL_LENGTH - worktop_width
        extension_x = worktop_width / 2 + extension_width / 2

        right_extension = SimpleMFTRightExtension(
            width=extension_width,
            depth=worktop_depth,
            thickness=self.worktop_thickness,
            placement=Placement(x=extension_x),
        )

        rail_x = -worktop_width / 2 + self.SUPPORT_RAIL_X_OFFSET
        upper_y = worktop_depth / 2 - self.SUPPORT_RAIL_INSET
        lower_y = -worktop_depth / 2 + self.SUPPORT_RAIL_INSET

        left_rail_length = worktop_depth - 2 * self.SUPPORT_RAIL_INSET
        left_support = MountingRailM8(
            length=left_rail_length,
            repeat_count=self.LEFT_RAIL_REPEAT_COUNT,
            repeat_pitch=self.SUPPORT_RAIL_REPEAT_PITCH,
            placement=Placement(
                x=rail_x,
                y=lower_y,
                z=self.SUPPORT_RAIL_Z,
                rotation=self.LEFT_RAIL_ROTATION,
            ),
        )

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

        return (
            worktop
            + right_extension
            + guide_rail
            + upper_support
            + lower_support
            + left_support
            + rightmost_dog
        )


SimpleMFTAssembly()
