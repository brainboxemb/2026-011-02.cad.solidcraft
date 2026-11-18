"""Shaped side wall for the second wooden HUB75 frame iteration."""

from scpf import (
    BOTTOM,
    FRONT,
    Box,
    RoundedRectangle2D,
    Sketch,
    component,
)


@component
class SideBoard:
    """Full-depth side wall with one rounded rear recess in the display zone."""

    thickness = 12.0
    depth = 100.0
    height = 444.0

    # Rear-profile inputs.
    recess_depth = 50.0
    recess_radius = 20.0
    recess_bottom = 162.0
    recess_top = 364.0

    # Build-only material details.
    material_name = None
    color = None

    def build(self):
        # Start with the complete side wall. X is plywood thickness, Y is
        # cabinet depth from the front face and Z is vertical height.
        body = Box(
            self.thickness,
            self.depth,
            self.height,
        ).at(
            0,
            0,
            0,
            anchor=FRONT + BOTTOM,
        )

        # The recess is cut from the rear. Its rounded rectangle extends one
        # radius beyond the physical rear face, so the visible result is the
        # same side-profile principle as the V1.1 reference: full depth at both
        # ends, a reduced-depth middle zone and R20 transitions.
        recess_height = self.recess_top - self.recess_bottom
        cut_depth = self.recess_depth + self.recess_radius
        cut_center_y = (
            self.depth
            - self.recess_depth
            + cut_depth / 2
        )
        cut_center_z = (
            self.recess_bottom
            + recess_height / 2
        )

        with Sketch(name="Rear recess", plane="YZ") as recess_sketch:
            profile = RoundedRectangle2D(
                cut_depth,
                recess_height,
                self.recess_radius,
            )
            recess_sketch.add(
                profile,
                offset=(cut_center_y, cut_center_z),
            )

        # Extrude slightly past both plywood faces so the subtraction is robust
        # even when the side-board thickness is changed later.
        recess = recess_sketch.extrude(
            self.thickness + 2,
            sym=True,
        )
        body = body - recess

        return body.with_material(
            self.material_name or "LIGHTPLY side board",
            density_g_cm3=0.55,
            color=self.color or "#CBA36B",
        )
