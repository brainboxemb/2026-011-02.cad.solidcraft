"""Single measured HUB75 panel reused in the regression and screen assembly.

Authoritative reference: lib.scad.hub75 / HUB75 frame project v1.2.
The current CAD body is still an approximate rear-tapered envelope with
rear-side blind mounting bores, not a complete PCB / connector / rear-rail construction.
"""
from scpf import Box, Hole


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

    def build(self):
        # Real long sloping sides from Z=2 to Z=14.5, not a short bevel.
        body = Box(self.width, self.height, self.depth).taper(
            from_z=self.front_depth, inset=self.rear_inset,
        )

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

