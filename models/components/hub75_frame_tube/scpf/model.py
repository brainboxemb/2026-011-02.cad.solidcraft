"""Reusable Ø10 × 1 mm aluminum tube for HUB75 display frames.

The retained native frame source owns separate top/bottom tube components, but
both use the same hollow Ø10/Ø8 profile and length.  This catalog owner keeps
one physical component and leaves top/bottom placement to the assembly.
"""

from scpf import Circle2D, Sketch, component


@component(include=("length",))
class Hub75FrameTube10mm:
    """Hollow aluminum tube with editable length."""

    length = 360.0

    OUTER_DIAMETER = 10.0
    WALL = 1.0
    INNER_DIAMETER = OUTER_DIAMETER - 2 * WALL

    def build(self):
        # Forge v0.19 standalone Sketch authoring accepts one closed profile per
        # Sketch. Keep both boundaries native/editable as two sketch features:
        # outer extrusion followed by the concentric bore cut.
        with Sketch(name="Tube outer profile", plane="YZ") as outer_profile:
            Circle2D(d=self.OUTER_DIAMETER)
        tube = outer_profile.extrude(self.length, sym=True)

        with Sketch(name="Tube bore profile", plane="YZ") as bore_profile:
            Circle2D(d=self.INNER_DIAMETER)
        bore = bore_profile.extrude(self.length + 2.0, sym=True)
        tube = tube - bore

        return tube.with_material(
            "Aluminium",
            density_g_cm3=2.70,
            color="#C4C8CB",
        )


Hub75FrameTube10mm()
