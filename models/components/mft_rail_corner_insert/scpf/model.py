"""Loose PETG corner insert from the supplied hoek_assembly source.

The native SolidCraft source keeps this as a separate body named
`PETG-hoekinzetstuk`.  In the catalog it is promoted to its own reusable
component because it is a distinct printable/replaceable physical part.

Coordinate contract matches the MFT rail corner subassembly:
- bracket inside corner is X=0 / Y=0;
- the insert occupies the outside -X/-Y quarter;
- Z=0 is the future MFT underside.
"""

from scpf import Sketch, component


@component(include="*")
class MFTRailCornerInsert:
    """Rounded outer-corner filler with two integral clip lips."""

    def build(self):
        # Native feature 38/39:
        # "Omtrek PETG-hoekkap" -> "Afgeronde PETG-hoekkap met inkeping".
        with Sketch(
            name="Omtrek PETG-hoekkap",
            plane="XY",
            origin=(0.0, 0.0, -26.8),
        ) as outline:
            profile = outline.profile(start=(-18.0, 0.0))
            profile.line_to((-4.525483399593905, 0.0))
            profile.line_to((-3.1112698372208096, -1.4142135623730951))
            profile.line_to((-10.182337649086284, -8.485281374238571))
            profile.arc_center_to(
                (-8.485281374238571, -10.182337649086284),
                center=(-9.33380951166243, -9.33380951166243),
                clockwise=True,
            )
            profile.line_to((-1.4142135623730951, -3.1112698372208096))
            profile.line_to((0.0, -4.525483399593905))
            profile.line_to((0.0, -18.0))
            profile.arc_center_to(
                (-18.0, 0.0),
                center=(0.0, 0.0),
                clockwise=True,
            )
            profile.close()

        insert = outline.extrude(26.6)

        # Native v2 feature 40/41: enlarged clip lips start at Z=-22.25 and
        # extend 17.5 mm upward. The lead-ins and rail-side reach are wider than
        # the first supplied corner source.
        with Sketch(
            name="PETG-klemlip Y",
            plane="XY",
            origin=(0.0, 0.0, -22.25),
        ) as y_lip_sketch:
            y_lip = y_lip_sketch.profile(start=(-1.0, -16.5))
            y_lip.line_to((4.5, -16.5))
            y_lip.line_to((5.5, -15.5))
            y_lip.line_to((5.5, -13.3))
            y_lip.line_to((-1.0, -13.3))
            y_lip.line_to((-1.0, -16.5))
            y_lip.close()
        insert = insert + y_lip_sketch.extrude(17.5)

        with Sketch(
            name="PETG-klemlip X",
            plane="XY",
            origin=(0.0, 0.0, -22.25),
        ) as x_lip_sketch:
            x_lip = x_lip_sketch.profile(start=(-13.3, -1.0))
            x_lip.line_to((-13.3, 5.5))
            x_lip.line_to((-15.5, 5.5))
            x_lip.line_to((-16.5, 4.5))
            x_lip.line_to((-16.5, -1.0))
            x_lip.line_to((-13.3, -1.0))
            x_lip.close()
        insert = insert + x_lip_sketch.extrude(17.5)

        # Native v2 feature 42/43: two additional upright click lugs enter the
        # rail C-profiles. They are independent from the lower retaining lips.
        with Sketch(
            name="Opstaande nokken in C-profielen",
            plane="XY",
            origin=(0.0, 0.0, -19.5),
        ) as lug_y_sketch:
            lug_y = lug_y_sketch.profile(start=(0.5, -16.0))
            lug_y.line_to((0.5, -18.25))
            lug_y.line_to((3.3, -18.25))
            lug_y.line_to((4.5, -16.5))
            lug_y.line_to((4.5, -16.0))
            lug_y.close()
        insert = insert + lug_y_sketch.extrude(12.0)

        with Sketch(
            name="Opstaande nok X in C-profiel",
            plane="XY",
            origin=(0.0, 0.0, -19.5),
        ) as lug_x_sketch:
            lug_x = lug_x_sketch.profile(start=(-16.0, 4.5))
            lug_x.line_to((-16.5, 4.5))
            lug_x.line_to((-18.25, 3.3))
            lug_x.line_to((-18.25, 0.5))
            lug_x.line_to((-16.0, 0.5))
            lug_x.close()
        insert = insert + lug_x_sketch.extrude(12.0)

        # Native v2 feature 44: R0.8 fillets on the two inner lip-root edges.
        insert = insert.fillet(
            0.8,
            edges=[
                (0.0, -13.3, -13.49999),
                (-13.3, 0.0, -13.49999),
            ],
        )

        return insert.with_material(
            "PETG prototype",
            density_g_cm3=1.27,
            color="#30343B",
        )


MFTRailCornerInsert()
