"""Generic parametric M8 mounting rail using native SolidCraft sheet metal.

The rail body is one native 27/18-style C-profile contour flange. One physical
perforation repeat unit consists of four native cut features:

    round -> longitudinal slot -> round -> transverse slot

Those four already-applied source features are passed together to ONE native
rectangular feature pattern. Pattern count, spacing and all profile dimensions
remain editable Forge/SolidCraft parameters.
"""

from scpf import (
    Anchor,
    Axis,
    Circle2D,
    Depth,
    Sketch,
    SlotCenterToCenter2D,
    component,
)


@component(include="*")
class MountingRailM8:
    # Standalone presentation default. The reference retail product is 1000 mm.
    length = 250.0

    # Generic 27/18 light C-profile reference dimensions.
    profile_width = 27.0
    profile_height = 18.0
    thickness = 1.25
    opening = 15.0

    # Native sheet rule. These remain explicit assumptions until measured.
    bend_radius = 1.25
    k_factor = 0.40

    # One complete perforation cycle contains four features.
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

        # One physical four-feature repeat unit.
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

        # Source feature 1: round opening.
        with Sketch(
            name="Repeat round A",
            on=rail,
            parent=Anchor.TOP,
        ) as round_a:
            round_a.add(
                Circle2D(d=self.round_diameter),
                offset=(0, y0),
            )
        round_a_cut = round_a.extrude(Depth.THROUGH_ALL)
        rail = rail - round_a_cut

        # Source feature 2: longitudinal slot.
        with Sketch(
            name="Repeat horizontal slot",
            on=rail,
            parent=Anchor.TOP,
        ) as horizontal_slot:
            half = horizontal_center_distance / 2
            SlotCenterToCenter2D(
                (0, y1 - half),
                (0, y1 + half),
                self.horizontal_slot_width,
            )
        horizontal_cut = horizontal_slot.extrude(Depth.THROUGH_ALL)
        rail = rail - horizontal_cut

        # Source feature 3: second round opening.
        with Sketch(
            name="Repeat round B",
            on=rail,
            parent=Anchor.TOP,
        ) as round_b:
            round_b.add(
                Circle2D(d=self.round_diameter),
                offset=(0, y2),
            )
        round_b_cut = round_b.extrude(Depth.THROUGH_ALL)
        rail = rail - round_b_cut

        # Source feature 4: transverse slot.
        with Sketch(
            name="Repeat vertical slot",
            on=rail,
            parent=Anchor.TOP,
        ) as vertical_slot:
            half = vertical_center_distance / 2
            SlotCenterToCenter2D(
                (-half, y3),
                (half, y3),
                self.vertical_slot_width,
            )
        vertical_cut = vertical_slot.extrude(Depth.THROUGH_ALL)
        rail = rail - vertical_cut

        # Forge 0.15 accepts a sequence of already-applied native features.
        # SolidCraft therefore stores ONE rectangular pattern whose source
        # feature list is the complete four-feature physical repeat unit.
        return rail.rectangular_pattern(
            (
                round_a_cut,
                horizontal_cut,
                round_b_cut,
                vertical_cut,
            ),
            count=self.repeat_count,
            spacing=repeat_pitch,
            direction=Axis.Y,
        )


MountingRailM8()
