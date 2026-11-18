"""Vertical beech roundwood used as the side carry handle."""

from scpf import BOTTOM, Cylinder, component


@component
class RoundwoodHandle:
    """Straight Ø22 roundwood; the handle itself is deliberately not slotted."""

    diameter = 22.0
    length = 150.0

    def build(self):
        return Cylinder(
            d=self.diameter,
            h=self.length,
            anchor=BOTTOM,
        ).with_material(
            "Beech roundwood",
            density_g_cm3=0.72,
            color="#A87545",
        )
