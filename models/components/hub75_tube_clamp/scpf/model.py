"""Reusable loose Ø10 tube clamp rebuilt from the native SolidCraft feature history."""

from math import cos, radians, sin, tan

from scpf import Sketch, component


# Native SolidCraft parameters used by the active Free/print-state features.
TUBE_D = 10.0
CLAMP_INTERFERENCE = 0.4
CLAMP_BORE = TUBE_D - CLAMP_INTERFERENCE
CLAMP_WALL = 2.0
CLAMP_WIDTH = 12.0
CLAMP_OPEN = 90.0
CLAMP_R = CLAMP_BORE / 2.0
CLAMP_R_OUT = CLAMP_R + CLAMP_WALL

DOVE_RUN = 16.0
DOVE_DEPTH = 2.05
DOVE_ANGLE = 45.0
DOVE_DATUM = TUBE_D / 2.0 + CLAMP_WALL - CLAMP_INTERFERENCE / 2.0

WEB_FRONT = TUBE_D / 2.0 + 0.65
SLOT_BACK = DOVE_DATUM + DOVE_DEPTH
SLOT_DEPTH = 1.75
SLOT_LAND = 0.5
SLOT_MOUTH = 5.8
SLOT_FLOOR = SLOT_MOUTH + 2.0 * (
    SLOT_DEPTH - 2.0 * SLOT_LAND
) * tan(radians(DOVE_ANGLE))
SLOT_STOP = 1.0
SLOT_ROUND = 0.15
SLOT_BACK_ROUND = 0.3

# Feature 14 authors the slot entry 0.2 mm past slot_back before rounding.
SLOT_ENTRY_EXTENSION = 0.2

# Parent feature 199, applied after the linked clamp is inserted.
SLOT_ENTRY_CHAMFER = 0.14


def _open_clamp_ring():
    """Feature 1: Open klemring met afgeronde lippen."""
    half_open = radians(CLAMP_OPEN / 2.0)
    radial_mid = (CLAMP_R + CLAMP_R_OUT) / 2.0

    outer_x = CLAMP_R_OUT * cos(half_open)
    outer_y = CLAMP_R_OUT * sin(half_open)
    inner_x = CLAMP_R * cos(half_open)
    inner_y = CLAMP_R * sin(half_open)
    lip_center_x = radial_mid * cos(half_open)
    lip_center_y = radial_mid * sin(half_open)

    with Sketch(
        name="Open klemring met afgeronde lippen",
        plane="XY",
        offset=-CLAMP_WIDTH / 2.0,
    ) as sketch:
        profile = sketch.profile(start=(outer_x, outer_y))
        profile.arc_center_to(
            (outer_x, -outer_y),
            center=(0.0, 0.0),
            clockwise=False,
        )
        profile.arc_center_to(
            (inner_x, -inner_y),
            center=(lip_center_x, -lip_center_y),
            clockwise=False,
        )
        profile.arc_center_to(
            (inner_x, inner_y),
            center=(0.0, 0.0),
            clockwise=True,
        )
        profile.arc_center_to(
            (outer_x, outer_y),
            center=(lip_center_x, lip_center_y),
            clockwise=False,
        )
        profile.close()

    return sketch


def _rounded_slide_back():
    """Feature 12: Afgeronde rug voor de schuifgleuf."""
    left = -SLOT_BACK
    right = -WEB_FRONT
    bottom = -CLAMP_WIDTH / 2.0
    top = CLAMP_WIDTH / 2.0
    radius = SLOT_BACK_ROUND

    with Sketch(
        name="Afgeronde rug voor de schuifgleuf",
        plane="XZ",
        offset=-DOVE_RUN / 2.0,
    ) as sketch:
        start = (left, bottom + radius)
        profile = sketch.profile(start=start)

        profile.arc_center_to(
            (left + radius, bottom),
            center=(left + radius, bottom + radius),
            clockwise=False,
        )
        profile.line_to((right - radius, bottom))
        profile.arc_center_to(
            (right, bottom + radius),
            center=(right - radius, bottom + radius),
            clockwise=False,
        )
        profile.line_to((right, top - radius))
        profile.arc_center_to(
            (right - radius, top),
            center=(right - radius, top - radius),
            clockwise=False,
        )
        profile.line_to((left + radius, top))
        profile.arc_center_to(
            (left, top - radius),
            center=(left + radius, top - radius),
            clockwise=False,
        )
        profile.line_to(start)
        profile.close()

    return sketch


