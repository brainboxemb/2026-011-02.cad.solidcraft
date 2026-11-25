"""Measured detailed HUB75 panel from the supplied hub75_improved native source.

The reusable Hub75Panel component keeps the panel housing in its historical
local frame: XY is the 159.7 x 319.71 mm panel plane and +Z runs from the
front stack toward the rear. The standalone detailed root adds the source
connector envelopes and white orientation markings as separate physical
component occurrences. The final native-source "Paneel rechtop" move is
presentation-only and is intentionally mapped back to this stable local frame
so existing screen assemblies keep their placement contract.
"""

from scpf import (
    Anchor,
    Box,
    Cylinder,
    Hole,
    Placement,
    Polygon2D,
    Sketch,
    assembly,
    component,
    half,
)


MOUNTING_TUBE_OUTER_DIAMETER = 8.50
MOUNTING_TUBE_PROTRUSION = 0.50
MOUNTING_TUBE_RELIEF_CLEARANCE = 0.75
MOUNTING_TUBE_RELIEF_DEPTH = 0.80

REINFORCEMENT_OUTER_DIAMETER = 14.0
REINFORCEMENT_RECESS_DIAMETER = 10.0
REINFORCEMENT_RECESS_DEPTH = 2.50
REINFORCEMENT_HOLE_DIAMETER = 2.50
REINFORCEMENT_HOLE_DEPTH = 10.00
REINFORCEMENT_OFFSET = 11.0

LOCATOR_PIN_DIAMETER = 3.00
LOCATOR_PIN_PROTRUSION = 3.00
LOCATOR_PIN_X = 75.0
LOCATOR_PIN_Y = 110.0

DATA_CONNECTOR_CENTER_Y = 113.50
DATA_CONNECTOR_LENGTH = 27.90
DATA_CONNECTOR_WIDTH = 9.50
DATA_CONNECTOR_HEIGHT = 10.64
DATA_CONNECTOR_FRONT_OFFSET = 0.63
DATA_RECESS_LENGTH = 21.762
DATA_RECESS_WIDTH = 5.89
DATA_RECESS_HEIGHT = 0.80
DATA_RECESS_Z = 10.24

POWER_CONNECTOR_LENGTH = 13.0
POWER_CONNECTOR_WIDTH = 20.0
POWER_CONNECTOR_HEIGHT = 7.0
POWER_CONNECTOR_FRONT_OFFSET = 1.0

ORIENTATION_MARK_DEPTH = 0.10


