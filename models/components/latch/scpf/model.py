"""Latch reconstruction from the supplied native SolidCraft reference.

This file deliberately starts with the design vocabulary and parameter set only.
Do not approximate the native sheet-metal or revolved features with ordinary
fused solids. See models/components/latch/README.md and docs/plan.md.
"""


class Latch:
    # Overall/reference dimensions.
    overall_length = 73.0
    latch_height = 14.5
    clearance = 0.10

    # Mounting foot.
    foot_start = 15.5
    foot_length = 43.0
    foot_width = 16.5
    foot_thickness = 2.0
    first_mounting_hole = 23.0
    mounting_hole_pitch = 14.0
    mounting_hole_diameter = 4.2

    # Operating handle.
    handle_width = 16.5
    handle_thickness = 1.6

    # Pull bail.
    bail_width = 23.5
    bail_thickness = 2.0
    bail_pin_x = 33.5
    bail_pin_z = 6.0
    bail_pin_diameter = 4.0

    # Main/front hinge.
    hinge_x = 45.5
    hinge_z = 7.45
    front_hinge_x = 20.5
    front_hinge_z = 7.3
    hinge_pin_diameter = 3.8

    # Locking spring/lip.
    locking_lip_width = 8.4
    locking_lip_thickness = 0.7

    # Native sheet-rule values copied from the source design.
    FOOT_BEND_RADIUS = 0.6
    FOOT_K_FACTOR = 0.40
    HANDLE_BEND_RADIUS = 0.9
    HANDLE_K_FACTOR = 0.40
    BAIL_BEND_RADIUS = 1.0
    BAIL_K_FACTOR = 0.40
    LOCKING_LIP_BEND_RADIUS = 0.8
    LOCKING_LIP_K_FACTOR = 0.42

    def build(self):
        raise NotImplementedError(
            "Latch reconstruction is waiting for the released Forge #843 "
            "Revolve API; the exact latch.sc reference is now present; see README.md."
        )


Latch()
