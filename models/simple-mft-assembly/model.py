"""Simple MFT worktop with one reusable 1080 mm guide rail.

World axes:
    X: left/right across the worktop width
    Y: front/rear along the worktop depth and guide-rail length
    Z: up

The rail is deliberately placed by this assembly. GuideRail owns only its local
profile and length; SimpleMFT owns only the worktop geometry.
"""
from scpf import Placement, half

from models.advanced.simple_mft.scpf.model import SimpleMFT
from models.components.guide_rail.scpf.model import GuideRail
from models.components.guide_rail.scpf.profiles import get_profile


class SimpleMFTAssembly:
    # Shared parent parameter: changing this moves the worktop top face and the
    # rail together instead of leaving the rail at a hard-coded Z=18 position.
    worktop_thickness = SimpleMFT.thickness

    # Festool MFT/3 uses FS 1080/2. Keep the length editable in the assembly.
    guide_rail_length = 1080.0

    GUIDE_RAIL_PROFILE = "festool"

    def build(self):
        profile = get_profile(self.GUIDE_RAIL_PROFILE)

        worktop = SimpleMFT(
            thickness=self.worktop_thickness,
        )

        # GuideRail's fixed profile starts at local X=0 and extends to +WIDTH,
        # while its length is already symmetric about local Y=0. Shifting it by
        # half its width centres the rail over worktop X=0 without a rotation.
        #
        # Z uses the same parent parameter passed into SimpleMFT.thickness, so
        # the rail remains on the top face when worktop_thickness is edited in
        # the saved SolidCraft model.
        guide_rail = GuideRail(
            length=self.guide_rail_length,
            profile=self.GUIDE_RAIL_PROFILE,
            placement=Placement(
                x=-half(profile.WIDTH),
                z=self.worktop_thickness,
            ),
        )

        return worktop + guide_rail


SimpleMFTAssembly()
