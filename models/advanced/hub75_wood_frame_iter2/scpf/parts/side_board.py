"""Side wall with one closed native hand slot."""

from scpf import (
    BOTTOM,
    FRONT,
    Box,
    Sketch,
    SlotCenterToCenter2D,
    component,
)


@component
class SideBoard:
    """Full-depth side wall with one vertical 30 mm native slot."""

    thickness = 12.0
    depth = 120.0
    height = 444.0

    opening_width = 30.0
    opening_edge_clearance = 20.0
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

        # Keep 20 mm of plywood between the slot and the 120 mm rear edge.
        # For a 30 mm wide slot the centreline is Y=85, so the slot spans
        # Y=70..100 and its round ends are R15 by definition.
        opening_center_y = (
            self.depth
            - self.opening_edge_clearance
            - self.opening_width / 2
        )

        # SlotCenterToCenter2D uses the centres of the two round ends. Move
        # those centres 15 mm inward from the requested overall top/bottom so
        # the complete slot still spans opening_bottom..opening_top.
        end_radius = self.opening_width / 2
        lower_center_z = self.opening_bottom + end_radius
        upper_center_z = self.opening_top - end_radius

        with Sketch(
            name="Side hand slot",
            on=body,
            plane="YZ",
        ) as opening_sketch:
            profile = SlotCenterToCenter2D(
                (opening_center_y, lower_center_z),
                (opening_center_y, upper_center_z),
                self.opening_width,
            )
            opening_sketch.add(profile)

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
