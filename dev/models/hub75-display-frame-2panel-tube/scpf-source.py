"""Two-panel HUB75 tube-supported Display Frame.

This variant preserves the existing panel grid and Medium frame layout, swaps
the outer Edge/Corner couplers to their tube-ready variants, and adds the
source-derived Ø10 tubes plus eight loose reusable tube-clamp occurrences.

The clamp component itself remains Free by default. Independent Installed state
is added later through CAD issue #204 when the released Forge state capability
is available; this structural assembly deliberately does not emulate it.
"""

from scpf import Placement, assembly

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

TUBE_LENGTH = 360.0
TUBE_AXIS_Y = -6.0
TUBE_TOP_Z = 330.0
TUBE_BOTTOM_Z = -10.0

EDGE_CLAMP_XS = (-20.0, 20.0)
CORNER_CLAMP_XS = (-153.0, 153.0)
TOP_CLAMP_ROTATION = ((1, 1, 1), 120)
BOTTOM_CLAMP_ROTATION = ((-1, -1, 1), 120)


def _clamp(*, name, x, z, rotation):
    """Create one loose source-derived clamp occurrence."""
    return Hub75TubeClamp(
        name=name,
        placement=Placement(
            x=x,
            y=TUBE_AXIS_Y,
            z=z,
            rotation=rotation,
        ),
    )


@assembly
class Hub75DisplayFrame2PanelTube:
    """Two panels, tube-ready frame hardware, two tubes and eight clamps."""

    def build(self):
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

        tube_top = Hub75FrameTube10mm(
            name="TubeTop",
            length=TUBE_LENGTH,
            placement=Placement(
                y=TUBE_AXIS_Y,
                z=TUBE_TOP_Z,
            ),
        )
        # Reuse the already-authored tube component explicitly. A second
        # constructor call with the same published length is de-duplicated by
        # Forge, but v0.22.0 does not retain that second call's placement.
        # An occurrence copy preserves one physical tube definition and emits
        # the required independent bottom placement.
        tube_bottom = tube_top.copy(
            name="TubeBottom",
            placement=Placement(
                y=TUBE_AXIS_Y,
                z=TUBE_BOTTOM_Z,
            ),
        )

        clamps = [
            _clamp(
                name="EdgeClampTopLeft",
                x=EDGE_CLAMP_XS[0],
                z=TUBE_TOP_Z,
                rotation=TOP_CLAMP_ROTATION,
            ),
            _clamp(
                name="EdgeClampTopRight",
                x=EDGE_CLAMP_XS[1],
                z=TUBE_TOP_Z,
                rotation=TOP_CLAMP_ROTATION,
            ),
            _clamp(
                name="EdgeClampBottomLeft",
                x=EDGE_CLAMP_XS[0],
                z=TUBE_BOTTOM_Z,
                rotation=BOTTOM_CLAMP_ROTATION,
            ),
            _clamp(
                name="EdgeClampBottomRight",
                x=EDGE_CLAMP_XS[1],
                z=TUBE_BOTTOM_Z,
                rotation=BOTTOM_CLAMP_ROTATION,
            ),
            _clamp(
                name="CornerClampTopLeft",
                x=CORNER_CLAMP_XS[0],
                z=TUBE_TOP_Z,
                rotation=TOP_CLAMP_ROTATION,
            ),
            _clamp(
                name="CornerClampTopRight",
                x=CORNER_CLAMP_XS[1],
                z=TUBE_TOP_Z,
                rotation=TOP_CLAMP_ROTATION,
            ),
            _clamp(
                name="CornerClampBottomLeft",
                x=CORNER_CLAMP_XS[0],
                z=TUBE_BOTTOM_Z,
                rotation=BOTTOM_CLAMP_ROTATION,
            ),
            _clamp(
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


Hub75DisplayFrame2PanelTube()
