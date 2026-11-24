"""Generic M8 mounting rail using native SolidCraft sheet metal.

The rail body is one native 27/18-style C-profile contour flange. One physical
perforation repeat unit consists of four fixed reference cut features:

    round -> longitudinal slot -> round -> transverse slot

Those four already-applied source features are passed together to ONE native
rectangular feature pattern. The rail length plus pattern count and spacing are
native editable Forge/SolidCraft parameters.
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


@component(include=("length", "repeat_count", "repeat_pitch"))
class MountingRailM8:
    # Standalone presentation default. The retail reference is 1000 mm.
    length = 250.0

    # Native editable repeat controls.
    repeat_count = 2
    repeat_pitch = 100.0

    # Generic 27/18 reference geometry. Keep source punch geometry fixed:
    # SolidCraft 0.48.1 sheet recess validation is reliable for these numeric
    # profiles, while symbolic disconnected sheet-cut geometry can be
    # misclassified as reaching a bend.
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
        half_side = (self.PROFILE_WIDTH - thickness) / 2
        lower_z = thickness / 2
        upper_z = self.PROFILE_HEIGHT - thickness / 2
        opening_half = self.OPENING / 2

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
            thickness=thickness,
            bend_radius=self.BEND_RADIUS,
            k_factor=self.K_FACTOR,
            rule_name="Mounting Rail M8 Rule",
        )

        # Centre the authored numeric source unit for the requested initial
        # length/count/pitch. This keeps the 250 mm default at 37.5 mm and a
        # 1000 mm / 10-repeat rail at the product-like 12.5 mm end margin,
        # while the native pattern count and spacing remain editable.
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

        with Sketch(
            name="Repeat round A",
            on=rail,
            parent=Anchor.TOP,
        ) as round_a:
            round_a.add(
                Circle2D(d=self.ROUND_DIAMETER),
                offset=(0, y0),
            )
        round_a_cut = round_a.extrude(Depth.THROUGH_ALL)
        rail = rail - round_a_cut

        with Sketch(
            name="Repeat horizontal slot",
            on=rail,
            parent=Anchor.TOP,
        ) as horizontal_slot:
            half = horizontal_center_distance / 2
            SlotCenterToCenter2D(
                (0, y1 - half),
                (0, y1 + half),
                self.HORIZONTAL_SLOT_WIDTH,
            )
        horizontal_cut = horizontal_slot.extrude(Depth.THROUGH_ALL)
        rail = rail - horizontal_cut

        with Sketch(
            name="Repeat round B",
            on=rail,
            parent=Anchor.TOP,
        ) as round_b:
            round_b.add(
                Circle2D(d=self.ROUND_DIAMETER),
                offset=(0, y2),
            )
        round_b_cut = round_b.extrude(Depth.THROUGH_ALL)
        rail = rail - round_b_cut

        with Sketch(
            name="Repeat vertical slot",
            on=rail,
            parent=Anchor.TOP,
        ) as vertical_slot:
            half = vertical_center_distance / 2
            SlotCenterToCenter2D(
                (-half, y3),
                (half, y3),
                self.VERTICAL_SLOT_WIDTH,
            )
        vertical_cut = vertical_slot.extrude(Depth.THROUGH_ALL)
        rail = rail - vertical_cut

        patterned = rail.rectangular_pattern(
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
        return patterned.with_material(
            "Galvanized steel",
            density_g_cm3=7.85,
            color="#9EA6AA",
        )


MountingRailM8()
