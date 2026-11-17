"""Simple MFT assembly with a reusable 1080 mm guide rail.

The worktop owns its geometry. GuideRail owns only its local extrusion profile.
This assembly owns the guide-rail placement.

World axes:
    X: left/right across the worktop width
    Y: front/rear along the worktop depth and guide-rail length
    Z: up
"""
from scpf import Placement

from models.advanced.simple_mft.scpf.model import SimpleMFT
from models.components.guide_rail.scpf.model import GuideRail


class SimpleMFTAssembly:
    GUIDE_RAIL_LENGTH = 1080.0

    def build(self):
        worktop = SimpleMFT().build()

        guide_rail = GuideRail(
            length=self.GUIDE_RAIL_LENGTH,
            placement=Placement(
                x=-GuideRail.TSO_H_TOTAL_WIDTH / 2,
                z=SimpleMFT.thickness,
            ),
        )

        return worktop + guide_rail
