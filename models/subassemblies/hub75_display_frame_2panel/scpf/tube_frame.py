"""Shared two-panel HUB75 tube-frame layout and existing rail-interface variant."""

from dataclasses import dataclass

from scpf import Placement, assembly

from models.components.hub75_panel.detailed.scpf.model import Hub75Panel
from models.components.hub75_frame_coupler.scpf.center_family import Hub75FrameCouplerCenter
from models.components.hub75_frame_coupler.scpf.edge_family import Hub75FrameCouplerEdgeTube
from models.components.hub75_frame_coupler.scpf.corner_family import (
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


def _clamp(*, component, name, x, z, rotation, tube_d, clamp_interference, clamp_bore):
    return component(
        tube_d=tube_d,
        clamp_interference=clamp_interference,
        clamp_bore=clamp_bore,
        name=name,
        placement=Placement(x=x, y=TUBE_AXIS_Y, z=z, rotation=rotation),
    )


def _build_tube_frame(
    *,
    edge_component,
    corner_left_component,
    corner_right_component,
    clamp_component,
    interface_label,
    tube_d,
    clamp_interference,
    clamp_bore,
    coupler_reference_ticks,
    coupler_reference_holes,
):
    def clamp(**kwargs):
        return _clamp(
            component=clamp_component,
            tube_d=tube_d,
            clamp_interference=clamp_interference,
            clamp_bore=clamp_bore,
            **kwargs,
        )

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
    center = Hub75FrameCouplerCenter(
        reference_ticks=coupler_reference_ticks,
        reference_holes=coupler_reference_holes,
        name="CenterCoupler",
        placement=Placement(z=PANEL_CENTER_Z),
    )

    edge_top = edge_component(
        reference_ticks=coupler_reference_ticks,
        reference_holes=coupler_reference_holes,
        name=f"EdgeCoupler{interface_label}Top",
        placement=Placement(z=FRAME_HEIGHT),
    )
    edge_bottom = edge_top.copy(
        name=f"EdgeCoupler{interface_label}Bottom",
        placement=Placement(rotation=((0, 1, 0), 180)),
    )

    corner_left_top = corner_left_component(
        reference_ticks=coupler_reference_ticks,
        reference_holes=coupler_reference_holes,
        name=f"CornerCoupler{interface_label}LeftTop",
        placement=Placement(x=-FRAME_WIDTH / 2.0, z=FRAME_HEIGHT),
    )
    corner_left_bottom = corner_left_top.copy(
        name=f"CornerCoupler{interface_label}LeftBottom",
        placement=Placement(x=FRAME_WIDTH / 2.0, rotation=((0, 1, 0), 180)),
    )
    corner_right_top = corner_right_component(
        reference_ticks=coupler_reference_ticks,
        reference_holes=coupler_reference_holes,
        name=f"CornerCoupler{interface_label}RightTop",
        placement=Placement(x=FRAME_WIDTH / 2.0, z=FRAME_HEIGHT),
    )
    corner_right_bottom = corner_right_top.copy(
        name=f"CornerCoupler{interface_label}RightBottom",
        placement=Placement(x=-FRAME_WIDTH / 2.0, rotation=((0, 1, 0), 180)),
    )

    tube_top = Hub75FrameTube10mm(
        name="TubeTop",
        placement=Placement(y=TUBE_AXIS_Y, z=TUBE_TOP_Z),
    )
    tube_bottom = Hub75FrameTube10mm(
        name="TubeBottom",
        placement=Placement(y=TUBE_AXIS_Y, z=TUBE_BOTTOM_Z),
    )

    clamps = [
        clamp(name="EdgeClampTopLeft", x=EDGE_CLAMP_XS[0], z=TUBE_TOP_Z, rotation=TOP_CLAMP_ROTATION),
        clamp(name="EdgeClampTopRight", x=EDGE_CLAMP_XS[1], z=TUBE_TOP_Z, rotation=TOP_CLAMP_ROTATION),
        clamp(name="EdgeClampBottomLeft", x=EDGE_CLAMP_XS[0], z=TUBE_BOTTOM_Z, rotation=BOTTOM_CLAMP_ROTATION),
        clamp(name="EdgeClampBottomRight", x=EDGE_CLAMP_XS[1], z=TUBE_BOTTOM_Z, rotation=BOTTOM_CLAMP_ROTATION),
        clamp(name="CornerClampTopLeft", x=CORNER_CLAMP_XS[0], z=TUBE_TOP_Z, rotation=TOP_CLAMP_ROTATION),
        clamp(name="CornerClampTopRight", x=CORNER_CLAMP_XS[1], z=TUBE_TOP_Z, rotation=TOP_CLAMP_ROTATION),
        clamp(name="CornerClampBottomLeft", x=CORNER_CLAMP_XS[0], z=TUBE_BOTTOM_Z, rotation=BOTTOM_CLAMP_ROTATION),
        clamp(name="CornerClampBottomRight", x=CORNER_CLAMP_XS[1], z=TUBE_BOTTOM_Z, rotation=BOTTOM_CLAMP_ROTATION),
    ]

    result = (
        left_panel + right_panel + center + edge_top + edge_bottom
        + corner_left_top + corner_left_bottom
        + corner_right_top + corner_right_bottom
        + tube_top + tube_bottom
    )
    for clamp_instance in clamps:
        result = result + clamp_instance
    return result


@assembly
@dataclass
class Hub75DisplayFrame2PanelTubeAssembly:
    tube_d: float = 10.0
    clamp_interference: float = 0.4
    clamp_bore: float = 9.6
    coupler_reference_ticks: bool = False
    coupler_reference_holes: bool = False

    def build(self):
        return _build_tube_frame(
            edge_component=Hub75FrameCouplerEdgeTube,
            corner_left_component=Hub75FrameCouplerCornerLeftTube,
            corner_right_component=Hub75FrameCouplerCornerRightTube,
            clamp_component=Hub75TubeClamp,
            interface_label="Tube",
            tube_d=self.tube_d,
            clamp_interference=self.clamp_interference,
            clamp_bore=self.clamp_bore,
            coupler_reference_ticks=self.coupler_reference_ticks,
            coupler_reference_holes=self.coupler_reference_holes,
        )


@dataclass
class Hub75DisplayFrame2PanelTube:
    tube_d: float = 10.0
    clamp_interference: float = 0.4
    clamp_bore: float = 9.6
    coupler_reference_ticks: bool = False
    coupler_reference_holes: bool = False

    def build(self):
        frame = Hub75DisplayFrame2PanelTubeAssembly(
            tube_d=self.tube_d,
            clamp_interference=self.clamp_interference,
            clamp_bore=self.clamp_bore,
            coupler_reference_ticks=self.coupler_reference_ticks,
            coupler_reference_holes=self.coupler_reference_holes,
        )
        frame.configure(
            active="Medium",
            columns=(self.clamp_bore,),
            # This mounted parent owns the effective clamp fit explicitly.
            # Reusable clamp components do not carry a global Installed rule.
            rows={"Medium": ("tube_d",)},
        )
        return frame


Hub75DisplayFrame2PanelTube()
