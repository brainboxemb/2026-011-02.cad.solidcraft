"""Five physically upright HUB75 panels in the XZ display plane.

World coordinates (shared with the wooden-frame project):
    X: left/right along the display
    Y: front/rear panel depth (front face at Y=0, rear at Y=-14.5)
    Z: vertical, up

The detailed Hub75Panel component is authored in its native XY plane with
its depth along +Z. Each occurrence gets one complete constructor/copy
Placement. Alternating panels use one composed absolute axis-angle rotation
(180 degrees about [0, 1, -1]).
"""
from scpf import Placement, half

from models.components.hub75_panel.detailed.scpf.model import Hub75Panel

# This model represents one fixed five-panel 160 x 320 mm nominal grid.
# These dimensions define the product layout; they are not editable native
# SolidCraft parameters. The physical panel envelope remains in
# models/components/hub75_panel/detailed/scpf/model.py.
NOMINAL_PITCH_X = 160.0
NOMINAL_HEIGHT = 320.0


class BasicHub75Screen:
    def build(self):
        center_z = half(NOMINAL_HEIGHT)

        central = Hub75Panel(
            placement=Placement(
                z=center_z,
                rotation=((1, 0, 0), 90),
            )
        )
        screen = central

        for index in (0, 1, 3, 4):
            x = (index - 2) * NOMINAL_PITCH_X
            rotation = (
                ((0, 1, -1), 180)
                if index in (1, 3)
                else ((1, 0, 0), 90)
            )
            screen = screen + central.copy(
                placement=Placement(
                    x=x,
                    z=center_z,
                    rotation=rotation,
                )
            )

        return screen
