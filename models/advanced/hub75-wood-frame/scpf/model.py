"""Wooden HUB75 display assembled from named parts and subassemblies."""

from assemblies.corner_brackets import CornerBrackets
from assemblies.glass_frame import GlassFrame
from assemblies.hub75_panels import HUB75Panels
from assemblies.wood_frame import WoodFrame
from parts.window import GLASS_BOTTOM_CLEARANCE, GLASS_THICKNESS, Window


class WoodenHub75Box:
    """Top-level adjustable design parameters and composition."""

    # Display / inside opening
    opening_width = 844.0
    opening_height = 362.0
    panel_count = 5
    panel_pitch = 160.0

    # Wood
    frame_wood_thickness = 12.0
    panel_wood_thickness = 9.0
    cabinet_depth = 100.0
    frame_front_y_position = -25.0
    roof_front_overhang = 10.0
    roof_rear_overhang = 1.0
    corner_radius = 4.0

    # Glazing retainers
    glazing_wood_width = 12.0
    glazing_wood_depth = 12.0

    def build(self):
        panels = HUB75Panels(
            opening_height=self.opening_height,
            panel_count=self.panel_count,
            panel_pitch=self.panel_pitch,
        )

        frame = WoodFrame(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            frame_wood_thickness=self.frame_wood_thickness,
            panel_wood_thickness=self.panel_wood_thickness,
            cabinet_depth=self.cabinet_depth,
            frame_front_y_position=self.frame_front_y_position,
            roof_front_overhang=self.roof_front_overhang,
            roof_rear_overhang=self.roof_rear_overhang,
            corner_radius=self.corner_radius,
        )

        glazing = GlassFrame(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            frame_front_y_position=self.frame_front_y_position,
            glazing_wood_width=self.glazing_wood_width,
            glazing_wood_depth=self.glazing_wood_depth,
        )

        brackets = CornerBrackets(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            frame_wood_thickness=self.frame_wood_thickness,
            cabinet_depth=self.cabinet_depth,
            frame_front_y_position=self.frame_front_y_position,
        )

        window = Window().move(
            y=self.frame_front_y_position + self.glazing_wood_depth + GLASS_THICKNESS / 2,
            z=GLASS_BOTTOM_CLEARANCE,
        )

        return panels + frame + glazing + brackets + window


WoodenHub75Box()
