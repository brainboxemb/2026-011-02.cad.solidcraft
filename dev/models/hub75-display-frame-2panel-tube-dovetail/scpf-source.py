"""Two-panel HUB75 tube frame using male clamps and female coupler receivers."""

from scpf import Always, ConfigRule, Configure, DriveParameter, Param, assembly
from models.components.hub75_frame_coupler.scpf.family import (
    Hub75FrameCouplerEdgeTubeReceiver,
    Hub75FrameCouplerCornerLeftTubeReceiver,
    Hub75FrameCouplerCornerRightTubeReceiver,
)
from models.components.hub75_tube_clamp.scpf.male import Hub75TubeClampMale
from models.subassemblies.hub75_display_frame_2panel.scpf.tube_frame import _build_tube_frame


@assembly
class Hub75DisplayFrame2PanelTubeDovetailAssembly:
    tube_d = 10.0
    clamp_interference = 0.4
    clamp_bore = 9.6

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
        )


class Hub75DisplayFrame2PanelTubeDovetail:
    tube_d = 10.0
    clamp_interference = 0.4
    clamp_bore = 9.6

    def build(self):
        frame = Hub75DisplayFrame2PanelTubeDovetailAssembly(
            tube_d=self.tube_d,
            clamp_interference=self.clamp_interference,
            clamp_bore=self.clamp_bore,
        )
        return Configure(
            frame,
            active="Medium",
            columns=(Param(self.clamp_bore),),
            rows={"Medium": ("tube_d-clamp_interference",)},
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


Hub75DisplayFrame2PanelTubeDovetail()
