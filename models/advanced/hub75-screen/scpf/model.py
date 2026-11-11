"""Five physically upright HUB75 panels in the XZ display plane.

World coordinates (shared with the wooden-frame project):
    X: left/right along the display
    Y: front/rear panel depth (front face at Y=0, rear at Y=-14.5)
    Z: vertical, up

The detailed Hub75Panel component is authored in its native XY plane with
its depth along +Z. Rotate each occurrence +90 degrees around X to stand
it upright. Alternating panels require one composed absolute axis-angle
rotation (180 degrees about [0, 1, -1]); SCPF currently replaces,
rather than composes, consecutive rotate() calls.
All occurrence rotations happen BEFORE their horizontal placement.
"""
from scpf import component
from components.hub75 import Hub75Panel as Hub75PanelDefinition

Hub75Panel = component(Hub75PanelDefinition)


class BasicHub75Screen:
    nominal_pitch_x = 160.0
    nominal_height = 320.0

    def build(self):
        # The native panel has its display face in XY and its rear in +Z.
        # Rotate to XZ so the 319.71 mm long side points upwards in world Z.
        # Keep the master at X=0: copies inherit the master's transformation.
        central = Hub75Panel().rotate(axis=(1, 0, 0), degrees=90)
        screen = central

        for index in (0, 1, 3, 4):
            x = (index - 2) * self.nominal_pitch_x
            occurrence = central.copy()
            if index in (1, 3):
                # Compose the upright X+90 and world Y+180 rotations as ONE
                # axis-angle: 180 degrees about (0, 1, -1). The current SCPF
                # rotate() sets, rather than composes, an orientation; a
                # second rotate(axis=Y) would discard the upright X rotation.
                occurrence = occurrence.rotate(axis=(0, 1, -1), degrees=180)
            # Apply placement last to avoid rotating the column offset.
            occurrence = occurrence.move(x=x)
            screen = screen + occurrence

        return screen


BasicHub75Screen()
