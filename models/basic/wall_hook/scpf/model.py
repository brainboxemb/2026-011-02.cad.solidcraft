"""Wall hook reconstructed from the supplied tutorial sketch.

Confirmed source dimensions are public model parameters. The visible corner
radii are not dimensioned in the supplied screenshots, so they remain isolated
as explicit provisional parameters.
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

    # Inferred from the rendered tutorial result; keep easy to revise.
    profile_fillet = 2.0
    window_fillet = 2.0

    def build(self):
        crossbar_y = self.overall_height - self.opening_depth
        right_inner_x = self.rib + self.opening_width
        right_outer_x = right_inner_x + self.rib
        right_top_y = crossbar_y + self.short_tip_rise
        right_outer_bottom_y = right_top_y - self.short_outer_height

        # The outside diagonal is exactly 45 degrees:
        # (6, 0) -> (32, 26). The inner diagonal keeps a true 6 mm normal web.
        window_top_y = crossbar_y - self.rib
        window_left_bottom_y = self.rib * sqrt(2.0)
        window_right_top_x = window_top_y - (
            -self.rib + self.rib * sqrt(2.0)
        )

        # Build the visible R2 silhouette directly in 2D. This avoids a
        # post-extrusion fillet feature while preserving true circular arcs.
        r = self.profile_fillet
        r45_offset = r * (sqrt(2.0) - 1.0)
        r45_diag = r45_offset / sqrt(2.0)

        start = (r, 0.0)
        with Sketch(name="Rounded bracket outline", plane="XY") as outline:
            profile = outline.profile(start=start)

            # Bottom-left -> lower 45-degree outside corner.
            profile.line_to((self.rib - r45_offset, 0.0))
            profile.arc_center_to(
                (
                    self.rib + r45_diag,
                    r45_diag,
                ),
                center=(self.rib - r45_offset, r),
                clockwise=False,
            )

            # Lower diagonal -> right vertical.
            profile.line_to(
                (
                    right_outer_x - r45_diag,
                    right_outer_bottom_y - r45_diag,
                )
            )
            profile.arc_center_to(
                (
                    right_outer_x,
                    right_outer_bottom_y + r45_offset,
                ),
                center=(
                    right_outer_x - r,
                    right_outer_bottom_y + r45_offset,
                ),
                clockwise=False,
            )

            # Outer top of the short hook tip.
            profile.line_to((right_outer_x, right_top_y - r))
            profile.arc_center_to(
                (right_outer_x - r, right_top_y),
                center=(right_outer_x - r, right_top_y - r),
                clockwise=False,
            )
            profile.line_to((right_inner_x + r, right_top_y))
            profile.arc_center_to(
                (right_inner_x, right_top_y - r),
                center=(right_inner_x + r, right_top_y - r),
                clockwise=False,
            )

            # Concave bottom corners of the U opening.
            profile.line_to((right_inner_x, crossbar_y + r))
            profile.arc_center_to(
                (right_inner_x - r, crossbar_y),
                center=(right_inner_x - r, crossbar_y + r),
                clockwise=True,
            )
            profile.line_to((self.rib + r, crossbar_y))
            profile.arc_center_to(
                (self.rib, crossbar_y + r),
                center=(self.rib + r, crossbar_y + r),
                clockwise=True,
            )

            # Tall hook arm top and outside spine.
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

        body = outline.extrude(self.thickness)

        # Rounded triangular relief. Its two acute corners are 45 degrees,
        # so their tangent distance is R / tan(22.5°) = R * (sqrt(2) + 1).
        wr = self.window_fillet
        acute_tangent = wr * (sqrt(2.0) + 1.0)
        acute_diag = acute_tangent / sqrt(2.0)

        window_left = self.rib
        window_bottom = window_left_bottom_y
        window_top = window_top_y
        window_right = window_right_top_x

        window_start = (
            window_left + acute_diag,
            window_bottom + acute_diag,
        )
        with Sketch(name="Rounded triangular gusset window", plane="XY") as window:
            relief = window.profile(start=window_start)

            # Acute lower-left corner -> 90-degree top-left corner.
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

            # Top edge -> acute upper-right corner.
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

        body = body - window.extrude(self.thickness)

        hole_x = self.rib / 2.0
        countersink_d = self.hole_diameter + 2.0 * self.hole_chamfer
        hole_ys = (
            self.overall_height - self.upper_hole_from_top,
            self.lower_hole_from_bottom,
        )

        # A 90-degree countersink with +1 mm radial opening gives the requested
        # 1 mm chamfer. Apply it from both 15 mm broad faces.
        for y in hole_ys:
            body = body + CountersinkHole(
                d=self.hole_diameter,
                countersink_d=countersink_d,
                countersink_angle=90,
                direction=(0, 0, -1),
            ).at(hole_x, y, self.thickness)

            body = body + CountersinkHole(
                d=self.hole_diameter,
                countersink_d=countersink_d,
                countersink_angle=90,
                direction=(0, 0, 1),
            ).at(hole_x, y, 0.0)

        return body


WallHook()
