"""Wall hook reconstructed from the supplied tutorial sketch.

Confirmed source dimensions are public model parameters. The side profile is
authored in world XZ and extruded symmetrically in Y so the broad side faces
are Forge/SolidCraft FRONT and BACK.
"""

from math import sqrt


class WallHook:
    overall_height = 57.0
    thickness = 15.0
    rib = 6.0
    opening_width = 20.0
    opening_depth = 25.0
    short_tip_rise = 10.0
    short_outer_height = 16.0

    hole_diameter = 4.2
    upper_hole_from_top = 10.0
    lower_hole_from_bottom = 17.0
    hole_chamfer = 1.0

    face_chamfer = 1.5

    # Inferred from the rendered tutorial result; keep easy to revise.
    profile_fillet = 2.0
    window_fillet = 2.0

    def build(self):
        crossbar_z = self.overall_height - self.opening_depth
        right_inner_x = self.rib + self.opening_width
        right_outer_x = right_inner_x + self.rib
        right_top_z = crossbar_z + self.short_tip_rise
        right_outer_bottom_z = right_top_z - self.short_outer_height

        # The outside diagonal is exactly 45 degrees:
        # (6, 0) -> (32, 26). The inner diagonal keeps a true 6 mm normal web.
        window_top_z = crossbar_z - self.rib
        window_left_bottom_z = self.rib * sqrt(2.0)
        window_right_top_x = window_top_z - (
            -self.rib + self.rib * sqrt(2.0)
        )

        # Build the visible R2 side silhouette directly in XZ with true arcs.
        r = self.profile_fillet
        r45_offset = r * (sqrt(2.0) - 1.0)
        r45_diag = r45_offset / sqrt(2.0)

        start = (r, 0.0)
        with Sketch(name="Rounded hook side profile", plane="XZ", origin=(0, 0, 0)) as outline:
            profile = outline.profile(start=start)

            profile.line_to((self.rib - r45_offset, 0.0))
            profile.arc_center_to(
                (self.rib + r45_diag, r45_diag),
                center=(self.rib - r45_offset, r),
                clockwise=False,
            )

            profile.line_to(
                (
                    right_outer_x - r45_diag,
                    right_outer_bottom_z - r45_diag,
                )
            )
            profile.arc_center_to(
                (
                    right_outer_x,
                    right_outer_bottom_z + r45_offset,
                ),
                center=(
                    right_outer_x - r,
                    right_outer_bottom_z + r45_offset,
                ),
                clockwise=False,
            )

            profile.line_to((right_outer_x, right_top_z - r))
            profile.arc_center_to(
                (right_outer_x - r, right_top_z),
                center=(right_outer_x - r, right_top_z - r),
                clockwise=False,
            )
            profile.line_to((right_inner_x + r, right_top_z))
            profile.arc_center_to(
                (right_inner_x, right_top_z - r),
                center=(right_inner_x + r, right_top_z - r),
                clockwise=False,
            )

            profile.line_to((right_inner_x, crossbar_z + r))
            profile.arc_center_to(
                (right_inner_x - r, crossbar_z),
                center=(right_inner_x - r, crossbar_z + r),
                clockwise=True,
            )
            profile.line_to((self.rib + r, crossbar_z))
            profile.arc_center_to(
                (self.rib, crossbar_z + r),
                center=(self.rib + r, crossbar_z + r),
                clockwise=True,
            )

            profile.line_to((self.rib, self.overall_height - r))
            profile.arc_center_to(
                (self.rib - r, self.overall_height),
                center=(self.rib - r, self.overall_height - r),
                clockwise=False,
            )
            profile.line_to((r, self.overall_height))
            profile.arc_center_to(
                (0.0, self.overall_height - r),
                center=(r, self.overall_height - r),
                clockwise=False,
            )
            profile.line_to((0.0, r))
            profile.arc_center_to(
                start,
                center=(r, r),
                clockwise=False,
            )
            profile.close()

        body = outline.extrude(self.thickness, sym=True)

        # Rounded triangular relief. Its two acute corners are 45 degrees,
        # so their tangent distance is R / tan(22.5°) = R * (sqrt(2) + 1).
        wr = self.window_fillet
        acute_tangent = wr * (sqrt(2.0) + 1.0)
        acute_diag = acute_tangent / sqrt(2.0)

        window_left = self.rib
        window_bottom = window_left_bottom_z
        window_top = window_top_z
        window_right = window_right_top_x

        window_start = (
            window_left + acute_diag,
            window_bottom + acute_diag,
        )
        with Sketch(name="Rounded triangular gusset window", plane="XZ", origin=(0, 0, 0)) as window:
            relief = window.profile(start=window_start)

            relief.arc_center_to(
                (
                    window_left,
                    window_bottom + acute_tangent,
                ),
                center=(
                    window_left + wr,
                    window_bottom + acute_tangent,
                ),
                clockwise=True,
            )
            relief.line_to((window_left, window_top - wr))
            relief.arc_center_to(
                (window_left + wr, window_top),
                center=(window_left + wr, window_top - wr),
                clockwise=True,
            )

            relief.line_to((window_right - acute_tangent, window_top))
            relief.arc_center_to(
                (
                    window_right - acute_diag,
                    window_top - acute_diag,
                ),
                center=(
                    window_right - acute_tangent,
                    window_top - wr,
                ),
                clockwise=True,
            )
            relief.line_to(window_start)
            relief.close()

        body = body - window.extrude(self.thickness, sym=True)

        # Forge v0.18 resolves the complete native boundary of both broad XZ
        # extrusion end faces. Apply this before the screw holes so their own
        # 1.0 mm countersink/chamfer remains independent.
        body = body.chamfer(
            self.face_chamfer,
            edges=Edges.from_faces(Faces.FRONT, Faces.BACK),
        )

        countersink_d = self.hole_diameter + 2.0 * self.hole_chamfer
        hole_zs = (
            self.overall_height - self.upper_hole_from_top,
            self.lower_hole_from_bottom,
        )

        # Rear mounting spine is 6 mm thick along X. The 15 mm extrusion is
        # centred on Y=0, so both screw-hole axes sit at Y=0 and run along X.
        for z in hole_zs:
            body = body + CountersinkHole(
                d=self.hole_diameter,
                countersink_d=countersink_d,
                countersink_angle=90,
                depth=self.rib,
                direction=(-1, 0, 0),
            ).at(self.rib, 0.0, z)

            body = body + CountersinkHole(
                d=self.hole_diameter,
                countersink_d=countersink_d,
                countersink_angle=90,
                depth=self.rib,
                direction=(1, 0, 0),
            ).at(0.0, 0.0, z)

        return body


WallHook()
