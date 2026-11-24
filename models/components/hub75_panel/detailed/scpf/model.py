"""Single measured HUB75 panel reused in the regression and screen assembly.

Authoritative reference: lib.scad.hub75 / HUB75 frame project v1.2.
The current CAD body is still an approximate rear-tapered envelope with
four rear electronics-bay pockets and six blind mounting bores. The pocket
outlines are currently square-cornered approximations; the rounded/stepped
bay edges, tubes, PCB and connectors still need distinct features.
"""
from scpf import Box, Cylinder, Hole, Sketch, Rectangle2D, Anchor, component, half, midpoint


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
        # front mask + PCB stack at Z=0..2 mm. On the source panel the four
        # openings are separated by 3 crossbars, 20 mm wide in reference
        # coordinates. A single named sketch creates one editable cut.
        #
        # OpenSCAD source coordinates use X/Z in the display face; SCPF uses
        # X/Y. The reference's 80/160/240 mm rib positions therefore become
        # Y=-H/4, Y=0 and Y=+H/4 in portrait orientation.
        side = self.rear_side_rail * (159.70 / 160.0)
        end = self.rear_end_rail * (319.71 / 320.0)
        rib_half = half(self.rear_crossbar * (319.71 / 320.0))
        half_height = half(self.height)
        quarter_height = self.height / 4
        opening_width = self.width - 2 * side
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
                bays.add(
                    Rectangle2D(opening_width, top - bottom),
                    offset=(0, midpoint(bottom, top)),
                )
        body = body - bays.extrude(-(self.depth - self.front_depth))

        # These four rectangles create the real rails and 3 dividing ribs.
        # Pending STEP details: 5 mm rounded corners, the stepped 7.75 mm
        # central rail relief, shallow rear recess and reinforcement tubes.
        # In particular this is not yet a complete molded HUB75 rear shell.

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

