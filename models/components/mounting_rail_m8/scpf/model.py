"""Generic M8 mounting rail using native SolidCraft sheet metal.

The rail is manufactured in the same order as a real perforated rail:

    flat blank -> four-source perforation pattern -> four 90-degree folds

The flat-first route avoids attaching recess Sketches to an already-bent sheet
panel. The four physical source cuts remain one native repeated feature group.
"""

from math import pi

from scpf import (
    Axis,
    Circle2D,
    Polygon2D,
    Sketch,
    SlotCenterToCenter2D,
    component,
)


@component(include=("length", "repeat_count", "repeat_pitch"))
class MountingRailM8:
    # Standalone presentation default. The retail reference is 1000 mm.
    length = 250.0

    # Native editable repeat controls.
    repeat_count = 2
    repeat_pitch = 100.0

    # Generic 27/18 reference geometry.
    PROFILE_WIDTH = 27.0
    PROFILE_HEIGHT = 18.0
    THICKNESS = 1.25
    OPENING = 15.0

    BEND_RADIUS = 1.25
    K_FACTOR = 0.40

    FEATURE_PITCH = 25.0

    ROUND_DIAMETER = 12.5
    HORIZONTAL_SLOT_LENGTH = 10.0
    HORIZONTAL_SLOT_WIDTH = 6.4
    VERTICAL_SLOT_LENGTH = 15.0
    VERTICAL_SLOT_WIDTH = 8.4

    def build(self):
        thickness = self.THICKNESS

        # Develop the requested 27 x 18 outer section with the same 15 mm
        # opening. For a 90-degree centreline fold SolidCraft removes a bend
        # zone equal to BA = pi/2 * (R + K*T). Relative to the requested
        # outside virtual sharp, each fold centre therefore sits inward by:
        #
        #   projection = (R + T) - BA/2
        #
        # Applying that projection at every bend gives the flat distances
        # between fold centre lines and the free lip edges.
        bend_allowance = (
            pi / 2 * (self.BEND_RADIUS + self.K_FACTOR * thickness)
        )
        bend_projection = (
            self.BEND_RADIUS + thickness - bend_allowance / 2
        )

        back_span = self.PROFILE_WIDTH - 2 * bend_projection
        side_span = self.PROFILE_HEIGHT - 2 * bend_projection
        lip_outer = (self.PROFILE_WIDTH - self.OPENING) / 2
        lip_span = lip_outer - bend_projection

        flat_width = back_span + 2 * side_span + 2 * lip_span
        flat_half = flat_width / 2
        inner_fold_x = back_span / 2
        outer_fold_x = inner_fold_x + side_span

        # Preserve the existing local component contract:
        #   +Y is rail length, Y=0 is the rail start, opening points toward -Z,
        #   outer back face reaches Z=PROFILE_HEIGHT.
        back_inner_z = self.PROFILE_HEIGHT - thickness
        back_outer_z = self.PROFILE_HEIGHT

        with Sketch(
            name="Flat rail blank",
            plane="XY",
            origin=(0, 0, back_inner_z),
        ) as blank:
            Polygon2D(
                [
                    (-flat_half, 0),
                    (flat_half, 0),
                    (flat_half, self.length),
                    (-flat_half, self.length),
                ]
            )

        rail = blank.sheet_metal(
            thickness=thickness,
            bend_radius=self.BEND_RADIUS,
            k_factor=self.K_FACTOR,
            rule_name="Mounting Rail M8 Rule",
        )

        # Centre the four-feature source unit for the requested initial
        # length/count/pitch. The 250 mm standalone rail starts at 37.5 mm;
        # the 1000 mm / 10-repeat assembly rail starts at 12.5 mm.
        length_value = float(self.length.value)
        repeat_count_value = int(self.repeat_count.value)
        repeat_pitch_value = float(self.repeat_pitch.value)
        source_span = 3 * self.FEATURE_PITCH
        patterned_span = (
            (repeat_count_value - 1) * repeat_pitch_value
            + source_span
        )
        end_offset = (length_value - patterned_span) / 2
        if end_offset < 0:
            raise ValueError(
                "mounting rail repeat pattern does not fit inside the rail length"
            )

        y0 = end_offset
        y1 = y0 + self.FEATURE_PITCH
        y2 = y0 + 2 * self.FEATURE_PITCH
        y3 = y0 + 3 * self.FEATURE_PITCH

        horizontal_center_distance = (
            self.HORIZONTAL_SLOT_LENGTH - self.HORIZONTAL_SLOT_WIDTH
        )
        vertical_center_distance = (
            self.VERTICAL_SLOT_LENGTH - self.VERTICAL_SLOT_WIDTH
        )

        # Cut the still-flat back panel from an explicit world XY plane. This
        # intentionally avoids the already-bent sheet face/panel attachment
        # state that SolidCraft 0.48.1 misclassifies in live replay.
        cut_depth = -(2 * thickness)

        with Sketch(
            name="Repeat round A",
            on=rail,
            plane="XY",
            origin=(0, 0, back_outer_z),
        ) as round_a:
            round_a.add(
                Circle2D(d=self.ROUND_DIAMETER),
                offset=(0, y0),
            )
        round_a_cut = round_a.extrude(cut_depth)
        rail = rail - round_a_cut

        with Sketch(
            name="Repeat horizontal slot",
            on=rail,
            plane="XY",
            origin=(0, 0, back_outer_z),
        ) as horizontal_slot:
            half = horizontal_center_distance / 2
            SlotCenterToCenter2D(
                (0, y1 - half),
                (0, y1 + half),
                self.HORIZONTAL_SLOT_WIDTH,
            )
        horizontal_cut = horizontal_slot.extrude(cut_depth)
        rail = rail - horizontal_cut

        with Sketch(
            name="Repeat round B",
            on=rail,
            plane="XY",
            origin=(0, 0, back_outer_z),
        ) as round_b:
            round_b.add(
                Circle2D(d=self.ROUND_DIAMETER),
                offset=(0, y2),
            )
        round_b_cut = round_b.extrude(cut_depth)
        rail = rail - round_b_cut

        with Sketch(
            name="Repeat vertical slot",
            on=rail,
            plane="XY",
            origin=(0, 0, back_outer_z),
        ) as vertical_slot:
            half = vertical_center_distance / 2
            SlotCenterToCenter2D(
                (-half, y3),
                (half, y3),
                self.VERTICAL_SLOT_WIDTH,
            )
        vertical_cut = vertical_slot.extrude(cut_depth)
        rail = rail - vertical_cut

        rail = rail.rectangular_pattern(
            (
                round_a_cut,
                horizontal_cut,
                round_b_cut,
                vertical_cut,
            ),
            count=self.repeat_count,
            spacing=self.repeat_pitch,
            direction=Axis.Y,
        )

        # Fold the lips first while all four bend lines are still available in
        # the original flat plane. Then fold both side walls down. Keeping the
        # centre/back panel fixed preserves the component's existing +Y and -Z
        # orientation contract.
        fixed = (0.0, length_value / 2, back_inner_z)
        line_y = (0.0, length_value)

        rail = rail.fold(
            line=(
                (-outer_fold_x, line_y[0], back_inner_z),
                (-outer_fold_x, line_y[1], back_inner_z),
            ),
            angle=90,
            fixed=fixed,
            flip=True,
        )
        rail = rail.fold(
            line=(
                (outer_fold_x, line_y[0], back_inner_z),
                (outer_fold_x, line_y[1], back_inner_z),
            ),
            angle=90,
            fixed=fixed,
            flip=True,
        )
        rail = rail.fold(
            line=(
                (-inner_fold_x, line_y[0], back_inner_z),
                (-inner_fold_x, line_y[1], back_inner_z),
            ),
            angle=90,
            fixed=fixed,
            flip=True,
        )
        rail = rail.fold(
            line=(
                (inner_fold_x, line_y[0], back_inner_z),
                (inner_fold_x, line_y[1], back_inner_z),
            ),
            angle=90,
            fixed=fixed,
            flip=True,
        )

        return rail


MountingRailM8()
