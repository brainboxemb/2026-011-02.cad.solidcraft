"""Concept socket connecting a vertical roundwood handle to a side wall."""

from scpf import BOTTOM, FRONT, Box, Cylinder, component


@component
class SideHandleSocket:
    """Printed sleeve with a short bridge to the recessed rear edge."""

    panel_thickness = 12.0
    rod_diameter = 22.0
    outer_diameter = 34.0
    height = 24.0
    bridge_depth = 8.0
    bore_clearance = 0.6

    def build(self):
        outer_radius = self.outer_diameter / 2

        # The bridge starts at the recessed plywood edge and ends tangent to
        # the sleeve. The socket centre is the local Y=0 datum.
        bridge = Box(
            self.panel_thickness,
            self.bridge_depth,
            self.height,
        ).at(
            0,
            -(outer_radius + self.bridge_depth),
            0,
            anchor=FRONT + BOTTOM,
        )

        sleeve = Cylinder(
            d=self.outer_diameter,
            h=self.height,
            anchor=BOTTOM,
        )
        body = bridge + sleeve

        # Keep the wooden handle intact. The clearance bore belongs to the
        # printed socket, not to the Ø22 roundwood.
        bore = Cylinder(
            d=self.rod_diameter + self.bore_clearance,
            h=self.height + 0.2,
            anchor=BOTTOM,
        ).at(
            0,
            0,
            -0.1,
            anchor=BOTTOM,
        )
        body = body - bore

        return body.with_material(
            "PETG handle socket",
            density_g_cm3=1.27,
            color="#4F8A5B",
        )
