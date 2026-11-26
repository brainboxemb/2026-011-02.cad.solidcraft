"""Two-panel HUB75 tube-supported Display Frame.

This variant preserves the existing panel grid and Medium frame layout, swaps
the outer Edge/Corner couplers to their tube-ready variants, and adds the
source-derived Ø10 tubes plus eight loose reusable tube-clamp occurrences.

The reusable clamp remains Free by default. This document owns one shared
clamp-bore parameter and enables the independent native Installed rule for all
eight clamp occurrences without adding a second configuration-row axis.
"""

from scpf import Always, ConfigRule, Configure, DriveParameter, Param, Placement, assembly

from models.components.hub75_panel.detailed.scpf.model import Hub75Panel
from models.components.hub75_frame_coupler.scpf.family import (
    Hub75FrameCouplerMiddle,
    Hub75FrameCouplerEdgeTube,
    Hub75FrameCouplerCornerLeftTube,
    Hub75FrameCouplerCornerRightTube,
)
from models.components.hub75_frame_tube.scpf.model import Hub75FrameTube10mm
from models.components.hub75_tube_clamp.scpf.model import Hub75TubeClamp


PANEL_PITCH_X = 160.0
PANEL_CENTER_Z = 160.0
FRAME_WIDTH = 320.0
FRAME_HEIGHT = 320.0

TUBE_AXIS_Y = -6.0
TUBE_TOP_Z = 330.0
TUBE_BOTTOM_Z = -10.0

EDGE_CLAMP_XS = (-20.0, 20.0)
CORNER_CLAMP_XS = (-153.0, 153.0)
TOP_CLAMP_ROTATION = ((1, 1, 1), 120)
BOTTOM_CLAMP_ROTATION = ((-1, -1, 1), 120)


def _clamp(
    *,
    name,
    x,
    z,
    rotation,
    tube_d,
    clamp_interference,
    clamp_bore,
):
    """Create one source-derived clamp occurrence with shared fit parameters."""
    return Hub75TubeClamp(
        tube_d=tube_d,
        clamp_interference=clamp_interference,
        clamp_bore=clamp_bore,
        name=name,
        placement=Placement(
            x=x,
            y=TUBE_AXIS_Y,
            z=z,
            rotation=rotation,
        ),
    )