def _rounded_slide_slot():
    """Feature 14: Schuifgleuf met aanloop en printflanken."""
    angle = radians(DOVE_ANGLE)
    radius = SLOT_ROUND

    # The source sketch is an eight-corner profile. Its 45-degree flank
    # transitions are rounded with one common radius. These values are the
    # tangency distances derived from the authored dimensions, not stored
    # contour coordinates.
    flank_tangent = radius * tan(angle / 2.0)
    flank_dx = flank_tangent * cos(angle)
    flank_dz = flank_tangent * sin(angle)

    outer_x = -SLOT_BACK - SLOT_ENTRY_EXTENSION
    entry_x = -SLOT_BACK + SLOT_LAND
    inner_x = -SLOT_BACK + SLOT_DEPTH - SLOT_LAND
    open_x = -SLOT_BACK + SLOT_DEPTH
    mouth = SLOT_MOUTH / 2.0
    floor = SLOT_FLOOR / 2.0

    with Sketch(
        name="Schuifgleuf met aanloop en printflanken",
        plane="XZ",
        offset=-DOVE_RUN / 2.0 - 0.05,
    ) as sketch:
        start = (outer_x, -mouth + radius)
        profile = sketch.profile(start=start)

        # Lower entry radius.
        profile.arc_center_to(
            (outer_x + radius, -mouth),
            center=(outer_x + radius, -mouth + radius),
            clockwise=False,
        )
        profile.line_to((entry_x - flank_tangent, -mouth))

        # Lower concave transition into the print flank.
        profile.arc_center_to(
            (entry_x + flank_dx, -mouth - flank_dz),
            center=(entry_x - flank_tangent, -mouth - radius),
            clockwise=True,
        )
        profile.line_to((inner_x - flank_dx, -floor + flank_dz))

        # Lower transition from print flank to the floor land.
        profile.arc_center_to(
            (inner_x + flank_tangent, -floor),
            center=(inner_x + flank_tangent, -floor + radius),
            clockwise=False,
        )
        profile.line_to((open_x - radius, -floor))

        # Rounded lower open corner.
        profile.arc_center_to(
            (open_x, -floor + radius),
            center=(open_x - radius, -floor + radius),
            clockwise=False,
        )
        profile.line_to((open_x, floor - radius))

        # Mirrored upper half.
        profile.arc_center_to(
            (open_x - radius, floor),
            center=(open_x - radius, floor - radius),
            clockwise=False,
        )
        profile.line_to((inner_x + flank_tangent, floor))
        profile.arc_center_to(
            (inner_x - flank_dx, floor - flank_dz),
            center=(inner_x + flank_tangent, floor - radius),
            clockwise=False,
        )
        profile.line_to((entry_x + flank_dx, mouth + flank_dz))
        profile.arc_center_to(
            (entry_x - flank_tangent, mouth),
            center=(entry_x - flank_tangent, mouth + radius),
            clockwise=True,
        )
        profile.line_to((outer_x + radius, mouth))
        profile.arc_center_to(
            (outer_x, mouth - radius),
            center=(outer_x + radius, mouth - radius),
            clockwise=False,
        )
        profile.line_to(start)
        profile.close()

    return sketch


def _entry_chamfer_edges():
    """Native pick points for parent feature 199, derived from slot dimensions."""
    entry_x = -SLOT_BACK + SLOT_LAND
    inner_x = -SLOT_BACK + SLOT_DEPTH - SLOT_LAND
    open_x = -SLOT_BACK + SLOT_DEPTH
    flank_mid_x = (entry_x + inner_x) / 2.0
    flank_mid_z = (SLOT_MOUTH / 2.0 + SLOT_FLOOR / 2.0) / 2.0
    entry_y = -DOVE_RUN / 2.0

    return [
        (flank_mid_x, entry_y, flank_mid_z),
        (open_x, entry_y, 0.0),
        (flank_mid_x, entry_y, -flank_mid_z),
    ]


@component
class Hub75TubeClamp10mm:
    """Free/print-state loose clamp used by Edge and Corner tube interfaces."""

    def build(self):
        # Features 1/2: open elastic clamp ring in the native XY frame.
        ring_sketch = _open_clamp_ring()
        body = ring_sketch.extrude(CLAMP_WIDTH)

        # Features 12/13: low integrated rounded back for the slide slot.
        back_sketch = _rounded_slide_back()
        body = body + back_sketch.extrude(DOVE_RUN)

        # Features 14/15: rounded slide slot with a 1 mm closed end stop.
        slot_sketch = _rounded_slide_slot()
        body = body - slot_sketch.extrude(
            DOVE_RUN - SLOT_STOP + 0.05
        )

        # Parent feature 199: Inloop in groef van Ø10 proefklem.
        body = body.chamfer(
            SLOT_ENTRY_CHAMFER,
            edges=_entry_chamfer_edges(),
        )

        return body


Hub75TubeClamp10mm()
