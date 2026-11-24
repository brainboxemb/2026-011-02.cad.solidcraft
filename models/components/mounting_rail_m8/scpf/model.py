"""Generic M8 mounting rail based on a light 27/18 installation C-profile.

Product facts retained from the supplied DRESSELHAUS/HORNBACH reference:
- galvanized steel;
- 1.25 mm material thickness;
- 1000 mm product length;
- intended for M8 threaded rods / pipe-clamp installation.

The 27 x 18 mm section and perforation geometry are generic 27/18 reference
dimensions, not claimed DRESSELHAUS manufacturing specifications.
"""

from scpf import (
    Anchor,
    Axis,
    Depth,
    Hole,
    Sketch,
    SlotCenterToCenter2D,
    component,
)


@component(include=("length",))
class MountingRailM8:
    length = 1000.0

    # Generic 27/18 light C-profile reference dimensions.
    PROFILE_WIDTH = 27.0
    PROFILE_HEIGHT = 18.0
    THICKNESS = 1.25
    OPENING = 15.0

    # Manufacturing assumptions until a specific maker drawing is available.
    BEND_RADIUS = 1.25
    K_FACTOR = 0.40

    # Generic 27/18 perforation reference. Along the rail:
    # round -> horizontal slot -> round -> vertical slot -> repeat.
    END_OFFSET = 12.5
    FEATURE_PITCH = 25.0
    ROUND_PITCH = 50.0
    SLOT_PITCH = 100.0

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

        # One open XZ sheet contour creates the complete C-profile as native
        # SolidCraft sheet-metal history over the requested rail length.
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

        length_value = float(self.length.value)

        # Round openings occur every 50 mm: 12.5, 62.5, 112.5, ...
        round_first = self.END_OFFSET
        round_count = int(
            (length_value - self.END_OFFSET - round_first) // self.ROUND_PITCH
        ) + 1
        round_hole = Hole(
            d=self.ROUND_DIAMETER,
            direction=(0, 0, -1),
        ).at(0, round_first, self.PROFILE_HEIGHT)
        rail = rail + round_hole
        rail = rail.rectangular_pattern(
            round_hole,
            count=round_count,
            spacing=self.ROUND_PITCH,
            direction=Axis.Y,
        )

        # Horizontal/longitudinal slot: first centre at 37.5 mm, then 100 mm.
        horizontal_first = self.END_OFFSET + self.FEATURE_PITCH
        horizontal_center_distance = (
            self.HORIZONTAL_SLOT_LENGTH - self.HORIZONTAL_SLOT_WIDTH
        )
        with Sketch(
            name="Horizontal slot",
            on=rail,
            parent=Anchor.TOP,
        ) as horizontal_slot:
            half = horizontal_center_distance / 2
            SlotCenterToCenter2D(
                (0, horizontal_first - half),
                (0, horizontal_first + half),
                self.HORIZONTAL_SLOT_WIDTH,
            )

        horizontal_cut = horizontal_slot.extrude(Depth.THROUGH_ALL)
        rail = rail - horizontal_cut
        horizontal_count = int(
            (length_value - self.END_OFFSET - horizontal_first)
            // self.SLOT_PITCH
        ) + 1
        rail = rail.rectangular_pattern(
            horizontal_cut,
            count=horizontal_count,
            spacing=self.SLOT_PITCH,
            direction=Axis.Y,
        )

        # Vertical/transverse slot: first centre at 87.5 mm, then 100 mm.
        vertical_first = self.END_OFFSET + 3 * self.FEATURE_PITCH
        vertical_center_distance = (
            self.VERTICAL_SLOT_LENGTH - self.VERTICAL_SLOT_WIDTH
        )
        with Sketch(
            name="Vertical slot",
            on=rail,
            parent=Anchor.TOP,
        ) as vertical_slot:
            half = vertical_center_distance / 2
            SlotCenterToCenter2D(
                (-half, vertical_first),
                (half, vertical_first),
                self.VERTICAL_SLOT_WIDTH,
            )

        vertical_cut = vertical_slot.extrude(Depth.THROUGH_ALL)
        rail = rail - vertical_cut
        vertical_count = int(
            (length_value - self.END_OFFSET - vertical_first)
            // self.SLOT_PITCH
        ) + 1
        return rail.rectangular_pattern(
            vertical_cut,
            count=vertical_count,
            spacing=self.SLOT_PITCH,
            direction=Axis.Y,
        )


MountingRailM8()
