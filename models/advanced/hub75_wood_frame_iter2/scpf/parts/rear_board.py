"""Rear plywood panel fitted between the side walls."""

from scpf import (
    BOTTOM,
    FRONT,
    Box,
    RoundedRectangle2D,
    Sketch,
    component,
    half,
)


@component
class RearBoard:
    """9 mm rear board with matching left/right handle openings."""

    width = 844.0
    depth = 9.0
    height = 444.0

    # Match the vertical handle opening in the side-wall profile.
    recess_depth = 50.0
    recess_radius = 20.0
    recess_bottom = 162.0
    recess_top = 364.0

    def build(self):
        body = Box(
            self.width,
            self.depth,
            self.height,
        ).at(
            0,
            0,
            0,
            anchor=FRONT + BOTTOM,
        )

        # Use the same R20 transition principle as the side panels. Each
        # rounded cut starts 50 mm in from the rear-board side edge and extends
        # one radius beyond that edge so the opening remains fully open.
        recess_height = self.recess_top - self.recess_bottom
        cut_width = self.recess_depth + self.recess_radius
        cut_center_x = (
            half(self.width)
            - self.recess_depth
            + half(cut_width)
        )
        cut_center_z = (
            self.recess_bottom
            + half(recess_height)
        )

        with Sketch(
            name="Rear handle openings",
            on=body,
            plane="XZ",
        ) as recess_sketch:
            left = RoundedRectangle2D(
                cut_width,
                recess_height,
                self.recess_radius,
            )
            recess_sketch.add(
                left,
                offset=(-cut_center_x, cut_center_z),
            )

            right = RoundedRectangle2D(
                cut_width,
                recess_height,
                self.recess_radius,
            )
            recess_sketch.add(
                right,
                offset=(cut_center_x, cut_center_z),
            )

        # Cut slightly beyond both 9 mm panel faces so no coplanar face is left
        # behind by the boolean operation.
        openings = recess_sketch.extrude(
            self.depth + 2,
            sym=True,
        )
        body = body - openings

        return body.with_material(
            "LIGHTPLY rear",
            density_g_cm3=0.55,
            color="#A87D4D",
        )
