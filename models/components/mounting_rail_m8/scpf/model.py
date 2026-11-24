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
    Circle2D,
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

    # Generic 27/18 perforation reference. The sequence is:
    # round -> longitudinal slot -> round -> transverse slot -> repeat.
    END_OFFSET = 12.5
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

        # The top/back web is perforated by one standalone XY Sketch at Z=18.
        # Pattern centres are spaced at 25 mm, starting 12.5 mm from the end.
        # Four positions make one 100 mm repeat unit.
        length_value = float(self.length.value)
        feature_count = int(
            (length_value - 2 * self.END_OFFSET) // self.FEATURE_PITCH
        ) + 1

        horizontal_center_distance = (
            self.HORIZONTAL_SLOT_LENGTH - self.HORIZONTAL_SLOT_WIDTH
        )
        vertical_center_distance = (
            self.VERTICAL_SLOT_LENGTH - self.VERTICAL_SLOT_WIDTH
        )

        with Sketch(
            name="Perforation pattern",
            plane="XY",
            origin=(0, 0, self.PROFILE_HEIGHT),
        ) as holes:
            for index in range(feature_count):
                y = self.END_OFFSET + index * self.FEATURE_PITCH
                kind = index % 4

                if kind in (0, 2):
                    holes.add(
                        Circle2D(d=self.ROUND_DIAMETER),
                        offset=(0, y),
                    )
                elif kind == 1:
                    half = horizontal_center_distance / 2
                    SlotCenterToCenter2D(
                        (0, y - half),
                        (0, y + half),
                        self.HORIZONTAL_SLOT_WIDTH,
                    )
                else:
                    half = vertical_center_distance / 2
                    SlotCenterToCenter2D(
                        (-half, y),
                        (half, y),
                        self.VERTICAL_SLOT_WIDTH,
                    )

        # The cutter starts on the outside of the 18 mm web and passes through
        # only the 1.25 mm sheet; extra depth keeps the Boolean robust.
        return rail - holes.extrude(-4.0)


MountingRailM8()