@component
class Hub75Panel:
    """Reusable physical panel housing without separate connector/print bodies."""

    width = 159.70
    height = 319.71
    depth = 14.50
    front_depth = 2.00
    rear_inset = 1.25

    mount_x = 72.0
    mount_y = 152.0
    hole_diameter = 3.0

    rear_side_rail = 12.5
    rear_end_rail = 10.75
    rear_crossbar = 20.0

    def build(self):
        # Native features 1..5: straight front section plus continuous rear
        # taper to the 1.25 mm inset rear perimeter.
        body = Box(
            self.width,
            self.height,
            self.depth,
            anchor=Anchor.BOTTOM,
        ).taper(
            from_z=self.front_depth,
            inset=self.rear_inset,
        )

        # Native feature 54: four connected rear-bay profiles. The source uses
        # R5 nominal inner corners, 30 mm nominal central narrow sections and
        # 3 mm 45-degree transitions, scaled in the original 160 x 320 space.
        # Forge v0.16 keeps products of a Parameter and a numeric constant
        # associative, but does not accept Parameter * Expression. These are
        # the exact nominal source ratios for the measured 159.70 x 319.71
        # panel and match the native expressions at the accepted dimensions.
        width_scale = 159.70 / 160.0
        height_scale = 319.71 / 320.0
        side = self.rear_side_rail * width_scale
        end = self.rear_end_rail * height_scale
        rib_half = half(self.rear_crossbar * height_scale)
        corner_r = 5.0 * width_scale
        narrow_half = 15.0 * width_scale
        transition = 3.0 * height_scale

        half_width = half(self.width)
        half_height = half(self.height)
        quarter_height = self.height / 4.0
        inner_x = half_width - side
        corner_x = inner_x - corner_r

        bay_ranges = (
            (-half_height + end, -quarter_height - rib_half),
            (-quarter_height + rib_half, -rib_half),
            (rib_half, quarter_height - rib_half),
            (quarter_height + rib_half, half_height - end),
        )

        def add_bay(sketch, bottom, top):
            profile = sketch.profile(start=(-corner_x, bottom))
            profile.line_to((-narrow_half - transition, bottom))
            profile.line_to((-narrow_half, bottom - transition))
            profile.line_to((narrow_half, bottom - transition))
            profile.line_to((narrow_half + transition, bottom))
            profile.line_to((corner_x, bottom))
            profile.arc_center_to(
                (inner_x, bottom + corner_r),
                center=(corner_x, bottom + corner_r),
                clockwise=False,
            )
            profile.line_to((inner_x, top - corner_r))
            profile.arc_center_to(
                (corner_x, top),
                center=(corner_x, top - corner_r),
                clockwise=False,
            )
            profile.line_to((narrow_half + transition, top))
            profile.line_to((narrow_half, top + transition))
            profile.line_to((-narrow_half, top + transition))
            profile.line_to((-narrow_half - transition, top))
            profile.line_to((-corner_x, top))
            profile.arc_center_to(
                (-inner_x, top - corner_r),
                center=(-corner_x, top - corner_r),
                clockwise=False,
            )
            profile.line_to((-inner_x, bottom + corner_r))
            profile.arc_center_to(
                (-corner_x, bottom),
                center=(-corner_x, bottom + corner_r),
                clockwise=False,
            )
            profile.close()

        with Sketch(
            name="Achtervakken met afgeronde hoeken en versmallingen",
            on=body,
            parent=Anchor.TOP,
        ) as bays:
            for bottom, top in bay_ranges:
                add_bay(bays, bottom, top)

        body = body - bays.extrude(-(self.depth - self.front_depth))

        # Native features 8..19: shallow Ø10 reliefs and six Ø8.5 mounting
        # tubes, proud by 0.5 mm from the rear surface.
        relief_diameter = (
            MOUNTING_TUBE_OUTER_DIAMETER
            + 2 * MOUNTING_TUBE_RELIEF_CLEARANCE
        )
        for x in (-self.mount_x, self.mount_x):
            for y in (-self.mount_y, 0, self.mount_y):
                body = body + Hole(
                    d=relief_diameter,
                    depth=MOUNTING_TUBE_RELIEF_DEPTH,
                    direction=(0, 0, -1),
                ).at(x, y, self.depth)

                body = body + Cylinder(
                    d=MOUNTING_TUBE_OUTER_DIAMETER,
                    h=(
                        self.depth
                        + MOUNTING_TUBE_PROTRUSION
                        - self.front_depth
                    ),
                    anchor=Anchor.BOTTOM,
                ).at(
                    x,
                    y,
                    self.front_depth,
                    anchor=Anchor.BOTTOM,
                )

        # Native features 20..37: six separate reinforcement bosses with
        # shallow Ø10 recesses and Ø2.5 blind bores.
        reinforcement_positions = (
            (-self.mount_x, -self.mount_y + REINFORCEMENT_OFFSET),
            (self.mount_x, -self.mount_y + REINFORCEMENT_OFFSET),
            (-self.mount_x, REINFORCEMENT_OFFSET),
            (self.mount_x, -REINFORCEMENT_OFFSET),
            (-self.mount_x, self.mount_y - REINFORCEMENT_OFFSET),
            (self.mount_x, self.mount_y - REINFORCEMENT_OFFSET),
        )
        reinforcement_depth = (
            REINFORCEMENT_RECESS_DEPTH + REINFORCEMENT_HOLE_DEPTH
        )
        for x, y in reinforcement_positions:
            body = body + Cylinder(
                d=REINFORCEMENT_OUTER_DIAMETER,
                h=reinforcement_depth,
                anchor=Anchor.BOTTOM,
            ).at(
                x,
                y,
                self.depth - reinforcement_depth,
                anchor=Anchor.BOTTOM,
            )
            body = body + Hole(
                d=REINFORCEMENT_RECESS_DIAMETER,
                depth=REINFORCEMENT_RECESS_DEPTH,
                direction=(0, 0, -1),
            ).at(x, y, self.depth)
            body = body + Hole(
                d=REINFORCEMENT_HOLE_DIAMETER,
                depth=REINFORCEMENT_HOLE_DEPTH,
                direction=(0, 0, -1),
            ).at(x, y, self.depth - REINFORCEMENT_RECESS_DEPTH)

        # Native features 38/39: two diagonal Ø3 x 3 mm locating pins.
        for x, y in (
            (-LOCATOR_PIN_X, LOCATOR_PIN_Y),
            (LOCATOR_PIN_X, -LOCATOR_PIN_Y),
        ):
            body = body + Cylinder(
                d=LOCATOR_PIN_DIAMETER,
                h=LOCATOR_PIN_PROTRUSION,
                anchor=Anchor.BOTTOM,
            ).at(x, y, self.depth, anchor=Anchor.BOTTOM)

        # Native features 40..45: six Ø3 bores through the proud tube faces,
        # stopping at the rear-housing start.
        rear_bore_start = self.depth + MOUNTING_TUBE_PROTRUSION
        rear_bore_depth = rear_bore_start - self.front_depth
        for x in (-self.mount_x, self.mount_x):
            for y in (-self.mount_y, 0, self.mount_y):
                body = body + Hole(
                    d=self.hole_diameter,
                    depth=rear_bore_depth,
                    direction=(0, 0, -1),
                ).at(x, y, rear_bore_start)

        # Native features 46/47: trim all added rear geometry to the true
        # tapered side-wall envelope. This removes tube/boss overhang beyond
        # the long sloping sides without changing the accepted outer taper.
        with Sketch(
            name="Vlakke zijwand trim links",
            plane="XZ",
        ) as left_side_trim:
            Polygon2D(
                [
                    (-half_width, self.front_depth),
                    (-(half_width - self.rear_inset), self.depth),
                    (-(half_width + 5.0), self.depth),
                    (-(half_width + 5.0), self.front_depth),
                ],
                plane="XZ",
                world=True,
            )
        body = body - left_side_trim.extrude(self.height + 2.0, sym=True)

        with Sketch(
            name="Vlakke zijwand trim rechts",
            plane="XZ",
        ) as right_side_trim:
            Polygon2D(
                [
                    (half_width, self.front_depth),
                    (half_width - self.rear_inset, self.depth),
                    (half_width + 5.0, self.depth),
                    (half_width + 5.0, self.front_depth),
                ],
                plane="XZ",
                world=True,
            )
        body = body - right_side_trim.extrude(self.height + 2.0, sym=True)

        return body.with_material(
            "HUB75 housing",
            density_g_cm3=1.20,
            color="#B8B8B8",
        )


