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
    """9 mm rear board with open rounded cutouts at both side edges."""

    width = 844.0
    depth = 9.0
    height = 374.0

    opening_depth = 50.0
    opening_radius = 20.0
    opening_bottom = 92.0
    opening_top = 294.0

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

        opening_height = self.opening_top - self.opening_bottom

        # Restore the original open side cutout. The rounded rectangle extends
        # one radius beyond the physical panel edge, leaving a 50 mm deep open
        # recess from each side with R20 transitions.
        cut_width = self.opening_depth + self.opening_radius
        cut_center_x = (
            half(self.width)
            - self.opening_depth
            + half(cut_width)
        )
        cut_center_z = (
            self.opening_bottom
            + half(opening_height)
        )

        with Sketch(
            name="Rear side openings",
            on=body,
            plane="XZ",
        ) as opening_sketch:
            left = RoundedRectangle2D(
                cut_width,
                opening_height,
                self.opening_radius,
            )
            opening_sketch.add(
                left,
                offset=(-cut_center_x, cut_center_z),
            )

            right = RoundedRectangle2D(
                cut_width,
                opening_height,
                self.opening_radius,
            )
            opening_sketch.add(
                right,
                offset=(cut_center_x, cut_center_z),
            )

        openings = opening_sketch.extrude(
            self.depth + 2,
            sym=True,
        )
        body = body - openings

        return body.with_material(
            "LIGHTPLY rear",
            density_g_cm3=0.55,
            color="#A87D4D",
        )
