"""Two physically upright HUB75 panels in the XZ display plane.

This is a separate fixed product layout alongside the five-panel
BasicHub75Screen. It reuses the same detailed Hub75Panel component and the same
alternating orientation convention.

World coordinates:
    X: left/right along the display
    Y: front/rear panel depth
    Z: vertical, up
"""

from scpf import Placement, half

from models.components.hub75_panel.detailed.scpf.model import Hub75Panel

# Fixed two-panel 160 x 320 mm nominal grid.
NOMINAL_PITCH_X = 160.0
NOMINAL_HEIGHT = 320.0


class BasicHub75Screen2Panel:
    def build(self):
        center_z = half(NOMINAL_HEIGHT)
        half_pitch = half(NOMINAL_PITCH_X)

        left = Hub75Panel(
            placement=Placement(
                x=-half_pitch,
                z=center_z,
                rotation=((1, 0, 0), 90),
            )
        )

        right = left.copy(
            placement=Placement(
                x=half_pitch,
                z=center_z,
                rotation=((0, 1, -1), 180),
            )
        )

        return left + right


BasicHub75Screen2Panel()
