"""Reusable loose Ø10 tube clamp reconstructed from native SolidCraft features."""

from math import sqrt

from scpf import Sketch, component


# Active SolidCraft configuration: "Vrij – printstand".
TUBE_DIAMETER = 10.0
CLAMP_INTERFERENCE = 0.4
CLAMP_BORE = TUBE_DIAMETER - CLAMP_INTERFERENCE
CLAMP_WALL = 2.0
CLAMP_WIDTH = 12.0

SLIDE_RUN = 16.0
SLOT_STOP = 1.0

# Active source feature: "Open klemring met afgeronde lippen".
RING_INNER_RADIUS = CLAMP_BORE / 2.0
RING_OUTER_RADIUS = RING_INNER_RADIUS + CLAMP_WALL
RING_OPENING_HALF_ANGLE = 45.0
RING_LIP_RADIUS = 1.0

# Active source feature: "Afgeronde rug voor de schuifgleuf".
BACK_X_MIN = -8.85
BACK_X_MAX = -5.65
BACK_HALF_HEIGHT = CLAMP_WIDTH / 2.0
BACK_CORNER_RADIUS = 0.30

# Active source feature: "Schuifgleuf met aanloop en printflanken".
#
# These positions are retained from the native SolidCraft sketch. They are
# sketch control dimensions, not measurements reverse-engineered from STEP.
SLOT_OUTER_X = -9.05
SLOT_ENTRY_X = -8.90
SLOT_ENTRY_HALF_HEIGHT = 2.75
SLOT_ENTRY_TANGENT_HALF_HEIGHT = 2.90
SLOT_ENTRY_FILLET_CENTER_X = -8.412132034355963
SLOT_ENTRY_FLANK_X = -8.306066017177981
SLOT_ENTRY_FLANK_Z = 2.943933982822018
SLOT_INNER_FLANK_X = -7.643933982822017
SLOT_INNER_FLANK_Z = 3.606066017177982
SLOT_INNER_FILLET_CENTER_X = -7.537867965644035
SLOT_NECK_X = -7.25
SLOT_OPEN_X = -7.10
SLOT_NECK_HALF_HEIGHT = 3.50
SLOT_OUTER_HALF_HEIGHT = 3.65
SLOT_FILLET_RADIUS = 0.15


def _ring_sketch():
    """Build the active open elastic clamp-ring profile directly."""
    outer_q = RING_OUTER_RADIUS / sqrt(2.0)
    inner_q = RING_INNER_RADIUS / sqrt(2.0)
    lip_center_q = (outer_q + inner_q) / 2.0

    with Sketch(
        name="Open klemring met afgeronde lippen",
        plane="XY",
        offset=-CLAMP_WIDTH / 2.0,
    ) as sketch:
        profile = sketch.profile(start=(outer_q, outer_q))
        profile.arc_center_to(
            (outer_q, -outer_q),
            center=(0.0, 0.0),
            clockwise=False,
        )
        profile.arc_center_to(
            (inner_q, -inner_q),
            center=(lip_center_q, -lip_center_q),
            clockwise=False,
        )
        profile.arc_center_to(
            (inner_q, inner_q),
            center=(0.0, 0.0),
            clockwise=True,
        )
        profile.arc_center_to(
            (outer_q, outer_q),
            center=(lip_center_q, lip_center_q),
            clockwise=False,
        )
        profile.close()

    return sketch


def _slide_back_sketch():
    """Build the active low integrated rounded slide back directly."""
    r = BACK_CORNER_RADIUS
    z = BACK_HALF_HEIGHT

    with Sketch(
        name="Afgeronde rug voor de schuifgleuf",
        plane="XZ",
        offset=-SLIDE_RUN / 2.0,
    ) as sketch:
        profile = sketch.profile(start=(BACK_X_MIN, -z + r))
        profile.arc_center_to(
            (BACK_X_MIN + r, -z),
            center=(BACK_X_MIN + r, -z + r),
            clockwise=False,
        )
        profile.line_to((BACK_X_MAX - r, -z))
        profile.arc_center_to(
            (BACK_X_MAX, -z + r),
            center=(BACK_X_MAX - r, -z + r),
            clockwise=False,
        )
        profile.line_to((BACK_X_MAX, z - r))
        profile.arc_center_to(
            (BACK_X_MAX - r, z),
            center=(BACK_X_MAX - r, z - r),
            clockwise=False,
        )
        profile.line_to((BACK_X_MIN + r, z))
        profile.arc_center_to(
            (BACK_X_MIN, z - r),
            center=(BACK_X_MIN + r, z - r),
            clockwise=False,
        )
        profile.close()

    return sketch


