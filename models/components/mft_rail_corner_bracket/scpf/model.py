"""Printable MFT corner bracket for two perpendicular MountingRailM8 profiles.

Prototype coordinate contract:
- +X follows the first rail away from the corner;
- +Y follows the second rail away from the corner;
- Z=0 is the underside of the MFT worktop;
- the two rail back webs meet at X=0 / Y=0;
- rail C-openings remain outside the bracket.

The two arm-hole pairs intentionally use the existing MountingRailM8 round-hole
positions: 12.5 mm and 62.5 mm from each rail end. Other dimensions are
provisional until the physical MFT underside and desired fasteners are measured.
"""

from scpf import (
    BOTTOM,
    FRONT,
    LEFT,
    Box,
    CountersinkHole,
    Hole,
    Polygon2D,
    Sketch,
    component,
)

from models.components.mounting_rail_m8.scpf.model import MountingRailM8


@component(include="*")
class MFTRailCornerBracket:
    arm_length = 75.0
    wall_thickness = 5.0

    top_gusset_leg = 55.0
    top_gusset_thickness = 5.0
    bottom_gusset_leg = 55.0
    bottom_gusset_thickness = 5.0

    # The bracket is also a load-bearing foot. Both rail ends sit on this
    # plastic shoe instead of hanging beside the bracket.
    foot_thickness = 6.0
    # Exact native quarter-round support-foot corner from hoek_assembly.sc.
    corner_foot_radius = 18.0

    rail_bolt_diameter = 8.5
    rail_hole_first = 12.5
    rail_hole_second = 62.5

    mft_screw_diameter = 5.5
    mft_screw_head_diameter = 10.5
    mft_screw_x = 20.0
    mft_screw_y = 20.0

    def build(self):
        rail_height = MountingRailM8.PROFILE_WIDTH
        foot_thickness_value = float(self.foot_thickness.value)
        # Two vertical arms lie against the inner/back web of each rail.
        x_arm = Box(
            self.arm_length,
            self.wall_thickness,
            rail_height,
        ).at(
            self.arm_length / 2,
            0,
            -rail_height,
            anchor=FRONT + BOTTOM,
        )

        y_arm = Box(
            self.wall_thickness,
            self.arm_length,
            rail_height,
        ).at(
            0,
            self.arm_length / 2,
            -rail_height,
            anchor=LEFT + BOTTOM,
        )

        # Upper triangular plate is flush with the MFT underside at Z=0.
        with Sketch(
            name="Top MFT gusset",
            plane="XY",
            origin=(0, 0, -self.top_gusset_thickness),
        ) as top_sketch:
            Polygon2D(
                [
                    (0, 0),
                    (self.top_gusset_leg, 0),
                    (0, self.top_gusset_leg),
                ]
            )
        top_gusset = top_sketch.extrude(self.top_gusset_thickness)

        # A matching lower gusset carries corner/racking load between both arms.
        with Sketch(
            name="Bottom corner gusset",
            plane="XY",
            origin=(0, 0, -rail_height),
        ) as bottom_sketch:
            Polygon2D(
                [
                    (0, 0),
                    (self.bottom_gusset_leg, 0),
                    (0, self.bottom_gusset_leg),
                ]
            )
        bottom_gusset = bottom_sketch.extrude(self.bottom_gusset_thickness)

        # Support shoes below both rail ends. The rail profile is 18 mm deep,
        # so these strips cover the complete footprint beneath each profile.
        # Their top is exactly the rail-bottom plane at Z=-27.
        rail_depth = MountingRailM8.PROFILE_HEIGHT
        foot_z = -rail_height - foot_thickness_value

        arm_length_value = float(self.arm_length.value)

        with Sketch(
            name="X rail support foot",
            plane="XY",
            origin=(0, 0, foot_z),
        ) as x_foot_sketch:
            Polygon2D(
                [
                    (0, -rail_depth),
                    (arm_length_value, -rail_depth),
                    (arm_length_value, 0),
                    (0, 0),
                ]
            )
        x_foot = x_foot_sketch.extrude(self.foot_thickness)

        with Sketch(
            name="Y rail support foot",
            plane="XY",
            origin=(0, 0, foot_z),
        ) as y_foot_sketch:
            Polygon2D(
                [
                    (-rail_depth, 0),
                    (0, 0),
                    (0, arm_length_value),
                    (-rail_depth, arm_length_value),
                ]
            )
        y_foot = y_foot_sketch.extrude(self.foot_thickness)

        # Exact native R18 outside support-foot corner from the supplied
        # hoek_assembly source. The quarter sector stays below the rail bottom;
        # the separate MFTCornerInsert now owns the replaceable outer filler /
        # protection geometry.
        with Sketch(
            name="Rounded outside corner foot",
            plane="XY",
            origin=(0, 0, foot_z),
        ) as bumper_sketch:
            corner = bumper_sketch.profile(start=(-18.0, 0.0))
            corner.line_to((0.0, 0.0))
            corner.line_to((0.0, -18.0))
            corner.arc_center_to(
                (-18.0, 0.0),
                center=(0.0, 0.0),
                clockwise=True,
            )
            corner.close()
        corner_bumper = bumper_sketch.extrude(self.foot_thickness)

        bracket = (
            x_arm
            + y_arm
            + top_gusset
            + bottom_gusset
            + x_foot
            + y_foot
            + corner_bumper
        )

        # The rail's round perforations are centered on the 27 mm back web.
        rail_hole_z = -rail_height / 2
        for x in (self.rail_hole_first, self.rail_hole_second):
            bracket = bracket + Hole(
                d=self.rail_bolt_diameter,
                depth=self.wall_thickness,
                direction=(0, -1, 0),
            ).at(
                x,
                self.wall_thickness,
                rail_hole_z,
            )

        for y in (self.rail_hole_first, self.rail_hole_second):
            bracket = bracket + Hole(
                d=self.rail_bolt_diameter,
                depth=self.wall_thickness,
                direction=(-1, 0, 0),
            ).at(
                self.wall_thickness,
                y,
                rail_hole_z,
            )

        # One provisional upward screw seat fixes the bracket to the MFT
        # underside. The countersink opens on the lower face for tool access.
        bracket = bracket + CountersinkHole(
            d=self.mft_screw_diameter,
            countersink_d=self.mft_screw_head_diameter,
            countersink_angle=90,
            depth=self.top_gusset_thickness,
            direction=(0, 0, 1),
        ).at(
            self.mft_screw_x,
            self.mft_screw_y,
            -self.top_gusset_thickness,
        )

        return bracket.with_material(
            "PETG prototype",
            density_g_cm3=1.27,
            color="#30343B",
        )


MFTRailCornerBracket()