@assembly
class Hub75DisplayFrame2PanelTubeAssembly:
    """Reusable structural frame with assembly-owned clamp-fit parameters."""

    tube_d = 10.0
    clamp_interference = 0.4
    clamp_bore = 9.6

    def build(self):
        def clamp(**kwargs):
            return _clamp(
                tube_d=self.tube_d,
                clamp_interference=self.clamp_interference,
                clamp_bore=self.clamp_bore,
                **kwargs,
            )

        # Same panel placement contract as the accepted non-tube frame.
        left_panel = Hub75Panel(
            name="PanelLeft",
            placement=Placement(
                x=-PANEL_PITCH_X / 2.0,
                z=PANEL_CENTER_Z,
                rotation=((1, 0, 0), 90),
            ),
        )
        right_panel = left_panel.copy(
            name="PanelRight",
            placement=Placement(
                x=PANEL_PITCH_X / 2.0,
                z=PANEL_CENTER_Z,
                rotation=((0, 1, -1), 180),
            ),
        )

        middle = Hub75FrameCouplerMiddle(
            name="MiddleCoupler",
            placement=Placement(z=PANEL_CENTER_Z),
        )

        edge_top = Hub75FrameCouplerEdgeTube(
            name="EdgeCouplerTubeTop",
            placement=Placement(z=FRAME_HEIGHT),
        )
        edge_bottom = edge_top.copy(
            name="EdgeCouplerTubeBottom",
            placement=Placement(
                rotation=((0, 1, 0), 180),
            ),
        )

        corner_left_top = Hub75FrameCouplerCornerLeftTube(
            name="CornerCouplerTubeLeftTop",
            placement=Placement(
                x=-FRAME_WIDTH / 2.0,
                z=FRAME_HEIGHT,
            ),
        )
        corner_left_bottom = corner_left_top.copy(
            name="CornerCouplerTubeLeftBottom",
            placement=Placement(
                x=FRAME_WIDTH / 2.0,
                rotation=((0, 1, 0), 180),
            ),
        )

        corner_right_top = Hub75FrameCouplerCornerRightTube(
            name="CornerCouplerTubeRightTop",
            placement=Placement(
                x=FRAME_WIDTH / 2.0,
                z=FRAME_HEIGHT,
            ),
        )
        corner_right_bottom = corner_right_top.copy(
            name="CornerCouplerTubeRightBottom",
            placement=Placement(
                x=-FRAME_WIDTH / 2.0,
                rotation=((0, 1, 0), 180),
            ),
        )

        # The reusable tube already owns the source 360 mm length as its
        # public default. Do not redundantly override it here; each occurrence
        # only owns its assembly placement.
        tube_top = Hub75FrameTube10mm(
            name="TubeTop",
            placement=Placement(
                y=TUBE_AXIS_Y,
                z=TUBE_TOP_Z,
            ),
        )
        tube_bottom = Hub75FrameTube10mm(
            name="TubeBottom",
            placement=Placement(
                y=TUBE_AXIS_Y,
                z=TUBE_BOTTOM_Z,
            ),
        )

        clamps = [
            clamp(
                name="EdgeClampTopLeft",
                x=EDGE_CLAMP_XS[0],
                z=TUBE_TOP_Z,
                rotation=TOP_CLAMP_ROTATION,
            ),
            clamp(
                name="EdgeClampTopRight",
                x=EDGE_CLAMP_XS[1],
                z=TUBE_TOP_Z,
                rotation=TOP_CLAMP_ROTATION,
            ),
            clamp(
                name="EdgeClampBottomLeft",
                x=EDGE_CLAMP_XS[0],
                z=TUBE_BOTTOM_Z,
                rotation=BOTTOM_CLAMP_ROTATION,
            ),
            clamp(
                name="EdgeClampBottomRight",
                x=EDGE_CLAMP_XS[1],
                z=TUBE_BOTTOM_Z,
                rotation=BOTTOM_CLAMP_ROTATION,
            ),
            clamp(
                name="CornerClampTopLeft",
                x=CORNER_CLAMP_XS[0],
                z=TUBE_TOP_Z,
                rotation=TOP_CLAMP_ROTATION,
            ),
            clamp(
                name="CornerClampTopRight",
                x=CORNER_CLAMP_XS[1],
                z=TUBE_TOP_Z,
                rotation=TOP_CLAMP_ROTATION,
            ),
            clamp(
                name="CornerClampBottomLeft",
                x=CORNER_CLAMP_XS[0],
                z=TUBE_BOTTOM_Z,
                rotation=BOTTOM_CLAMP_ROTATION,
            ),
            clamp(
                name="CornerClampBottomRight",
                x=CORNER_CLAMP_XS[1],
                z=TUBE_BOTTOM_Z,
                rotation=BOTTOM_CLAMP_ROTATION,
            ),
        ]

        result = (
            left_panel
            + right_panel
            + middle
            + edge_top
            + edge_bottom
            + corner_left_top
            + corner_left_bottom
            + corner_right_top
            + corner_right_bottom
            + tube_top
            + tube_bottom
        )
        for clamp in clamps:
            result = result + clamp
        return result


class Hub75DisplayFrame2PanelTube:
    """Configured catalog document with Installed enabled independently."""

    tube_d = 10.0
    clamp_interference = 0.4
    clamp_bore = 9.6

    def build(self):
        frame = Hub75DisplayFrame2PanelTubeAssembly(
            tube_d=self.tube_d,
            clamp_interference=self.clamp_interference,
            clamp_bore=self.clamp_bore,
        )
        return Configure(
            frame,
            active="Medium",
            columns=(Param(self.clamp_bore),),
            rows={
                # #189 owns real Small/Medium/Large coupler geometry. Keep the
                # current physical Medium row honest until that work lands.
                "Medium": ("tube_d-clamp_interference",),
            },
            rules=(
                ConfigRule(
                    "installed",
                    "Installed",
                    enabled=True,
                    condition=Always(),
                    effect=DriveParameter(self.clamp_bore, self.tube_d),
                ),
            ),
        )


Hub75DisplayFrame2PanelTube()
