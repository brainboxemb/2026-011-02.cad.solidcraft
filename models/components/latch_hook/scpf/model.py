"""Source-faithful native sheet-metal latch hook.

Authoritative references:
- ../reference/hook.sc
- ../reference/hook.json

The supplied SolidCraft source contains exactly three native features:
1. Uitslag haak (sketch)
2. Vlakke plaat 2 mm (sheet base)
3. Haak omvouwen (sheet fold)

This SCPF model mirrors those fixed source coordinates instead of re-deriving
or visually approximating the outline.
"""

from scpf import Hole, Sketch, component


# Exact source geometry from hook.json.
_BEND_ANGLE = 138.7667505744678
_THICKNESS = 2.0
_K_FACTOR = 0.44
_BEND_RADIUS = 2.1

_HOLE_DIAMETER = 4.3
_HOLE_X = 5.0
_HOLE_Y = 7.0

_LOBE_END_X = 7.209449193419511
_LOBE_END_Y = 11.485346615558026
_NECK_START_X = 15.3
_HALF_NECK = 7.5
_BLANK_END_X = 28.14928735268115
_FOLD_X = 15.9


@component(include="*")
class LatchHook:
    def build(self):
        with Sketch(name="Uitslag haak", plane="XY") as blank:
            contour = blank.profile(start=(0.0, 7.0))
            contour.line_to((0.0, -7.0))

            # Native lower R5 lobe.  The following straight segment is tangent
            # to this arc in the supplied source.
            contour.arc_center_to(
                (_LOBE_END_X, -_LOBE_END_Y),
                center=(5.0, -7.0),
                clockwise=False,
            )
            contour.line_to((_NECK_START_X, -_HALF_NECK))
            contour.line_to((_BLANK_END_X, -_HALF_NECK))
            contour.line_to((_BLANK_END_X, _HALF_NECK))
            contour.line_to((_NECK_START_X, _HALF_NECK))
            contour.line_to((_LOBE_END_X, _LOBE_END_Y))

            # Native upper R5 lobe, mirrored from the lower side.
            contour.arc_center_to(
                (0.0, 7.0),
                center=(5.0, 7.0),
                clockwise=False,
            )
            contour.close()

        hook = blank.sheet_metal(
            thickness=_THICKNESS,
            bend_radius=_BEND_RADIUS,
            k_factor=_K_FACTOR,
            rule_name="Haak 2 mm",
        )

        # The native source sketch contains the two Ø4.3 circles at
        # (5, -7) and (5, 7).  Forge expresses those as flat-sheet holes
        # before the fold.
        for y in (-_HOLE_Y, _HOLE_Y):
            hook = hook + Hole(
                d=_HOLE_DIAMETER,
                direction=(0, 0, -1),
            ).at(_HOLE_X, y, _THICKNESS)

        # Exact native fold contract from feature "Haak omvouwen":
        # x=15.9, angle 138.7667505744678°, position=start, stays=left.
        hook = hook.fold(
            line=((15.9, -7.5), (15.9, 7.5)),
            angle=_BEND_ANGLE,
            fixed=(5.0, 0.0, 0.0),
            position="start",
        )

        return hook.with_material(
            "Galvanized steel",
            density_g_cm3=7.85,
            color="#B7BDC2",
        )


LatchHook()
