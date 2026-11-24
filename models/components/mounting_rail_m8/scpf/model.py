"""Generic parametric M8 mounting rail using native SolidCraft sheet metal.

The rail body is one native 27/18-style C-profile contour flange. The
perforation is authored as ONE four-profile repeat unit:

    round -> longitudinal slot -> round -> transverse slot

That unit becomes one web-through cut feature and one native rectangular
feature pattern. Pattern count, spacing and all profile dimensions remain
editable Forge/SolidCraft parameters.
"""

from scpf import (
    Anchor,
    Axis,
    Circle2D,
    Sketch,
    SlotCenterToCenter2D,
    component,
)


@component(include="*")
class MountingRailM8:
    # Product / section dimensions.
    length = 250.0
    profile_width = 27.0
    profile_height = 18.0
    thickness = 1.25
    opening = 15.0

    # Native sheet rule. These remain explicit assumptions until measured.
    bend_radius = 1.25
    k_factor = 0.40

    # One complete perforation cycle contains four features. The default
    # 25 mm feature pitch therefore gives a 100 mm native repeat pitch.
    end_offset = 37.5
    feature_pitch = 25.0
    repeat_count = 2

    round_diameter = 12.5

    horizontal_slot_length = 10.0
    horizontal_slot_width = 6.4

    vertical_slot_length = 15.0
    vertical_slot_width = 8.4

    def build(self):
        half_side = (self.profile_width - self.thickness) / 2
        lower_z = self.thickness / 2
        upper_z = self.profile_height - self.thickness / 2
        opening_half = self.opening / 2

        # Native sheet-metal C-profile.
        with Sketch(name="C profile", plane="XZ") as profile:
            chain = profile.chain(start=(-opening_half, lower_z))
            chain.line_to((-half_side, lower_z))
            chain.line_to((-half_side, upper_z))
            chain.line_to((half_side, upper_z))
            chain.line_to((half_side, lower_z))
            chain.line_to((opening_half, lower_z))
            contour = chain.finish()

        rail = contour.contour_flange(
            distance=self.length,
            thickness=self.thickness,
            bend_radius=self.bend_radius,
            k_factor=self.k_factor,
            rule_name="Mounting Rail M8 Rule",
        )

        # Author one complete 4-feature repeat unit on the real top web.
        # end_offset is a native editable parameter instead of a derived
        # Expression*Expression formula, which Forge 0.15 deliberately does
        # not support.
        repeat_pitch = 4 * self.feature_pitch
        y0 = self.end_offset
        y1 = y0 + self.feature_pitch
        y2 = y0 + 2 * self.feature_pitch
        y3 = y0 + 3 * self.feature_pitch

        horizontal_center_distance = (
            self.horizontal_slot_length - self.horizontal_slot_width
        )
        vertical_center_distance = (
            self.vertical_slot_length - self.vertical_slot_width
        )

        with Sketch(
            name="Perforation repeat unit",
            on=rail,
            parent=Anchor.TOP,
        ) as unit:
            unit.add(
                Circle2D(d=self.round_diameter),
                offset=(0, y0),
            )

            horizontal_half = horizontal_center_distance / 2
            SlotCenterToCenter2D(
                (0, y1 - horizontal_half),
                (0, y1 + horizontal_half),
                self.horizontal_slot_width,
            )

            unit.add(
                Circle2D(d=self.round_diameter),
                offset=(0, y2),
            )

            vertical_half = vertical_center_distance / 2
            SlotCenterToCenter2D(
                (-vertical_half, y3),
                (vertical_half, y3),
                self.vertical_slot_width,
            )

        # One shallow cut owns the complete 4-profile unit. Cutting only
        # through the web avoids SolidCraft's unsupported sheet-bend recess
        # case that THROUGH_ALL triggers for a compound profile.
        unit_cut = unit.extrude(-2 * self.thickness)
        rail = rail - unit_cut

        return rail.rectangular_pattern(
            unit_cut,
            count=self.repeat_count,
            spacing=repeat_pitch,
            direction=Axis.Y,
        )


MountingRailM8()
