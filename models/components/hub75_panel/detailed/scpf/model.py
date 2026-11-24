"""Single measured HUB75 panel reused in the regression and screen assembly.

Authoritative reference: lib.scad.hub75 / HUB75 frame project v1.2.
The CAD body uses the measured rear taper, four explicit rounded/stepped rear
electronics-bay contours and the accepted mounting/reinforcement interfaces.
The shallow rail recess and connector envelopes remain separate follow-up
features.
"""
from math import sqrt

from scpf import (
    Anchor,
    Box,
    Cylinder,
    Hole,
    Polygon2D,
    RoundedRectangle2D,
    Sketch,
    component,
    half,
)


# Fixed mechanical interface dimensions from the existing v1.2 panel
# reference. These are product geometry, not editable design parameters.
MOUNTING_TUBE_OUTER_DIAMETER = 8.50
MOUNTING_TUBE_PROTRUSION = 0.50
MOUNTING_TUBE_RELIEF_CLEARANCE = 0.75
MOUNTING_TUBE_RELIEF_DEPTH = 0.80

# Separate reinforcement features beside the six mounting tubes. The Ø14 and
# Ø2.5 values remain documented as current physical estimates in the source
# reference rather than drawing dimensions.
REINFORCEMENT_OUTER_DIAMETER = 14.0
REINFORCEMENT_RECESS_DIAMETER = 10.0
REINFORCEMENT_RECESS_DEPTH = 2.50
REINFORCEMENT_HOLE_DIAMETER = 2.50
REINFORCEMENT_HOLE_DEPTH = 10.00
REINFORCEMENT_OFFSET = 11.0

# Two PDF-related locating pins in centred portrait component coordinates.
LOCATOR_PIN_DIAMETER = 3.00
LOCATOR_PIN_PROTRUSION = 3.00
LOCATOR_PIN_X = 75.0
LOCATOR_PIN_Y = 110.0

# STEP-derived rear bay contour details. The reference values live in nominal
# 160 x 320 mm panel space and are scaled into the measured 159.70 x 319.71 mm
# envelope in build(), matching the preserved v1.2 OpenSCAD component.
REAR_END_NARROW_WIDTH = 7.75
REAR_END_NARROW_LENGTH = 30.0
REAR_OPENING_CORNER_RADIUS = 5.0

# Shallow STEP-derived rear rail recess. These values are explicitly
# approximate rear-frame details from the v1.2 reference, not PDF dimensions.
REAR_RECESS_DEPTH = 0.80
REAR_SIDE_RECESS_MARGIN = 2.0
REAR_END_RECESS_MARGIN = 2.0
REAR_CROSSBAR_RECESS_MARGIN = 1.5
REAR_RECESS_CORNER_RADIUS = 0.8


