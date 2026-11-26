"""Wall hook reconstructed from the supplied tutorial sketch.

Confirmed source dimensions are public model parameters. The side profile is
authored as sharp polygons in world XZ, extruded symmetrically in Y, then
rounded with native SolidCraft fillet operations.
"""

from math import sqrt


@component
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
    front_hole_chamfer = 1.0
    rear_hole_relief = 0.3
    tool_access_diameter = 8.0

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

        # The outside reinforcement edge is exactly 45 degrees:
        # (6, 0) -> (32, 26). Offset its inner edge by a true 6 mm normal web.
        diagonal_offset = self.rib * sqrt(2.0)
        window_top_z = crossbar_z - self.rib
        window_left_bottom_z = diagonal_offset
        window_right_top_x = window_top_z - (diagonal_offset - self.rib)

        # Start with the simple sharp-cornered side silhouette. The vertex ids
        # become native sweep-edge selectors after the symmetric Y extrusion.
        with Sketch(name="Sharp hook side profile", plane="XZ") as outline:
            Polygon2D(
                [
                    ("back_lower", (0.0, 0.0)),
                    ("diagonal_lower", (self.rib, 0.0)),
                    ("diagonal_upper", (right_outer_x, right_outer_bottom_z)),
                    ("outer_tip_upper", (right_outer_x, right_top_z)),
                    ("inner_tip_upper", (right_inner_x, right_top_z)),
                    ("inner_tip_lower", (right_inner_x, crossbar_z)),
                    ("inner_back_corner", (self.rib, crossbar_z)),
                    ("back_upper_inner", (self.rib, self.overall_height)),
                    ("back_upper_outer", (0.0, self.overall_height)),
                ],
                plane="XZ",
                world=True,
            )

        body = outline.extrude(self.thickness, sym=True)
        body = body.fillet(
            self.profile_fillet,
            edges=Edges.from_vertices(
                "back_lower",
                "diagonal_lower",
                "diagonal_upper",
                "outer_tip_upper",
                "inner_tip_upper",
                "inner_tip_lower",
                "inner_back_corner",
                "back_upper_inner",
                "back_upper_outer",
            ),
        )

        # Build the reinforcement opening as a plain triangle first. Subtract
        # the sharp cutter, then fillet the three resulting inner sweep edges
        # on the hook body itself.
        with Sketch(name="Sharp triangular gusset window", plane="XZ") as window:
            Polygon2D(
                [
                    ("window_lower", (self.rib, window_left_bottom_z)),
                    ("window_front", (window_right_top_x, window_top_z)),
                    ("window_upper", (self.rib, window_top_z)),
                ],
                plane="XZ",
                world=True,
            )

        body = body - window.extrude(self.thickness, sym=True)
        body = body.fillet(
            self.window_fillet,
            edges=[
                (self.rib, 0.0, window_left_bottom_z),
                (window_right_top_x, 0.0, window_top_z),
                (self.rib, 0.0, window_top_z),
            ],
        )

        # Keep the lower Ø4.2 mounting hole confined to the 6 mm rear spine,
        # but clear the diagonal reinforcement in front of it so a screwdriver
        # or bit can reach the screw head along the same world-X axis.
        body = body - Cylinder(
            d=self.tool_access_diameter,
            h=right_outer_x - self.rib,
            axis=Axis.X,
            anchor=Anchor.LEFT,
        ).at(
            self.rib,
            0.0,
            self.lower_hole_from_bottom,
            anchor=Anchor.LEFT,
        )

        # Chamfer the complete native boundary of both broad XZ end faces before
        # the mounting holes so their own countersink/chamfer remains independent.
        body = body.chamfer(
            self.face_chamfer,
            edges=Edges.from_faces(Faces.FRONT, Faces.BACK),
        )

        front_countersink_d = (
            self.hole_diameter + 2.0 * self.front_hole_chamfer
        )
        rear_relief_d = self.hole_diameter + 2.0 * self.rear_hole_relief
        hole_zs = (
            self.overall_height - self.upper_hole_from_top,
            self.lower_hole_from_bottom,
        )

        # Rear mounting spine is 6 mm thick along X. The 15 mm extrusion is
        # centred on Y=0, so both screw-hole axes sit at Y=0 and run along X.
        # The tool/front face at X=6 keeps the normal screw-entry countersink.
        # The wall-contact face at X=0 only gets a tiny elephant-foot relief.
        for z in hole_zs:
            body = body + CountersinkHole(
                d=self.hole_diameter,
                countersink_d=front_countersink_d,
                countersink_angle=90,
                depth=self.rib,
                direction=(-1, 0, 0),
            ).at(self.rib, 0.0, z)

            body = body + CountersinkHole(
                d=self.hole_diameter,
                countersink_d=rear_relief_d,
                countersink_angle=90,
                depth=self.rib,
                direction=(1, 0, 0),
            ).at(0.0, 0.0, z)

        return body.with_appearance("#FFD21A")



