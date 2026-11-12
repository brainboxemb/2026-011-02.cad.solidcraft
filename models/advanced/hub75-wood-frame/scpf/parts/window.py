"""Plexiglass window part."""

from scpf import Box


class Window:
    width = 840.0
    height = 360.0
    thickness = 4.0

    def build(self):
        return Box(
            self.width,
            self.thickness,
            self.height,
        ).with_material(
            "Plexiglass",
            density_g_cm3=1.19,
            color="#B7DAEF",
        )
