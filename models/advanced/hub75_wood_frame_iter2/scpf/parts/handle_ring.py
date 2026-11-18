"""Simple plastic ring around the end of a vertical roundwood handle."""

from scpf import BOTTOM, Cylinder, component


@component
class HandleRing:
    """Ten millimetre high protective ring around Ø22 roundwood."""

    rod_diameter = 22.0
    radial_thickness = 3.0
    height = 10.0
    bore_clearance = 0.4

    def build(self):
        outer_diameter = (
            self.rod_diameter
            + 2 * self.radial_thickness
        )

        outer = Cylinder(
            d=outer_diameter,
            h=self.height,
            anchor=BOTTOM,
        )

        # Give the wooden rod a small assembly clearance. The bore extends
        # slightly beyond both ring faces so the subtraction has no coplanar
        # end faces.
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

        return (outer - bore).with_material(
            "PETG handle ring",
            density_g_cm3=1.27,
            color="#4F8A5B",
        )
