"""Vertical beech roundwood used as the side carry handle."""

from scpf import (
    BOTTOM,
    Cylinder,
    Rectangle2D,
    Sketch,
    component,
    half,
)


@component
class RoundwoodHandle:
    """Ø22 roundwood with 15 mm half-depth notches at both ends."""

    diameter = 22.0
    length = 180.0
    notch_depth = 11.0
    notch_height = 15.0

    def build(self):
        body = Cylinder(
            d=self.diameter,
            h=self.length,
            anchor=BOTTOM,
        )

        # The left-side handle is the reference orientation. At both extended
        # ends remove the half of the rod that faces the plywood side wall.
        # The 11 mm notch depth is exactly half of the Ø22 rod, so the outside
        # half-cylinder remains intact over the 15 mm end extension.
        notch_x = -half(self.notch_depth)
        bottom_notch_z = half(self.notch_height)
        top_notch_z = self.length - half(self.notch_height)

        with Sketch(
            name="Handle end notches",
            on=body,
            plane="XZ",
        ) as notch_sketch:
            lower = Rectangle2D(
                self.notch_depth,
                self.notch_height,
            )
            notch_sketch.add(
                lower,
                offset=(notch_x, bottom_notch_z),
            )

            upper = Rectangle2D(
                self.notch_depth,
                self.notch_height,
            )
            notch_sketch.add(
                upper,
                offset=(notch_x, top_notch_z),
            )

        # Cut through the full Y thickness of the roundwood. The right handle
        # reuses this same component rotated 180 degrees around Z, which puts
        # the notches on its own side-wall-facing half.
        notches = notch_sketch.extrude(
            self.diameter + 2,
            sym=True,
        )
        body = body - notches

        return body.with_material(
            "Beech roundwood",
            density_g_cm3=0.72,
            color="#A87545",
        )
