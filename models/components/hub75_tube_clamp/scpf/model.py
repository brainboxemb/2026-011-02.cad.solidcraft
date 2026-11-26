"""Reusable parameterized HUB75 tube clamp in its Free/print state."""

from math import cos, radians, sin, tan

from scpf import Sketch, component


# Fixed source dimensions shared by all tube sizes.
CLAMP_WALL = 2.0
CLAMP_WIDTH = 12.0
CLAMP_OPEN = 90.0

DOVE_RUN = 16.0
DOVE_DEPTH = 2.05
DOVE_ANGLE = 45.0

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


def _open_clamp_ring(*, clamp_r, clamp_r_out):
    """Feature 1: Open klemring met afgeronde lippen."""
    half_open = radians(CLAMP_OPEN / 2.0)
    radial_mid = (clamp_r + clamp_r_out) / 2.0

    outer_x = clamp_r_out * cos(half_open)
    outer_y = clamp_r_out * sin(half_open)
    inner_x = clamp_r * cos(half_open)
    inner_y = clamp_r * sin(half_open)
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


def _rounded_slide_back(*, slot_back, web_front):
    """Feature 12: Afgeronde rug voor de schuifgleuf."""
    left = -slot_back
    right = -web_front
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


def _rounded_slide_slot(*, slot_back):
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

    outer_x = -slot_back - SLOT_ENTRY_EXTENSION
    entry_x = -slot_back + SLOT_LAND
    inner_x = -slot_back + SLOT_DEPTH - SLOT_LAND
    open_x = -slot_back + SLOT_DEPTH
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


def _entry_chamfer_edges(*, slot_back):
    """Native pick points for parent feature 199, derived from slot dimensions."""
    entry_x = -slot_back + SLOT_LAND
    inner_x = -slot_back + SLOT_DEPTH - SLOT_LAND
    open_x = -slot_back + SLOT_DEPTH
    flank_mid_x = (entry_x + inner_x) / 2.0
    flank_mid_z = (SLOT_MOUTH / 2.0 + SLOT_FLOOR / 2.0) / 2.0
    entry_y = -DOVE_RUN / 2.0

    return [
        (flank_mid_x, entry_y, flank_mid_z),
        (open_x, entry_y, 0.0),
        (flank_mid_x, entry_y, -flank_mid_z),
    ]


@component(include=("tube_d", "clamp_interference"))
class Hub75TubeClamp:
    """Loose clamp; the physical component defaults to its Free/print state."""

    tube_d = 10.0
    clamp_interference = 0.4

    def build(self):
        # Free is the intrinsic standalone/manufacturing state. Installed state
        # is deliberately added later at the assembly/configuration layer.
        clamp_bore = self.tube_d - self.clamp_interference
        clamp_r = clamp_bore / 2.0
        clamp_r_out = clamp_r + CLAMP_WALL

        dove_datum = (
            self.tube_d / 2.0
            + CLAMP_WALL
            - self.clamp_interference / 2.0
        )
        web_front = self.tube_d / 2.0 + 0.65
        slot_back = dove_datum + DOVE_DEPTH

        # Features 1/2: open elastic clamp ring in the native XY frame.
        ring_sketch = _open_clamp_ring(
            clamp_r=clamp_r,
            clamp_r_out=clamp_r_out,
        )
        body = ring_sketch.extrude(CLAMP_WIDTH)

        # Features 12/13: low integrated rounded back for the slide slot.
        back_sketch = _rounded_slide_back(
            slot_back=slot_back,
            web_front=web_front,
        )
        body = body + back_sketch.extrude(DOVE_RUN)

        # Features 14/15: rounded slide slot with a 1 mm closed end stop.
        slot_sketch = _rounded_slide_slot(slot_back=slot_back)
        body = body - slot_sketch.extrude(
            DOVE_RUN - SLOT_STOP + 0.05
        )

        # Parent feature 199: Inloop in groef van de proefklem.
        body = body.chamfer(
            SLOT_ENTRY_CHAMFER,
            edges=_entry_chamfer_edges(slot_back=slot_back),
        )

        return body


Hub75TubeClamp()
