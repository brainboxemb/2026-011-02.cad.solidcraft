"""Rear plywood panel fitted between the side walls."""

from scpf import BOTTOM, FRONT, Box, RoundedRectangle2D, Sketch, component, half


@component
class RearBoard:
    """9 mm rear board with closed rounded hand openings near both sides."""

    width = 844.0
    depth = 9.0
    height = 444.0

    opening_width = 30.0
    opening_edge_clearance = 20.0
    opening_radius = 10.0
    opening_bottom = 162.0
    opening_top = 364.0

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

        # Mirror the side-wall hand-hole idea on the rear panel. Each 30 mm
        # opening keeps 20 mm of plywood to the nearest side edge.
        opening_center_x = (
            half(self.width)
            - self.opening_edge_clearance
            - half(self.opening_width)
        )
        opening_center_z = (
            self.opening_bottom
            + half(opening_height)
        )

        with Sketch(
            name="Rear hand openings",
            on=body,
            plane="XZ",
        ) as opening_sketch:
            left = RoundedRectangle2D(
                self.opening_width,
                opening_height,
                self.opening_radius,
            )
            opening_sketch.add(
                left,
                offset=(-opening_center_x, opening_center_z),
            )

            right = RoundedRectangle2D(
                self.opening_width,
                opening_height,
                self.opening_radius,
            )
            opening_sketch.add(
                right,
                offset=(opening_center_x, opening_center_z),
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
