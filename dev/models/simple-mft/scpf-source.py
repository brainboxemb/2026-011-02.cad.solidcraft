"""Simple MFT worktop inspired by the Craftmaker S30 replacement top.

The plate envelope and dog-hole diameter follow the published replacement-top
dimensions. The 76 mm pitch, 20 mm corner cuts and clamp-slot dimensions are
photo-based design estimates, not manufacturer dimensions.

The current 2D expectation is calibrated from the front product photo:
- slot width about 24 mm;
- slot end-centre distance about 80 mm, giving about 104 mm overall length;
- per diagonal arm, the inner slot starts on grid ring 1 and extends outward;
- the outer slot starts on grid ring 3 and extends inward;
- the four diagonal grid-ring-2 dog-hole positions are omitted.

The dog holes deliberately follow a normal SolidCraft workflow:
- one Circle seed;
- one associative 9 x 7 Sketch rectangular pattern;
- one selective cut using 59 of the 63 closed profiles.

The clamp slots use one Slot seed, one Sketch pattern and three mirrors.
"""

from math import sqrt

from scpf import (
    Anchor,
    Axis,
    Box,
    Circle2D,
    Depth,
    Edges,
    Sketch,
    SlotCenterToCenter2D,
    component,
)


@component(include="*")
class SimpleMFT:
    width = 805.0
    depth = 555.0
    thickness = 18.0
    hole_diameter = 20.0
    hole_pitch = 76.0
    corner_chamfer = 20.0

    COLUMNS = 9
    ROWS = 7

    SLOT_WIDTH = 24.0
    SLOT_CENTER_DISTANCE = 80.0

    def build(self):
        board = Box(
            self.width,
            self.depth,
            self.thickness,
            anchor=Anchor.BOTTOM,
        )

        # Build the dog-hole geometry as ONE native associative SolidCraft
        # Sketch pattern. The sketch contains all 9 x 7 = 63 Circle profiles;
        # we deliberately keep the pattern complete instead of constructing
        # 59 independent holes in Python.
        p = self.hole_pitch
        pitch = float(p.value)

        with Sketch(name="Dog holes", on=board, parent=Anchor.TOP) as holes:
            seed = holes.add(
                Circle2D(d=self.hole_diameter),
                offset=(-4 * p, -3 * p),
            )
            holes.rectangular_pattern(
                seed,
                count=self.COLUMNS,
                spacing=p,
                direction=Axis.X,
                count2=self.ROWS,
                spacing2=p,
                direction2=Axis.Y,
            )

        # Four diagonal ring-2 positions must remain solid because that clear
        # space belongs to the clamp-slot layout. These are grid coordinates,
        # not millimetre coordinates: with the current 76 mm pitch they are
        # the four positions at (±152, ±152) mm.
        excluded_dog_hole_grid_positions = {
            (-2, -2),
            (-2, 2),
            (2, -2),
            (2, 2),
        }

        # SolidCraft's native solid.extrude can select closed Sketch regions
        # by a point inside each region. SCPF passes these 59 points directly
        # as native profile picks; it does NOT create 59 separate Circle/cut
        # features. SolidCraft stores the selected regions by their surrounding
        # sketch curves, so the cut continues to follow the associative 9 x 7
        # pattern when its saved parameters (for example pitch) are changed.
        #
        # exact_regions=True means each point selects exactly the closed region
        # that contains it. The four excluded pattern regions therefore stay
        # uncut while the other 59 become one native through-all extrusion.
        dog_hole_profile_picks = [
            (column * pitch, row * pitch)
            for row in range(-3, 4)
            for column in range(-4, 5)
            if (column, row) not in excluded_dog_hole_grid_positions
        ]
        board = board - holes.extrude(
            Depth.THROUGH_ALL,
            profiles=dog_hole_profile_picks,
            exact_regions=True,
        )

        # SolidCraft 0.42 direct Slot creators use fixed numeric profile points.
        slot_center_distance = float(self.SLOT_CENTER_DISTANCE)
        slot_width = float(self.SLOT_WIDTH)
        along_axis = slot_center_distance / sqrt(2)

        inner_ring = (pitch, pitch)
        inner_outward = (
            pitch + along_axis,
            pitch + along_axis,
        )

        # Translation from the inner Slot to the outer Slot on the same arm.
        # SolidCraft normalises the (1, 1) direction vector.
        slot_pattern_spacing = (
            2 * sqrt(2) * pitch - slot_center_distance
        )

        with Sketch(name="Clamp slots", on=board, parent=Anchor.TOP) as slots:
            master_slot = SlotCenterToCenter2D(
                inner_ring,
                inner_outward,
                slot_width,
            )
            upper_right = slots.rectangular_pattern(
                master_slot,
                count=2,
                spacing=slot_pattern_spacing,
                direction=(1, 1),
            )
            upper_left = slots.mirror(upper_right, axis=Axis.Y)
            slots.mirror(upper_right, axis=Axis.X)
            slots.mirror(upper_left, axis=Axis.X)

        board = board - slots.extrude(Depth.THROUGH_ALL)

        # Apply the four plan-view corner chamfers after the attached cuts.
        board = board.chamfer(
            self.corner_chamfer,
            edges=Edges.VERTICAL,
        )

        return board.with_material(
            "MDF",
            density_g_cm3=0.70,
            color="#C8A46A",
        )
