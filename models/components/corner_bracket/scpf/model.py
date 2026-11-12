"""One shared, editable CornerBracket shape WITHOUT screw holes.

The standalone demonstration and wooden HUB75 assembly import this single
geometry definition. While the screw-hole operations are producing native
SolidCraft warnings, keep the bracket as a clean L-shaped body with the
reviewed inner fillet and outer/elephant-foot chamfers. Historical hole
experiments remain only in the standalone reference.py, not here.
"""
from scpf import AnchorFrame, Polygon2D, Direction, Edges, pv, component


@component
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

    def anchors(self):
        """Mount frames that place the L-profile outside a matching wood corner.

        The neutral bracket origin is its concave inside corner. The frame
        corner we attach to is one material thickness inward from that origin
        in Z, so two alternating local origins cover the four clock positions.
        Front and rear use opposite face normals; their x directions encode
        the intended quarter-turn orientation.
        """
        w = pv(self.wall_thickness)
        return {
            "front_mount_a": AnchorFrame(
                origin=(0, 0, -w),
                z=(0, 1, 0),
                x=(0, 0, -1),
            ),
            "front_mount_b": AnchorFrame(
                origin=(w, 0, 0),
                z=(0, 1, 0),
                x=(0, 0, -1),
            ),
            "rear_mount_a": AnchorFrame(
                origin=(0, 0, -w),
                z=(0, -1, 0),
                x=(1, 0, 0),
            ),
            "rear_mount_b": AnchorFrame(
                origin=(w, 0, 0),
                z=(0, -1, 0),
                x=(1, 0, 0),
            ),
        }

    def build(self):
        w = self.wall_thickness
        h = self.horizontal_arm_length
        v = self.vertical_arm_length
        end = self.arm_end_chamfer
        outer = self.outer_corner_chamfer

        # One neutral local model in the XZ plane (+Z up, +X right).
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
        # I is always the component origin. Assemblies place and rotate
        # occurrences of this geometry; this model never knows where it is used.
        points = [
            ("i_corner", (0, 0)),
            ("o_hor_tip", (h, 0)),
            ("o_hor_bevel", (h, w - end)),
            ("o_hor", (h - end, w)),
            ("o_corner", (-w + outer, w)),
            ("o_vert", (-w, w - outer)),
            ("o_vert_bevel", (-w, -v + end)),
            ("o_vert_end", (-w + end, -v)),
            ("v_tip", (0, -v)),
        ]

        profile = Polygon2D(
            points,
            plane="XZ",
            world=True,
        )

        body = profile.extrude(
            self.bracket_width,
            direction=Direction.SYMMETRIC,
        )

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
        body = body.chamfer(
            self.elephant_foot_relief,
            edges=Edges.from_profile("i_corner", sides="both"),
        )

        # No mounting holes in this version. The historical four-hole
        # geometry caused warnings in native SolidCraft when replayed
        # inside the larger wooden frame. Keep this bracket reliable while
        # the mounting approach is reviewed.

        return body
