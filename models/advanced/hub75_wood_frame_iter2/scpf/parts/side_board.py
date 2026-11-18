"""Side wall with one closed native hand slot."""

from scpf import (
    BOTTOM,
    FRONT,
    Box,
    Sketch,
    SlotCenterToCenter2D,
    component,
)


# Build-time hand-slot geometry.
#
# Keep these as normal Python numbers, not editable SolidCraft parameters.
# SlotCenterToCenter2D can therefore use the native direct Slot command while
# the dimensions still have one readable source and are calculated from each
# other instead of duplicating 85/177/349 as unrelated magic numbers.
SIDE_PANEL_DEPTH = 120.0
HANDLE_SLOT_WIDTH = 30.0
HANDLE_SLOT_REAR_CLEARANCE = 20.0
HANDLE_SLOT_BOTTOM = 162.0
HANDLE_SLOT_TOP = 364.0


@component
class SideBoard:
    """Full-depth side wall with one vertical 30 mm native slot."""

    thickness = 12.0
    depth = SIDE_PANEL_DEPTH
    height = 444.0

    material_name = None
    color = None

    def build(self):
        body = Box(
            self.thickness,
            self.depth,
            self.height,
        ).at(
            0,
            0,
            0,
            anchor=FRONT + BOTTOM,
        )

        # Calculate the native Slot points from the design dimensions.
        # 120 - 20 - 30/2 = Y=85 mm, so the complete slot spans Y=70..100.
        slot_radius = HANDLE_SLOT_WIDTH / 2
        slot_center_y = (
            SIDE_PANEL_DEPTH
            - HANDLE_SLOT_REAR_CLEARANCE
            - slot_radius
        )

        # SlotCenterToCenter2D takes the centres of the round ends. Moving both
        # centres one radius inward preserves the requested overall Z limits:
        # 162..364 becomes centre points Z=177 and Z=349.
        lower_center_z = HANDLE_SLOT_BOTTOM + slot_radius
        upper_center_z = HANDLE_SLOT_TOP - slot_radius

        p0 = (slot_center_y, lower_center_z)
        p1 = (slot_center_y, upper_center_z)

        with Sketch(
            name="Side hand slot",
            on=body,
            plane="YZ",
        ) as opening_sketch:
            profile = SlotCenterToCenter2D(
                p0,
                p1,
                HANDLE_SLOT_WIDTH,
            )
            opening_sketch.add(profile)

        opening = opening_sketch.extrude(
            self.thickness + 2,
            sym=True,
        )
        body = body - opening

        return body.with_material(
            self.material_name or "LIGHTPLY side board",
            density_g_cm3=0.55,
            color=self.color or "#CBA36B",
        )
