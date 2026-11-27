"""Two-panel HUB75 Display Frame using the fixed Medium coupler family.

The panel placement is identical to BasicHub75Screen2Panel.  Coupler placement
is derived from the retained native hub75-screen-2panel-couplers source after
normalizing each coupler definition to a reusable local frame.

World axes:
    X: left/right along the display
    Y: front/rear; couplers sit behind the panel plane
    Z: vertical, up
"""

from dataclasses import dataclass

from scpf import Placement, assembly

from models.components.hub75_panel.detailed.scpf.model import Hub75Panel
from models.components.hub75_frame_coupler.scpf.family import (
    Hub75FrameCouplerMiddle,
    Hub75FrameCouplerEdge,
    Hub75FrameCouplerCornerLeft,
    Hub75FrameCouplerCornerRight,
)


PANEL_PITCH_X = 160.0
PANEL_CENTER_Z = 160.0
FRAME_WIDTH = 320.0
FRAME_HEIGHT = 320.0


@assembly
@dataclass
class Hub75DisplayFrame2Panel:
    """Two HUB75 panels plus seven Medium coupler occurrences."""

    coupler_reference_ticks: bool = False
    coupler_reference_holes: bool = False

    def build(self):
        # Same two-panel placement contract as BasicHub75Screen2Panel.
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

        # The native source stores the top coupler definitions in absolute XZ
        # coordinates.  The family normalizes those definitions, so the
        # source identity placements become these clean frame datums.
        middle = Hub75FrameCouplerMiddle(
            reference_ticks=self.coupler_reference_ticks,
            reference_holes=self.coupler_reference_holes,
            name="MiddleCoupler",
            placement=Placement(z=PANEL_CENTER_Z),
        )

        edge_top = Hub75FrameCouplerEdge(
            reference_ticks=self.coupler_reference_ticks,
            reference_holes=self.coupler_reference_holes,
            name="EdgeCouplerTop",
            placement=Placement(z=FRAME_HEIGHT),
        )
        edge_bottom = edge_top.copy(
            name="EdgeCouplerBottom",
            placement=Placement(
                rotation=((0, 1, 0), 180),
            ),
        )

        corner_left_top = Hub75FrameCouplerCornerLeft(
            reference_ticks=self.coupler_reference_ticks,
            reference_holes=self.coupler_reference_holes,
            name="CornerCouplerLeftTop",
            placement=Placement(
                x=-FRAME_WIDTH / 2.0,
                z=FRAME_HEIGHT,
            ),
        )
        # In the native source the second left-corner occurrence is the top
        # definition rotated 180° around Y.  After local-frame normalization
        # that places it at the physical bottom-right corner.
        corner_left_bottom = corner_left_top.copy(
            name="CornerCouplerLeftBottom",
            placement=Placement(
                x=FRAME_WIDTH / 2.0,
                rotation=((0, 1, 0), 180),
            ),
        )

        corner_right_top = Hub75FrameCouplerCornerRight(
            reference_ticks=self.coupler_reference_ticks,
            reference_holes=self.coupler_reference_holes,
            name="CornerCouplerRightTop",
            placement=Placement(
                x=FRAME_WIDTH / 2.0,
                z=FRAME_HEIGHT,
            ),
        )
        # Symmetric source rule: the rotated right definition lands at the
        # physical bottom-left corner.
        corner_right_bottom = corner_right_top.copy(
            name="CornerCouplerRightBottom",
            placement=Placement(
                x=-FRAME_WIDTH / 2.0,
                rotation=((0, 1, 0), 180),
            ),
        )

        return (
            left_panel
            + right_panel
            + middle
            + edge_top
            + edge_bottom
            + corner_left_top
            + corner_left_bottom
            + corner_right_top
            + corner_right_bottom
        )


Hub75DisplayFrame2Panel()