@component
class Hub75DataConnector:
    """Source-derived rear IDC/HUB75 connector clearance envelope."""

    def build(self):
        connector = Box(
            DATA_CONNECTOR_LENGTH,
            DATA_CONNECTOR_WIDTH,
            DATA_CONNECTOR_HEIGHT,
            anchor=Anchor.BOTTOM,
        )
        recess = Box(
            DATA_RECESS_LENGTH,
            DATA_RECESS_WIDTH,
            DATA_RECESS_HEIGHT,
            anchor=Anchor.BOTTOM,
        ).at(
            0,
            0,
            DATA_RECESS_Z,
            anchor=Anchor.BOTTOM,
        )
        return connector - recess


@component
class Hub75PowerConnector:
    """Approximate source power-connector clearance envelope."""

    def build(self):
        return Box(
            POWER_CONNECTOR_LENGTH,
            POWER_CONNECTOR_WIDTH,
            POWER_CONNECTOR_HEIGHT,
            anchor=Anchor.BOTTOM,
        )


@component
class Hub75ArrowDown:
    """White source orientation mark pointing in -Y in the local panel frame."""

    def build(self):
        with Sketch(name="Witte pijl omlaag", plane="XY") as sketch:
            Polygon2D([
                (-1.68, 7.56),
                (1.68, 7.56),
                (1.68, -2.10),
                (4.20, -2.10),
                (0.00, -7.56),
                (-4.20, -2.10),
                (-1.68, -2.10),
            ])
        return sketch.extrude(ORIENTATION_MARK_DEPTH).with_material(
            "Witte opdruk",
            density_g_cm3=1.20,
            color="#FFFFFF",
        )