def wall_hook_drawing():
    """A4 landscape manufacturing/mounting sheet for the finished Wall Hook."""
    hook = WallHook()
    return hook.with_drawing(
        name="Wall Hook Drawing",
        scale="2:1",
        gap_mm=12,
        views={
            "front": DrawingView(at=(55, 130)),
            "top": DrawingView(at=(55, 48)),
            "right": DrawingView(at=(142, 130)),
            "iso": DrawingView(
                at=(225, 132),
                scale="1:1",
                visual_style="shaded",
            ),
        },
        properties={
            "project": "SolidCraft CAD model catalog",
            "part_number": "wall-hook",
            "revision": "A",
            "author": "brainboxemb",
            "organization": "brainboxemb",
            "description": "Wall Hook technical drawing",
        },
        title_block={
            "title": "Wall Hook",
            "identification_number": "wall-hook",
            "document_status": "Development",
            "department": "CAD",
        },
        revision=DrawingRevision(
            revision="A",
            description="Initial technical drawing",
            designer="brainboxemb",
            checker="CI",
            date="2026-11-26",
        ),
        notes=(
            DrawingNote(
                "NOTES\n"
                "1. ALL DIMENSIONS IN MM.\n"
                "2. MOUNTING HOLE CENTRES: UPPER 10 FROM TOP; LOWER 17 FROM BOTTOM.\n"
                "3. 2× Ø4.2 MOUNTING HOLES; LOWER TOOL ACCESS Ø8.\n"
                "4. FRONT/BACK BOUNDARY CHAMFER 1.5.\n"
                "5. HOLE ENTRY CHAMFER 1.0; WALL-SIDE RELIEF 0.3.",
                at=(174, 58),
                cap_mm=2.2,
            ),
        ),
        dimensions=(
            DrawingDimension.faces(
                "front",
                (3, 0, 0),
                (3, 0, 57),
                direction="vertical",
                offset_mm=12,
                decimals=0,
            ),
            DrawingDimension.faces(
                "top",
                (3, -7.5, 47),
                (3, 7.5, 47),
                direction="vertical",
                offset_mm=10,
                decimals=0,
            ),
            DrawingDimension.faces(
                "front",
                (0, 0, 40),
                (6, 0, 40),
                direction="horizontal",
                offset_mm=8,
                decimals=0,
            ),
            DrawingDimension.faces(
                "front",
                (6, 0, 37),
                (26, 0, 37),
                direction="horizontal",
                offset_mm=8,
                decimals=0,
            ),
            DrawingDimension.faces(
                "front",
                (16, 0, 32),
                (3, 0, 57),
                direction="vertical",
                offset_mm=8,
                decimals=0,
            ),
            DrawingDimension.radial(
                "right",
                (5, 2.1, 47),
                diameter=True,
                override_text="2× Ø{value} THRU",
                line_through_mm=(176, 166),
                decimals=1,
            ),
            DrawingDimension.radial(
                "right",
                (6, 4, 17),
                diameter=True,
                override_text="Ø{value} TOOL ACCESS",
                line_through_mm=(176, 96),
                decimals=0,
            ),
        ),
    )


wall_hook_drawing()
