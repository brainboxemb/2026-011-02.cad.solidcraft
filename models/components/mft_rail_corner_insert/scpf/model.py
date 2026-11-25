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
            profile.line_to((-1.6970562748477138, 0.0))
            profile.line_to((-10.182337649086284, -8.485281374238571))
            profile.arc_center_to(
                (-8.485281374238571, -10.182337649086284),
                center=(-9.33380951166243, -9.33380951166243),
                clockwise=True,
            )
            profile.line_to((0.0, -1.6970562748477138))
            profile.line_to((0.0, -18.0))
            profile.arc_center_to(
                (-18.0, 0.0),
                center=(0.0, 0.0),
                clockwise=True,
            )
            profile.close()

        insert = outline.extrude(26.6)

        # Native feature 40/41:
        # two clip lips in the XY plane at Z=-21.35, each with an 0.8 mm
        # diagonal lead-in before the 2 mm retaining face.
        with Sketch(
            name="PETG-klemlip Y",
            plane="XY",
            origin=(0.0, 0.0, -21.35),
        ) as y_lip_sketch:
            y_lip = y_lip_sketch.profile(start=(-1.0, -16.5))
            y_lip.line_to((2.7, -16.5))
            y_lip.line_to((3.5, -15.7))
            y_lip.line_to((3.5, -13.7))
            y_lip.line_to((-1.0, -13.7))
            y_lip.line_to((-1.0, -16.5))
            y_lip.close()
        insert = insert + y_lip_sketch.extrude(15.7)

        with Sketch(
            name="PETG-klemlip X",
            plane="XY",
            origin=(0.0, 0.0, -21.35),
        ) as x_lip_sketch:
            x_lip = x_lip_sketch.profile(start=(-13.7, -1.0))
            x_lip.line_to((-13.7, 3.5))
            x_lip.line_to((-15.7, 3.5))
            x_lip.line_to((-16.5, 2.7))
            x_lip.line_to((-16.5, -1.0))
            x_lip.line_to((-13.7, -1.0))
            x_lip.close()
        insert = insert + x_lip_sketch.extrude(15.7)

        return insert.with_material(
            "PETG prototype",
            density_g_cm3=1.27,
            color="#50555C",
        )


MFTRailCornerInsert()
