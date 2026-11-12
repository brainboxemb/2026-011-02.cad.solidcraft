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
SCPF creates all native copies before asking SolidCraft to place them.
Rotations and positions are applied with SolidCraft's native commands, not
custom matrix arithmetic.
"""
from models.components.hub75_panel.detailed.scpf.model import Hub75Panel

# This model represents one fixed five-panel 160 x 320 mm nominal grid.
# These dimensions define the product layout; they are not editable native
# SolidCraft parameters. The physical panel envelope remains in models/components/hub75_panel/detailed/scpf/model.py.
NOMINAL_PITCH_X = 160.0
NOMINAL_HEIGHT = 320.0


class BasicHub75Screen:
    def build(self):
        # The native panel has its display face in XY and its rear in +Z.
        # Rotate to XZ so the 319.71 mm long side points upwards in world Z.
        # The master is X=0 and Z=160; all native copies start unplaced.
        # SolidCraft applies each occurrence's intended pose once.
        central = Hub75Panel().rotate(
            axis=(1, 0, 0),
            degrees=90,
        ).move(z=NOMINAL_HEIGHT / 2)
        screen = central

        for index in (0, 1, 3, 4):
            x = (index - 2) * NOMINAL_PITCH_X
            occurrence = central.copy()
            if index in (1, 3):
                # Compose the upright X+90 and world Y+180 rotations as ONE
                # axis-angle: 180 degrees about (0, 1, -1). The current SCPF
                # rotate() sets, rather than composes, an orientation; a
                # second rotate(axis=Y) would discard the upright X rotation.
                occurrence = occurrence.rotate(axis=(0, 1, -1), degrees=180)
            # This sets a Python-side position; the native move is emitted
            # after ALL copies are created (SolidCraft 0.30.1).
            occurrence = occurrence.move(x=x)
            screen = screen + occurrence

        return screen
