"""Shared CornerBracket with the preserved OpenSCAD fixing geometry.

The standalone component and wooden HUB75 assemblies import this exact class.
The 2D XZ profile carries the 0.6 mm arm-tip print relief, while native
SolidCraft features add the inside R4 fillet, broad-face chamfers and four
recessed M5 clearance seats.
"""
from scpf import CountersinkHole, Edges, Hole, Polygon2D, Sketch, component


@component
class CornerBracket:
    arm_width = 24.0
    arm_height = 12.0
    horizontal_arm_length = 60.0
    vertical_arm_length = 60.0

    outer_corner_chamfer = 6.0
    arm_end_chamfer = 3.0
    side_edge_chamfer = 2.0
    elephant_foot_relief = 0.6
    inside_corner_radius = 4.0

    plywood_thickness = 12.0
    bolt_offset = 12.0
    bolt_spacing = 18.0
    bolt_y_offset = 0.0
    bolt_diameter = 5.0
    bolt_clearance = 0.4
    head_diameter = 10.0
    head_clearance = 0.4
    head_recess = 1.0
    bolt_hole_edge_relief = 0.2

    def _bolt_seat(
        self,
        body,
        *,
        outside,
        direction,
        countersink_entry,
        inside,
        inside_direction,
    ):
        """Apply one preserved flat-bottom screw-head seat as native features."""
        through_d = self.bolt_diameter + self.bolt_clearance
        head_d = self.head_diameter + self.head_clearance
        wall_depth = self.arm_height - self.head_recess

        # The OpenSCAD reference intentionally separates these operations.
        # Do not replace them with one oversized countersink: the first 1 mm is
        # cylindrical, then a 90-degree cone transitions to the through bore.
        body = body + Hole(
            d=head_d,
            depth=self.head_recess,
            direction=direction,
        ).at(*outside)

        body = body + CountersinkHole(
            d=through_d,
            countersink_d=head_d,
            countersink_angle=90,
            depth=wall_depth,
            direction=direction,
        ).at(*countersink_entry)

        # Shallow flat edge reliefs are separate from the head seat itself.
        body = body + Hole(
            d=head_d + 2 * self.bolt_hole_edge_relief,
            depth=self.bolt_hole_edge_relief,
            direction=direction,
        ).at(*outside)
        body = body + Hole(
            d=through_d + 2 * self.bolt_hole_edge_relief,
            depth=self.bolt_hole_edge_relief,
            direction=inside_direction,
        ).at(*inside)
        return body

    def build(self):
        w = self.arm_height
        h = self.horizontal_arm_length
        v = self.vertical_arm_length
        end = self.arm_end_chamfer
        outer = self.outer_corner_chamfer
        ef = self.elephant_foot_relief

        # Preserve the OpenSCAD base_profile_2d() topology. The two 0.6 mm tip
        # reliefs belong in this profile; a sweep-edge chamfer across the whole
        # 24 mm width is not geometrically equivalent.
        points = [
            ("i_corner", (0, 0)),
            ("tip_hor_relief", (h - ef, 0)),
            ("o_hor_tip", (h, ef)),
            ("o_hor_bevel", (h, w - end)),
            ("o_hor", (h - end, w)),
            ("o_corner", (-w + outer, w)),
            ("o_vert", (-w, w - outer)),
            ("o_vert_bevel", (-w, -v + end)),
            ("o_vert_end", (-w + end, -v)),
            ("tip_vert_relief", (-ef, -v)),
            ("v_tip", (0, -v + ef)),
        ]

        with Sketch(name="Profile", plane="XZ") as sketch:
            Polygon2D(points, plane="XZ", world=True)

        body = sketch.extrude(self.arm_width, sym=True)

        body = body.fillet(
            self.inside_corner_radius,
            edges=Edges.from_vertices("i_corner"),
        )
        # The two tiny tip-relief diagonals deliberately use `tip_*` names,
        # not `o_*`: including them in the 2 mm side chamfer makes the native
        # blend rails overrun those 0.6 mm faces. OpenSCAD treats that local
        # junction separately in arm_tip_relief_cuts().
        #
        # TEMPORARY compatibility workaround — CAD #362 / Forge #750.
        # The preserved OpenSCAD geometry also subtracts a small locally rotated
        # triangular-prism wedge at each arm tip. Released Forge v0.11 cannot
        # express that standalone 45-degree cutter generically, so the tip_*
        # segments stay excluded here until Forge #750 is released and adopted.
        body = body.chamfer(
            self.side_edge_chamfer,
            edges=Edges.from_profile("o_*", sides="both"),
        )
        # Broad-face elephant-foot relief starts on the inside horizontal edge;
        # SolidCraft's tangent propagation carries it around the R4 corner.
        body = body.chamfer(
            self.elephant_foot_relief,
            edges=Edges.from_profile("i_corner", sides="both"),
        )

        first = self.plywood_thickness + self.bolt_offset
        second = first + self.bolt_spacing
        y = self.bolt_y_offset

        for x in (first, second):
            body = self._bolt_seat(
                body,
                outside=(x, y, w),
                direction=(0, 0, -1),
                countersink_entry=(x, y, w - self.head_recess),
                inside=(x, y, 0),
                inside_direction=(0, 0, 1),
            )

        for z in (-first, -second):
            body = self._bolt_seat(
                body,
                outside=(-w, y, z),
                direction=(1, 0, 0),
                countersink_entry=(-w + self.head_recess, y, z),
                inside=(0, y, z),
                inside_direction=(-1, 0, 0),
            )

        return body
