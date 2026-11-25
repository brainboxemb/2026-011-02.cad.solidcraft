"""SolidCraft default Sheet Metal Bracket reproduced with native Forge sheet metal.

The feature order, edge picks and sheet-rule values mirror the supplied
SolidCraft default model. This is intentionally native sheet-metal history,
not a solid-envelope approximation.
"""


class SheetMetalBracket:
    width = 120.0
    depth = 60.0

    thickness = 2.0
    k_factor = 0.44
    bend_radius = 2.0

    long_flange_height = 30.0
    long_flange_angle = 90.0

    end_flange_height = 20.0
    end_flange_angle = 60.0

    hem_length = 8.0

    def build(self):
        # Native source sketch Base: p1=(0,0), p2=(120,0),
        # p3=(120,60), p4=(0,60).
        with Sketch(name="Base", plane="XY") as blank:
            Polygon2D(
                [
                    ("v1", (0.0, 0.0)),
                    ("v2", (self.width, 0.0)),
                    ("v3", (self.width, self.depth)),
                    ("v4", (0.0, self.depth)),
                ],
                plane="XY",
            )

        sheet = blank.sheet_metal(
            thickness=self.thickness,
            bend_radius=self.bend_radius,
            k_factor=self.k_factor,
            rule_name="Steel 2mm",
        )

        # SolidCraft default EdgeFlange1:
        # F2:side:l1|F2:top and F2:side:l3|F2:top.
        sheet = sheet.flange(
            edges=[
                (60.0, 0.0, 2.0),
                (60.0, 60.0, 2.0),
            ],
            height=self.long_flange_height,
            angle=self.long_flange_angle,
            position="inside",
        )

        # SolidCraft default EdgeFlange2:
        # F2:side:l2|F2:top.
        sheet = sheet.flange(
            edges=[(120.0, 30.0, 2.0)],
            height=self.end_flange_height,
            angle=self.end_flange_angle,
            position="inside",
        )

        # SolidCraft default Hem1:
        # F2:side:l4|F2:top. Deliberately omit gap= so the active
        # sheet rule owns the default hem clearance (0.01 mm in the source).
        sheet = sheet.hem(
            edges=[(0.0, 30.0, 2.0)],
            length=self.hem_length,
        )

        return sheet


SheetMetalBracket()
