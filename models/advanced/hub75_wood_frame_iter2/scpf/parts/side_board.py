"""Side wall with one closed rounded hand opening."""

from scpf import BOTTOM, FRONT, Box, RoundedRectangle2D, Sketch, component


@component
class SideBoard:
    """Full-depth side wall with a closed vertical hand opening."""

    thickness = 12.0
    depth = 120.0
    height = 444.0

    opening_width = 30.0
    opening_edge_clearance = 20.0
    opening_radius = 10.0
    opening_bottom = 162.0
    opening_top = 364.0

    material_name = None
    color = None

    def build(self):
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

        opening_height = self.opening_top - self.opening_bottom

        # Keep 20 mm of plywood between the opening and the 120 mm rear edge.
        # With a 30 mm opening this places the hole at Y=70..100.
        opening_center_y = (
            self.depth
            - self.opening_edge_clearance
            - self.opening_width / 2
        )
        opening_center_z = (
            self.opening_bottom
            + opening_height / 2
        )

        with Sketch(
            name="Side hand opening",
            on=body,
            plane="YZ",
        ) as opening_sketch:
            profile = RoundedRectangle2D(
                self.opening_width,
                opening_height,
                self.opening_radius,
            )
            opening_sketch.add(
                profile,
                offset=(opening_center_y, opening_center_z),
            )

        opening = opening_sketch.extrude(
            self.thickness + 2,
            sym=True,
        )
        body = body - opening

        return body.with_material(
            self.material_name or "LIGHTPLY side board",
            density_g_cm3=0.55,
            color=self.color or "#CBA36B",
        )
