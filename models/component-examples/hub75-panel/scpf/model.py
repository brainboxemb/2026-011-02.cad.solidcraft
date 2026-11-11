"""One reusable HUB75 mechanical component, shown upright in world XZ.

A single panel is a component. A screen assembly is responsible for copies.
The detailed panel definition stays native XY with rear depth in +Z; its
occurrence stands upright with +90 degrees about X, front facing world +Y.
"""
from scpf import component
from components.hub75 import Hub75Panel as Hub75PanelDefinition

Hub75Panel = component(Hub75PanelDefinition)


class SingleHub75Panel:
    def build(self):
        # Native panel height is centred around Y=0; rotate that height into
        # vertical world Z, then centre it in the 320 mm nominal display grid.
        return Hub75Panel().rotate(axis=(1, 0, 0), degrees=90).move(z=160)


SingleHub75Panel()
