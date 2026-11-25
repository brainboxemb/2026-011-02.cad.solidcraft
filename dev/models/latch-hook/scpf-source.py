"""Native sheet-metal latch hook reconstructed from the supplied drawing.

The model follows the manufacturing sequence directly:
1. cut one flat 2 mm sheet blank;
2. add the two mounting holes;
3. form one native sheet-metal hook bend.

The side projection is solved from the dimensioned formed geometry.  The top
outline keeps the dimensioned 24 mm mounting width, 14 mm hole pitch and 15 mm
neck, while the undimensioned transitions are circular blends tangent to both
mounting lobes and the straight neck.
"""

from math import atan2, degrees, hypot, radians, sqrt

from scpf import Hole, Sketch, component


# Dimensioned drawing inputs.
_THICKNESS = 2.0
_BEND_RADIUS = 2.1
_K_FACTOR = 0.40

_OVERALL_WIDTH = 24.0
_NECK_WIDTH = 15.0
_HOLE_DIAMETER = 4.3
_HOLE_PITCH = 14.0
_HOLE_X = 5.0

_FORMED_PROJECTION = 20.0
_HOOK_TIP_X = 13.5
_FORMED_HEIGHT = 10.5

# Undimensioned top-outline choice.  The drawing shows a short straight neck
# before the bend.  X=12 mm gives that neck while allowing a circular blend
# tangent to both the R5 mounting lobe and the 15 mm-wide straight section.
_NECK_START_X = 12.0


def _derive_side_geometry():
    """Return fold X, fold angle and required blank end from formed dimensions."""

    outside_radius = _BEND_RADIUS + _THICKNESS
    fold_x = _FORMED_PROJECTION - outside_radius

    # The outer bend circle is tangent to the bottom face of the fixed plate,
    # so its centre is at (fold_x, outside_radius).  The free outer tip is the
    # dimensioned point (13.5, 10.5).  Solve the upper-right tangent from that
    # point to the outside circle.
    cx = fold_x
    cz = outside_radius
    tx = _HOOK_TIP_X
    tz = _FORMED_HEIGHT

    vx = tx - cx
    vz = tz - cz
    distance_sq = vx * vx + vz * vz
    tangent_scale = outside_radius * outside_radius / distance_sq
    tangent_offset = (
        outside_radius
        * sqrt(distance_sq - outside_radius * outside_radius)
        / distance_sq
    )

    candidates = (
        (
            cx + tangent_scale * vx + tangent_offset * vz,
            cz + tangent_scale * vz - tangent_offset * vx,
        ),
        (
            cx + tangent_scale * vx - tangent_offset * vz,
            cz + tangent_scale * vz + tangent_offset * vx,
        ),
    )
    tangent_x, tangent_z = max(candidates, key=lambda point: point[0])

    fold_angle = degrees(
        atan2(tz - tangent_z, tx - tangent_x)
    )
    straight_lip = hypot(tx - tangent_x, tz - tangent_z)

    neutral_radius = _BEND_RADIUS + _K_FACTOR * _THICKNESS
    bend_allowance = radians(fold_angle) * neutral_radius

    # position="centerline" places half of the bend allowance on each side of
    # the authored fold line in the flat blank.
    blank_end_x = fold_x + bend_allowance / 2 + straight_lip
    return fold_x, fold_angle, blank_end_x


def _derive_top_blend():
    """Return one smooth upper transition from the R5 lobe to the 15 mm neck."""

    lobe_center = (_HOLE_X, _HOLE_PITCH / 2)
    lobe_radius = (_OVERALL_WIDTH - _HOLE_PITCH) / 2
    neck_point = (_NECK_START_X, _NECK_WIDTH / 2)

    # The blend must finish horizontally at the neck, so its centre lies
    # directly above neck_point.  Requiring external tangency to the R5 lobe
    # fixes that centre uniquely.
    cx, cy = lobe_center
    nx, ny = neck_point
    dx = nx - cx
    blend_center_y = (
        dx * dx
        + cy * cy
        - lobe_radius * lobe_radius
        - ny * ny
        + 2 * lobe_radius * ny
    ) / (2 * (cy + lobe_radius - ny))
    blend_center = (nx, blend_center_y)
    blend_radius = blend_center_y - ny

    centre_distance = lobe_radius + blend_radius
    contact = (
        cx + lobe_radius * (nx - cx) / centre_distance,
        cy + lobe_radius * (blend_center_y - cy) / centre_distance,
    )
    return contact, blend_center


_FOLD_X, _FOLD_ANGLE, _BLANK_END_X = _derive_side_geometry()
_TOP_CONTACT, _TOP_BLEND_CENTER = _derive_top_blend()


@component(include="*")
class LatchHook:
    thickness = _THICKNESS
    bend_radius = _BEND_RADIUS
    k_factor = _K_FACTOR

    overall_width = _OVERALL_WIDTH
    neck_width = _NECK_WIDTH
    hole_diameter = _HOLE_DIAMETER
    hole_pitch = _HOLE_PITCH
    hole_x = _HOLE_X

    def build(self):
        half_pitch = self.hole_pitch / 2
        half_neck = self.neck_width / 2
        top_y = self.overall_width / 2
        bottom_y = -top_y

        contact_x, contact_y = _TOP_CONTACT
        blend_cx, blend_cy = _TOP_BLEND_CENTER

        with Sketch(name="Latch hook blank", plane="XY") as blank:
            contour = blank.profile(start=(self.hole_x, top_y))

            # Upper R5 lobe -> tangent circular blend -> straight 15 mm neck.
            contour.arc_center_to(
                (contact_x, contact_y),
                center=(_HOLE_X, _HOLE_PITCH / 2),
                clockwise=True,
            )
            contour.arc_center_to(
                (_NECK_START_X, _NECK_WIDTH / 2),
                center=(blend_cx, blend_cy),
                clockwise=False,
            )
            contour.line_to((_BLANK_END_X, half_neck))
            contour.line_to((_BLANK_END_X, -half_neck))
            contour.line_to((_NECK_START_X, -_NECK_WIDTH / 2))

            # Mirrored lower blend and lower R5 mounting lobe.
            contour.arc_center_to(
                (contact_x, -contact_y),
                center=(blend_cx, -blend_cy),
                clockwise=False,
            )
            contour.arc_center_to(
                (_HOLE_X, -_OVERALL_WIDTH / 2),
                center=(_HOLE_X, -_HOLE_PITCH / 2),
                clockwise=True,
            )
            contour.arc_center_to(
                (0.0, -_HOLE_PITCH / 2),
                center=(_HOLE_X, -_HOLE_PITCH / 2),
                clockwise=True,
            )
            contour.line_to((0.0, _HOLE_PITCH / 2))
            contour.arc_center_to(
                (self.hole_x, top_y),
                center=(_HOLE_X, _HOLE_PITCH / 2),
                clockwise=True,
            )
            contour.close()

        hook = blank.sheet_metal(
            thickness=self.thickness,
            bend_radius=self.bend_radius,
            k_factor=self.k_factor,
            rule_name="Latch hook 2 mm",
        )

        for y in (-half_pitch, half_pitch):
            hook = hook + Hole(
                d=self.hole_diameter,
                direction=(0, 0, -1),
            ).at(self.hole_x, y, self.thickness)

        hook = hook.fold(
            line=((_FOLD_X, -7.5), (_FOLD_X, 7.5)),
            angle=_FOLD_ANGLE,
            fixed=(5.0, 0.0, 0.0),
            position="centerline",
        )

        return hook.with_material(
            "Galvanized steel",
            density_g_cm3=7.85,
            color="#B7BDC2",
        )


LatchHook()
