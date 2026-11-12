"""One shared, editable CornerBracket shape WITHOUT screw holes.

The standalone demonstration and wooden HUB75 assembly import this single
geometry definition. While the screw-hole operations are producing native
SolidCraft warnings, keep the bracket as a clean L-shaped body with the
reviewed inner fillet and outer/elephant-foot chamfers. Historical hole
experiments remain only in the standalone model_reference.py, not here.
"""
from scpf import Polygon2D, Direction, Edges

class CornerBracket:
    bracket_width = 24.0
    wall_thickness = 12.0
    horizontal_arm_length = 60.0
    vertical_arm_length = 60.0

    outer_corner_chamfer = 6.0
    arm_end_chamfer = 3.0
    side_edge_chamfer = 2.0
    elephant_foot_relief = 0.6
    inside_corner_radius = 4.0
    z_position = 0.0

    def build(self):
        w = self.wall_thickness
        h = self.horizontal_arm_length
        v = self.vertical_arm_length
        end = self.arm_end_chamfer
        outer = self.outer_corner_chamfer
        ef = self.elephant_foot_relief
        z = getattr(self, "z_position", 0.0)

        # L profile in the XZ plane (+Z up, +X right; not to scale):
        #
        #       D--------------------------------C
        #      /                                  \
        #     E                                    B
        #     |                                    |
        #     |         I--------------------------A
        #     |         |
        #     |         |
        #     F         |
        #      \        |
        #       G-------H
        #
        # A o_hor_tip    B o_hor_bevel  C o_hor
        # D o_corner     E o_vert       F o_vert_bevel
        # G o_vert_end   H v_tip        I i_corner
        #
        # Start at I, the inside corner and sketch origin (0, 0).
        # Polygon order: I -> A -> B -> C -> D -> E -> F -> G -> H -> I.
        # Each label names its point and the segment starting at that point.
        # Elephant-foot relief is NOT part of this sketch: it comes later.
        profile = Polygon2D([
            ("i_corner", (0, z)),
            ("o_hor_tip", (h, z)),
            ("o_hor_bevel", (h, z + w - end)),
            ("o_hor", (h - end, z + w)),
            ("o_corner", (-w + outer, z + w)),
            ("o_vert", (-w, z + w - outer)),
            ("o_vert_bevel", (-w, z - v + end)),
            ("o_vert_end", (-w + end, z - v)),
            ("v_tip", (0, z - v)),
        ], plane="XZ", world=True)

        body = profile.extrude(self.bracket_width, direction=Direction.SYMMETRIC)

        # Round the inside, then remove printing relief from the two tip
        # edges (parallel to the extrusion direction).
        body = body.fillet(
            self.inside_corner_radius,
            edges=Edges.from_vertices("i_corner"),
        )
        body = body.chamfer(
            self.elephant_foot_relief,
            edges=Edges.from_vertices("o_hor_tip", "v_tip"),
        )
        body = body.chamfer(
            self.side_edge_chamfer,
            edges=Edges.from_profile("o_*", sides="both"),
        )
        # Inner relief along both broad faces, independent of the 2D outline.
        body = body.chamfer(
            self.elephant_foot_relief,
            edges=Edges.from_profile("i_corner", sides="both"),
        )

        # No mounting holes in this version. The historical four-hole
        # geometry caused warnings in native SolidCraft when replayed
        # inside the larger wooden frame. Keep this bracket reliable as a
        # positioned/rounded solid while the mounting approach is reviewed.
        # Do not reintroduce holes through model-specific workarounds.

        return body


