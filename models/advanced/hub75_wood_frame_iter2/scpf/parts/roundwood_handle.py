"""Vertical beech roundwood used as the side carry handle."""

from scpf import BOTTOM, Box, Cylinder, component, half


# Extend boolean cutters slightly beyond the physical rod ends. This avoids
# coplanar end faces, which are fragile in CAD boolean operations.
NOTCH_BOOLEAN_MARGIN = 0.1


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

        # The component is authored for the right-hand side. The side wall is
        # on local -X, so remove X=-11..0 from both 15 mm end extensions.
        # This leaves the outside half-cylinder (X=0..+11) intact.
        cut_x = -half(self.notch_depth)

        # Cut completely through Y and slightly beyond both rod end faces.
        # Using simple Box cutters is deliberate: the notch is rectangular and
        # does not need a sketch, and the overlap makes the boolean robust.
        cut_depth_y = self.diameter + 2.0
        cut_height_z = self.notch_height + 2 * NOTCH_BOOLEAN_MARGIN

        bottom_cut = Box(
            self.notch_depth,
            cut_depth_y,
            cut_height_z,
        ).at(
            cut_x,
            0,
            -NOTCH_BOOLEAN_MARGIN,
            anchor=BOTTOM,
        )

        top_cut = Box(
            self.notch_depth,
            cut_depth_y,
            cut_height_z,
        ).at(
            cut_x,
            0,
            self.length - self.notch_height - NOTCH_BOOLEAN_MARGIN,
            anchor=BOTTOM,
        )

        body = body - bottom_cut - top_cut

        return body.with_material(
            "Beech roundwood",
            density_g_cm3=0.72,
            color="#A87545",
        )
