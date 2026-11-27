"""Two-panel HUB75 tube frame using male clamps and female coupler receivers."""

from dataclasses import dataclass

from scpf import assembly
from models.components.hub75_frame_coupler.scpf.family import (
    Hub75FrameCouplerEdgeTubeReceiver,
    Hub75FrameCouplerCornerLeftTubeReceiver,
    Hub75FrameCouplerCornerRightTubeReceiver,
)
from models.components.hub75_tube_clamp.scpf.male import Hub75TubeClampMale
from models.subassemblies.hub75_display_frame_2panel.scpf.tube_frame import _build_tube_frame


@assembly
@dataclass
class Hub75DisplayFrame2PanelTubeDovetailAssembly:
    tube_d: float = 10.0
    clamp_interference: float = 0.4
    clamp_bore: float = 9.6
    coupler_reference_ticks: bool = False
    coupler_reference_holes: bool = False

    def build(self):
        return _build_tube_frame(
            edge_component=Hub75FrameCouplerEdgeTubeReceiver,
            corner_left_component=Hub75FrameCouplerCornerLeftTubeReceiver,
            corner_right_component=Hub75FrameCouplerCornerRightTubeReceiver,
            clamp_component=Hub75TubeClampMale,
            interface_label="Receiver",
            tube_d=self.tube_d,
            clamp_interference=self.clamp_interference,
            clamp_bore=self.clamp_bore,
            coupler_reference_ticks=self.coupler_reference_ticks,
            coupler_reference_holes=self.coupler_reference_holes,
        )


@dataclass
class Hub75DisplayFrame2PanelTubeDovetail:
    tube_d: float = 10.0
    clamp_interference: float = 0.4
    clamp_bore: float = 9.6
    coupler_reference_ticks: bool = False
    coupler_reference_holes: bool = False

    def build(self):
        frame = Hub75DisplayFrame2PanelTubeDovetailAssembly(
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
            rows={"Medium": ("tube_d",)},
        )
        return frame


Hub75DisplayFrame2PanelTubeDovetail()
