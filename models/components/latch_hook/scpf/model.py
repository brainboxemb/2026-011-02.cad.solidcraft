"""Native sheet-metal latch hook reconstructed from the supplied drawing.

The model is authored as one flat 2 mm sheet blank with two mounting holes,
followed by one native sheet fold.  No fused-solid approximation is used.

Source drawing constraints:
- sheet thickness: 2 mm
- formed projection: 20 mm
- free hook tip X: 13.5 mm
- formed overall height: 10.5 mm
- inside bend radius: 2.1 mm
- mounting width: 24 mm
- neck width: 15 mm
- hole diameter: 4.3 mm
- hole pitch: 14 mm
- hole centre datum: 5 mm from the left edge

The outer mounting-lobe contour is resolved by tangency from the dimensioned
24 mm overall width, 14 mm pitch and 5 mm left-edge hole datum.
"""

from scpf import Hole, Sketch, component


@component(include="*")
class LatchHook:
    thickness = 2.0
    bend_radius = 2.1
    k_factor = 0.40

    overall_width = 24.0
    neck_width = 15.0
    hole_diameter = 4.3
    hole_pitch = 14.0
    hole_x = 5.0

    formed_projection = 20.0
    hook_tip_x = 13.5
    formed_height = 10.5

    # Derived from the formed side profile.  With 2 mm material and R2.1,
    # the outside bend radius is 4.1 mm, so the bend centreline sits at
    # X = 20 - 4.1 = 15.9 mm.  Tangency from that outside-radius circle to
    # the dimensioned free tip (13.5, 10.5) yields 147.414°.
    _fold_x = 15.9
    _fold_angle = 147.414
    _blank_end_x = 25.10

    def build(self):
        lobe_radius = 5.0
        half_pitch = self.hole_pitch / 2
        half_neck = self.neck_width / 2
        top_y = self.overall_width / 2
        bottom_y = -top_y

        with Sketch(name="Latch hook blank", plane="XY") as blank:
            contour = blank.profile(start=(self.hole_x, top_y))
            contour.line_to((self._fold_x, half_neck))
            contour.line_to((self._blank_end_x, half_neck))
            contour.line_to((self._blank_end_x, -half_neck))
            contour.line_to((self._fold_x, -half_neck))
            contour.line_to((self.hole_x, bottom_y))
            contour.arc_center_to(
                (0.0, -half_pitch),
                center=(self.hole_x, -half_pitch),
                clockwise=True,
            )
            contour.line_to((0.0, half_pitch))
            contour.arc_center_to(
                (self.hole_x, top_y),
                center=(self.hole_x, half_pitch),
                clockwise=True,
            )
            contour.close()

        hook = blank.sheet_metal(
            thickness=self.thickness,
            bend_radius=self.bend_radius,
            k_factor=self.k_factor,
            rule_name="Latch hook 2 mm",
        )

        for y in (-half_pitch, half_pitch):
            hook = hook + Hole(
                d=self.hole_diameter,
                direction=(0, 0, -1),
            ).at(self.hole_x, y, self.thickness)

        hook = hook.fold(
            line=((self._fold_x, -half_neck), (self._fold_x, half_neck)),
            angle=self._fold_angle,
            fixed=(self.hole_x, 0, 0),
            position="centerline",
        )

        return hook.with_material(
            "Galvanized steel",
            density_g_cm3=7.85,
            color="#B7BDC2",
        )


LatchHook()
