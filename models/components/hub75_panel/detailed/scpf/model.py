"""Single measured HUB75 panel reused in the regression and screen assembly.

Authoritative reference: lib.scad.hub75 / HUB75 frame project v1.2.
The current CAD body is still an approximate rear-tapered envelope with
four rear electronics-bay pockets and six blind mounting bores. The pocket
outlines are currently square-cornered approximations; the rounded/stepped
bay edges, tubes, PCB and connectors still need distinct features.
"""
from scpf import Box, Hole, Sketch, Rectangle2D, Anchor, Direction, component


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
        body = Box(self.width, self.height, self.depth).taper(
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
        rib_half = self.rear_crossbar * (319.71 / 320.0) / 2
        half_height = self.height / 2
        quarter_height = self.height / 4
        opening_width = self.width - 2 * side
        left = -self.width / 2 + side
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
                    offset=(left, bottom),
                )
        body = body - bays.extrude(
            self.depth - self.front_depth,
            direction=Direction.NEGATIVE,
        )

        # These four rectangles create the real rails and 3 dividing ribs.
        # Pending STEP details: 5 mm rounded corners, the stepped 7.75 mm
        # central rail relief, shallow rear recess and reinforcement tubes.
        # In particular this is not yet a complete molded HUB75 rear shell.

        # The mounting bores are at the BACK of the mechanical housing.
        # Our first envelope model previously cut all the way through the
        # 2 mm front mask / PCB stack. The real panel must have a solid
        # front face: stop the six bores at the START of the rear housing,
        # Z=front_depth, without opening the front at Z=0.
        #
        # OpenSCAD builds separate mounting tubes and front layers. A blind
        # bore in the simplified single-body envelope preserves that
        # mechanical intent without inventing the missing rear structure.
        rear_bore_depth = self.depth - self.front_depth
        for x in (-self.mount_x, self.mount_x):
            for y in (-self.mount_y, 0, self.mount_y):
                body = body + Hole(
                    d=self.hole_diameter,
                    depth=rear_bore_depth,
                    direction=(0, 0, -1),
                ).at(x, y, self.depth)

        # One gray housing material. Detailed PCB/front/connector colors
        # require separate native bodies in a later panel-model iteration.
        return body.with_material(
            "HUB75 housing", density_g_cm3=1.20, color="#B8B8B8"
        )

