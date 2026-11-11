"""Basic five-panel array copied from the OpenSCAD v1.2 placement rules.

SCPF coordinates: X horizontal, Y panel vertical, Z front-to-rear.
The OpenSCAD 180-degree Y rotation maps to a 180-degree Z rotation.
From rear left to right: chain numbers 5,4,3,2,1, input top/bottom
alternating TOP, BOTTOM, TOP, BOTTOM, TOP.
"""
from scpf import component
from components.hub75 import Hub75Panel as Hub75PanelDefinition

Hub75Panel = component(Hub75PanelDefinition)

class BasicHub75Screen:
    nominal_pitch_x = 160.0
    nominal_height = 320.0

    def build(self):
        # The first occurrence stays at world X=0 (middle column).
        # occurrence.copy inherits its source transform, so a first
        # occurrence at -320 mm would cause double-offset copies.
        central = Hub75Panel()
        screen = central
        for index in (0, 1, 3, 4):
            x = (index - 2) * self.nominal_pitch_x
            occurrence = central.copy().move(x=x)
            if index in (1, 3):
                occurrence = occurrence.rotate(axis=(0, 0, 1), degrees=180)
            screen = screen + occurrence
        return screen

BasicHub75Screen()