@component
class Hub75Panel:
    width = 159.70
    height = 319.71
    depth = 14.50
    front_depth = 2.00  # straight front: 1 mm mask + 1 mm PCB
    rear_inset = 1.25   # STEP taper: inset on every side at the rear

    # Source holes: X=7.85/151.85, Z=7.855/159.855/311.855 from
    # the drawing's lower-left corner. They become +/-72 and +/-152
    # once the panel is centred on the front plane.
    mount_x = 72.0
    mount_y = 152.0
    hole_diameter = 3.0

    # Rear web geometry from v1.2 hub75_panel.scad / supplied STEP reference.
    # Source dimensions belong to nominal 160 x 320 mm reference space.
    rear_side_rail = 12.5       # each long rail, X direction
    rear_end_rail = 10.75      # top/bottom border, long Y direction
    rear_crossbar = 20.0       # 3 horizontal ribs, centered at quarters

    def build(self):
        # Real long sloping sides from Z=2 to Z=14.5, not a short bevel.
        body = Box(self.width, self.height, self.depth, anchor=Anchor.BOTTOM).taper(
            from_z=self.front_depth, inset=self.rear_inset,
        )

        # Cut the four electronics bays FROM THE REAR, leaving the complete
        # front mask + PCB stack at Z=0..2 mm. The v1.2 STEP/OpenSCAD
        # reference uses one continuous contour per bay: R5 inner corners plus
        # a central stepped relief at the top and bottom edge.
        #
        # OpenSCAD source coordinates use X/Z in the display face; SCPF uses
        # X/Y. The reference's 80/160/240 mm rib positions therefore become
        # Y=-H/4, Y=0 and Y=+H/4 in portrait orientation.
        side = self.rear_side_rail * (159.70 / 160.0)
        end = self.rear_end_rail * (319.71 / 320.0)
        narrow_end = REAR_END_NARROW_WIDTH * (319.71 / 320.0)
        rib_half = half(self.rear_crossbar * (319.71 / 320.0))
        half_height = half(self.height)
        quarter_height = self.height / 4
        opening_width = self.width - 2 * side
        left = -half(opening_width)
        right = half(opening_width)

        # The 10.75 -> 7.75 mm rail change is a nominal 3 mm step with 45°
        # transitions. The 30 mm narrow section scales along panel X.
        step_depth = end - narrow_end
        half_narrow = half(
            REAR_END_NARROW_LENGTH * (159.70 / 160.0)
        )

        # The reference takes the minimum of X/Y scaling for R5. The measured
        # panel has the smaller X scale, so this exact expression preserves the
        # reference default while staying associative with editable width.
        corner_radius = REAR_OPENING_CORNER_RADIUS * (self.width / 160.0)

        bay_ranges = (
            (-half_height + end, -quarter_height - rib_half),
            (-quarter_height + rib_half, -rib_half),
            (rib_half, quarter_height - rib_half),
            (quarter_height + rib_half, half_height - end),
        )
        with Sketch(
            name="Rear electronics bays",
            on=body,
            parent=Anchor.TOP,
        ) as bays:
            for bottom, top in bay_ranges:
                start_point = (left + corner_radius, bottom)
                profile = bays.profile(start=start_point)

                # Bottom edge with the central rail relief extending outward.
                profile.line_to((-(step_depth + half_narrow), bottom))
                profile.line_to((-half_narrow, bottom - step_depth))
                profile.line_to((half_narrow, bottom - step_depth))
                profile.line_to((half_narrow + step_depth, bottom))
                profile.line_to((right - corner_radius, bottom))

                # Right-side R5 corners and wall.
                profile.arc_center_to(
                    (right, bottom + corner_radius),
                    center=(right - corner_radius, bottom + corner_radius),
                )
                profile.line_to((right, top - corner_radius))
                profile.arc_center_to(
                    (right - corner_radius, top),
                    center=(right - corner_radius, top - corner_radius),
                )

                # Top edge with the same central relief mirrored upward.
                profile.line_to((half_narrow + step_depth, top))
                profile.line_to((half_narrow, top + step_depth))
                profile.line_to((-half_narrow, top + step_depth))
                profile.line_to((-(step_depth + half_narrow), top))
                profile.line_to((left + corner_radius, top))

                # Left-side R5 corners and wall, returning to the authored
                # start point so Forge registers one closed profile region.
                profile.arc_center_to(
                    (left, top - corner_radius),
                    center=(left + corner_radius, top - corner_radius),
                )
                profile.line_to((left, bottom + corner_radius))
                profile.arc_center_to(
                    start_point,
                    center=(left + corner_radius, bottom + corner_radius),
                )
                profile.close()

        body = body - bays.extrude(-(self.depth - self.front_depth))

        # The resulting contour keeps the normal 10.75 mm end rails, narrows
        # them to 7.75 mm across the central 30 mm section, and leaves the
        # three nominal 20 mm separators with the reference 14 mm stepped
        # centre after both adjacent 3 mm reliefs.

        # Recess the rear-facing rail strips by the reference 0.8 mm. Keep
        # this as a separate cut from the electronics bays: the recess is a
        # shallow surface feature, while the bay cut runs to front_depth.
        #
        # Side/end strips use the reference 0.8 mm corner radius. The three
        # crossbar strips are the actual stepped rib profile inset by the
        # reference 1.5 mm border. Reinforcement cylinders are joined after
        # this cut, which preserves their Ø14 footprints at the nominal rear
        # mounting plane just like rear_recess_2d() in the OpenSCAD source.
        side_margin = (self.width / 160.0) * REAR_SIDE_RECESS_MARGIN
        end_margin = (self.height / 320.0) * REAR_END_RECESS_MARGIN
        cross_margin = (
            (self.height / 320.0) * REAR_CROSSBAR_RECESS_MARGIN
        )
        recess_radius = (
            (self.width / 160.0) * REAR_RECESS_CORNER_RADIUS
        )

        side_recess_width = (
            side - self.rear_inset - 2 * side_margin
        )
        side_recess_height = self.height - 2 * end
        left_side_center = (
            -half(self.width)
            + self.rear_inset
            + side_margin
            + half(side_recess_width)
        )
        right_side_center = (
            half(self.width)
            - self.rear_inset
            - side_margin
            - half(side_recess_width)
        )

        end_recess_width = opening_width
        end_recess_height = (
            end - self.rear_inset - 2 * end_margin
        )
        bottom_end_center = (
            -half(self.height)
            + self.rear_inset
            + end_margin
            + half(end_recess_height)
        )
        top_end_center = (
            half(self.height)
            - self.rear_inset
            - end_margin
            - half(end_recess_height)
        )

        # The OpenSCAD crossbar recess is offset(delta=-cross_margin) from the
        # real stepped rib. For the 45-degree transition, the intersections
        # with the inset horizontal edges move by m*(sqrt(2)-1).
        transition_inset = cross_margin * (sqrt(2) - 1)
        recess_left = left + cross_margin
        recess_right = right - cross_margin
        step_outer_left = -(
            step_depth + half_narrow + transition_inset
        )
        step_inner_left = -(transition_inset + half_narrow)
        step_inner_right = transition_inset + half_narrow
        step_outer_right = (
            step_depth + half_narrow + transition_inset
        )

        with Sketch(
            name="Rear rail recesses",
            on=body,
            parent=Anchor.TOP,
        ) as recess:
            recess.add(
                RoundedRectangle2D(
                    side_recess_width,
                    side_recess_height,
                    recess_radius,
                ),
                offset=(left_side_center, 0),
            )
            recess.add(
                RoundedRectangle2D(
                    side_recess_width,
                    side_recess_height,
                    recess_radius,
                ),
                offset=(right_side_center, 0),
            )
            recess.add(
                RoundedRectangle2D(
                    end_recess_width,
                    end_recess_height,
                    recess_radius,
                ),
                offset=(0, bottom_end_center),
            )
            recess.add(
                RoundedRectangle2D(
                    end_recess_width,
                    end_recess_height,
                    recess_radius,
                ),
                offset=(0, top_end_center),
            )

            for index, center in enumerate(
                (
                    -quarter_height,
                    self.height * 0,
                    quarter_height,
                ),
                start=1,
            ):
                outer_bottom = center - rib_half + cross_margin
                inner_bottom = (
                    center - rib_half + step_depth + cross_margin
                )
                outer_top = center + rib_half - cross_margin
                inner_top = (
                    center + rib_half - step_depth - cross_margin
                )
                Polygon2D(
                    [
                        (recess_left, outer_bottom),
                        (step_outer_left, outer_bottom),
                        (step_inner_left, inner_bottom),
                        (step_inner_right, inner_bottom),
                        (step_outer_right, outer_bottom),
                        (recess_right, outer_bottom),
                        (recess_right, outer_top),
                        (step_outer_right, outer_top),
                        (step_inner_right, inner_top),
                        (step_inner_left, inner_top),
                        (step_outer_left, outer_top),
                        (recess_left, outer_top),
                    ],
                    ids=tuple(
                        f"r{index}_{segment}"
                        for segment in range(1, 13)
                    ),
                )

        body = body - recess.extrude(-REAR_RECESS_DEPTH)

        # Restore the mechanically relevant rear mounting interfaces from
        # the existing v1.2 OpenSCAD/STEP/PDF reference. The surrounding rail
        # gets a shallow circular relief first; the true Ø8.5 tube is then
        # joined back so its rear outline remains visibly circular.
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

                tube = Cylinder(
                    d=MOUNTING_TUBE_OUTER_DIAMETER,
                    h=(
                        self.depth
                        + MOUNTING_TUBE_PROTRUSION
                        - self.front_depth
                    ),
                    anchor=Anchor.BOTTOM,
                ).at(x, y, self.front_depth, anchor=Anchor.BOTTOM)
                body = body + tube

        # The six reinforcement features are separate from the mounting tubes.
        # Their source offset is asymmetric at the middle pair in portrait
        # orientation: left-middle is +11 mm, right-middle is -11 mm.
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
            reinforcement = Cylinder(
                d=REINFORCEMENT_OUTER_DIAMETER,
                h=reinforcement_depth,
                anchor=Anchor.BOTTOM,
            ).at(
                x,
                y,
                self.depth - reinforcement_depth,
                anchor=Anchor.BOTTOM,
            )
            body = body + reinforcement
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

        # PDF-dimensioned diagonal locator pair. In the centred portrait local
        # axes these are upper-left (-75,+110) and lower-right (+75,-110).
        for x, y in (
            (-LOCATOR_PIN_X, LOCATOR_PIN_Y),
            (LOCATOR_PIN_X, -LOCATOR_PIN_Y),
        ):
            pin = Cylinder(
                d=LOCATOR_PIN_DIAMETER,
                h=LOCATOR_PIN_PROTRUSION,
                anchor=Anchor.BOTTOM,
            ).at(x, y, self.depth, anchor=Anchor.BOTTOM)
            body = body + pin

        # Keep the six Ø3 mounting bores open through the new 0.5 mm tube
        # protrusion while still stopping at the rear-housing start Z=2 mm.
        rear_bore_start = self.depth + MOUNTING_TUBE_PROTRUSION
        rear_bore_depth = rear_bore_start - self.front_depth
        for x in (-self.mount_x, self.mount_x):
            for y in (-self.mount_y, 0, self.mount_y):
                body = body + Hole(
                    d=self.hole_diameter,
                    depth=rear_bore_depth,
                    direction=(0, 0, -1),
                ).at(x, y, rear_bore_start)

        # One gray housing material. Detailed PCB/front/connector colors
        # require separate native bodies in a later panel-model iteration.
        return body.with_material(
            "HUB75 housing", density_g_cm3=1.20, color="#B8B8B8"
        )

