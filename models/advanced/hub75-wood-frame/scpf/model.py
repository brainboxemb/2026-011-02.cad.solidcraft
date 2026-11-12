"""Wooden HUB75 display assembled from separate part and assembly modules."""

from assemblies.corner_brackets import build_corner_brackets
from assemblies.glass_frame import build_glass_frame
from assemblies.hub75_panels import build_hub75_panels
from assemblies.window import build_window
from assemblies.wood_frame import build_wood_frame


class WoodenHub75Box:
    """Top-level design parameters and composition only."""

    # Display / inside opening
    opening_width = 844.0
    opening_height = 362.0
    panel_count = 5
    panel_pitch = 160.0

    # Wood
    wood_thickness = 12.0
    back_thickness = 9.0
    cabinet_depth = 100.0
    frame_front_y = -25.0
    roof_front_overhang = 10.0
    roof_rear_overhang = 1.0
    corner_radius = 4.0

    # Window and mitred glazing
    glass_width = 840.0
    glass_height = 360.0
    glass_thickness = 4.0
    glass_bottom_clearance = 1.0
    glazing_width = 15.0
    glazing_depth = 15.0

    def build(self):
        panels = build_hub75_panels(
            opening_height=self.opening_height,
            panel_count=self.panel_count,
            panel_pitch=self.panel_pitch,
        )

        frame = build_wood_frame(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            wood_thickness=self.wood_thickness,
            back_thickness=self.back_thickness,
            cabinet_depth=self.cabinet_depth,
            frame_front_y=self.frame_front_y,
            roof_front_overhang=self.roof_front_overhang,
            roof_rear_overhang=self.roof_rear_overhang,
            corner_radius=self.corner_radius,
        )

        glazing = build_glass_frame(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            frame_front_y=self.frame_front_y,
            glazing_width=self.glazing_width,
            glazing_depth=self.glazing_depth,
        )

        brackets = build_corner_brackets(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            wood_thickness=self.wood_thickness,
            cabinet_depth=self.cabinet_depth,
            frame_front_y=self.frame_front_y,
        )

        window = build_window(
            glass_width=self.glass_width,
            glass_height=self.glass_height,
            glass_thickness=self.glass_thickness,
            glass_bottom_clearance=self.glass_bottom_clearance,
            frame_front_y=self.frame_front_y,
            glazing_depth=self.glazing_depth,
        )

        return panels + frame + glazing + brackets + window


WoodenHub75Box()