@component
class Hub75ArrowRight:
    """White source orientation mark pointing in +X in the local panel frame."""

    def build(self):
        with Sketch(name="Witte pijl rechts", plane="XY") as sketch:
            Polygon2D([
                (-9.0, -2.0),
                (-9.0, 2.0),
                (2.5, 2.0),
                (2.5, 5.0),
                (9.0, 0.0),
                (2.5, -5.0),
                (2.5, -2.0),
            ])
        return sketch.extrude(ORIENTATION_MARK_DEPTH).with_material(
            "Witte opdruk",
            density_g_cm3=1.20,
            color="#FFFFFF",
        )


@assembly
class Hub75PanelDetailed:
    """Complete detailed source view while preserving Hub75Panel reuse."""

    width = 159.70
    height = 319.71
    depth = 14.50
    front_depth = 2.00
    rear_inset = 1.25
    rear_side_rail = 12.5
    rear_crossbar = 20.0
    rear_end_rail = 10.75
    mount_x = 72.0
    mount_y = 152.0
    hole_diameter = 3.0

    def build(self):
        housing = Hub75Panel(
            width=self.width,
            height=self.height,
            depth=self.depth,
            front_depth=self.front_depth,
            rear_inset=self.rear_inset,
            rear_side_rail=self.rear_side_rail,
            rear_crossbar=self.rear_crossbar,
            rear_end_rail=self.rear_end_rail,
            mount_x=self.mount_x,
            mount_y=self.mount_y,
            hole_diameter=self.hole_diameter,
            name="Hub75Panel",
        )

        lower_data = Hub75DataConnector(
            name="HUB75_data_onder",
            placement=Placement(
                y=-DATA_CONNECTOR_CENTER_Y,
                z=self.front_depth + DATA_CONNECTOR_FRONT_OFFSET,
            ),
        )
        upper_data = lower_data.copy(
            name="HUB75_data_boven",
            placement=Placement(
                y=DATA_CONNECTOR_CENTER_Y,
                z=self.front_depth + DATA_CONNECTOR_FRONT_OFFSET,
            ),
        )

        power_x = self.width * (53.0 / 160.0 - 0.5)
        power_y = self.height * (128.0 / 320.0 - 0.5)
        power = Hub75PowerConnector(
            name="Voedingsconnector",
            placement=Placement(
                x=power_x,
                y=power_y,
                z=self.front_depth + POWER_CONNECTOR_FRONT_OFFSET,
            ),
        )

        side = self.rear_side_rail * (159.70 / 160.0)
        arrow_right_x = self.width / 2.0 - side - 21.0
        source_midline = (
            (
                self.rear_end_rail * (319.71 / 320.0)
                + self.height / 4.0
                - self.rear_crossbar * (319.71 / 320.0) / 2.0
            )
            / 2.0
            - self.height / 2.0
        )

        arrow_down_top = Hub75ArrowDown(
            name="Orientatiepijl_1",
            placement=Placement(
                x=-38.0,
                y=113.5,
                z=self.front_depth,
            ),
        )
        arrow_right_upper = Hub75ArrowRight(
            name="Orientatiepijl_2",
            placement=Placement(
                x=arrow_right_x,
                y=self.height * 0.125,
                z=self.front_depth,
            ),
        )
        arrow_down_lower = arrow_down_top.copy(
            name="Orientatiepijl_3",
            placement=Placement(
                x=-38.0,
                y=source_midline,
                z=self.front_depth,
            ),
        )
        arrow_right_lower = arrow_right_upper.copy(
            name="Orientatiepijl_4",
            placement=Placement(
                x=arrow_right_x,
                y=source_midline,
                z=self.front_depth,
            ),
        )

        return (
            housing
            + lower_data
            + upper_data
            + power
            + arrow_down_top
            + arrow_right_upper
            + arrow_down_lower
            + arrow_right_lower
        )


Hub75PanelDetailed()