def _slide_slot_sketch():
    """Build the active rounded slide slot with print flanks directly."""
    r = SLOT_FILLET_RADIUS

    with Sketch(
        name="Schuifgleuf met aanloop en printflanken",
        plane="XZ",
        offset=-SLIDE_RUN / 2.0 - 0.05,
    ) as sketch:
        profile = sketch.profile(
            start=(SLOT_OUTER_X, -SLOT_ENTRY_HALF_HEIGHT)
        )

        # Lower half: rounded entry -> 45-degree print flank -> rounded neck.
        profile.arc_center_to(
            (SLOT_ENTRY_X, -SLOT_ENTRY_TANGENT_HALF_HEIGHT),
            center=(SLOT_ENTRY_X, -SLOT_ENTRY_HALF_HEIGHT),
            clockwise=False,
        )
        profile.line_to(
            (SLOT_ENTRY_FILLET_CENTER_X, -SLOT_ENTRY_TANGENT_HALF_HEIGHT)
        )
        profile.arc_center_to(
            (SLOT_ENTRY_FLANK_X, -SLOT_ENTRY_FLANK_Z),
            center=(
                SLOT_ENTRY_FILLET_CENTER_X,
                -SLOT_ENTRY_TANGENT_HALF_HEIGHT - r,
            ),
            clockwise=True,
        )
        profile.line_to((SLOT_INNER_FLANK_X, -SLOT_INNER_FLANK_Z))
        profile.arc_center_to(
            (SLOT_INNER_FILLET_CENTER_X, -SLOT_OUTER_HALF_HEIGHT),
            center=(
                SLOT_INNER_FILLET_CENTER_X,
                -SLOT_NECK_HALF_HEIGHT,
            ),
            clockwise=False,
        )
        profile.line_to((SLOT_NECK_X, -SLOT_OUTER_HALF_HEIGHT))
        profile.arc_center_to(
            (SLOT_OPEN_X, -SLOT_NECK_HALF_HEIGHT),
            center=(SLOT_NECK_X, -SLOT_NECK_HALF_HEIGHT),
            clockwise=False,
        )

        # Open-side wall and mirrored upper half.
        profile.line_to((SLOT_OPEN_X, SLOT_NECK_HALF_HEIGHT))
        profile.arc_center_to(
            (SLOT_NECK_X, SLOT_OUTER_HALF_HEIGHT),
            center=(SLOT_NECK_X, SLOT_NECK_HALF_HEIGHT),
            clockwise=False,
        )
        profile.line_to((SLOT_INNER_FILLET_CENTER_X, SLOT_OUTER_HALF_HEIGHT))
        profile.arc_center_to(
            (SLOT_INNER_FLANK_X, SLOT_INNER_FLANK_Z),
            center=(
                SLOT_INNER_FILLET_CENTER_X,
                SLOT_NECK_HALF_HEIGHT,
            ),
            clockwise=False,
        )
        profile.line_to((SLOT_ENTRY_FLANK_X, SLOT_ENTRY_FLANK_Z))
        profile.arc_center_to(
            (SLOT_ENTRY_FILLET_CENTER_X, SLOT_ENTRY_TANGENT_HALF_HEIGHT),
            center=(
                SLOT_ENTRY_FILLET_CENTER_X,
                SLOT_ENTRY_TANGENT_HALF_HEIGHT + r,
            ),
            clockwise=True,
        )
        profile.line_to(
            (SLOT_ENTRY_X, SLOT_ENTRY_TANGENT_HALF_HEIGHT)
        )
        profile.arc_center_to(
            (SLOT_OUTER_X, SLOT_ENTRY_HALF_HEIGHT),
            center=(SLOT_ENTRY_X, SLOT_ENTRY_HALF_HEIGHT),
            clockwise=False,
        )
        profile.close()

    return sketch


@component
class Hub75TubeClamp10mm:
    """Free/print-state loose clamp used by Edge and Corner tube interfaces."""

    def build(self):
        # Source features 1/2: open elastic clamp ring in the native XY frame.
        ring_sketch = _ring_sketch()
        body = ring_sketch.extrude(CLAMP_WIDTH)

        # Source features 12/13: low integrated rounded back for the slide slot.
        back_sketch = _slide_back_sketch()
        body = body + back_sketch.extrude(SLIDE_RUN)

        # Source features 14/15: rounded slide slot with the 1 mm closed stop.
        slot_sketch = _slide_slot_sketch()
        body = body - slot_sketch.extrude(
            SLIDE_RUN - SLOT_STOP + 0.05
        )

        # Parent production amendment, feature 199:
        # "Inloop in groef van Ø10 proefklem".
        body = body.chamfer(
            0.14,
            edges=[
                (-7.975, -8.0, 3.275),
                (-7.1, -8.0, 0.0),
                (-7.975, -8.0, -3.275),
            ],
        )

        return body


Hub75TubeClamp10mm()
