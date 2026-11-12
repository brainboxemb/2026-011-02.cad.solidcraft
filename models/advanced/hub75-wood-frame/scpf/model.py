"""Wooden HUB75 display assembled from named parts and subassemblies."""

from assemblies.corner_brackets import CornerBrackets
from assemblies.glass_frame import GlassFrame
from assemblies.hub75_panels import HUB75Panels
from assemblies.wood_frame import WoodFrame
from parts.window import GLASS_THICKNESS, Window


class WoodenHub75Box:
    """Top-level adjustable design parameters and composition."""

    # Coordinate / datum conventions
    #
    # X = 0 : horizontal centre of the cabinet/opening.
    #           Changing frame wood thickness grows the cabinet outwards in ±X;
    #           the opening itself stays centred and keeps opening_width.
    # Y = 0 : front face of the wooden cabinet.
    #           cabinet_depth grows only towards +Y. The rear sidewall face is
    #           Y=cabinet_depth and the back board starts at that same plane.
    # Z = 0 : outside bottom face of the wooden cabinet.
    #           frame_wood_thickness grows upwards from here; the opening starts
    #           at Z=frame_wood_thickness and keeps opening_height.
    #
    # Derived reference planes:
    #   opening X = ±opening_width / 2
    #   cabinet X = ±(opening_width / 2 + frame_wood_thickness)
    #   opening Z = frame_wood_thickness ..
    #               frame_wood_thickness + opening_height
    #   cabinet rear Y = cabinet_depth
    #   back board front Y = cabinet_depth
    #   roof front Y = -roof_front_overhang (the deliberate front exception)
    #
    # Parameter rule: dimensions may move these reference planes, but no
    # dependent part may freeze such a relationship into an occurrence.move.

    # Display / inside opening
    opening_width = 844.0
    opening_height = 362.0
    panel_count = 5
    panel_pitch = 160.0

    # Wood
    frame_wood_thickness = 12.0
    panel_wood_thickness = 9.0
    cabinet_depth = 100.0
    panel_recess_depth = 25.0
    roof_front_overhang = 10.0
    roof_rear_overhang = 1.0
    corner_radius = 4.0

    # Glazing retainers
    glazing_wood_width = 12.0
    glazing_wood_depth = 12.0

    def build(self):
        panels = HUB75Panels(
            opening_height=self.opening_height,
            frame_wood_thickness=self.frame_wood_thickness,
            panel_count=self.panel_count,
            panel_pitch=self.panel_pitch,
            panel_recess_depth=self.panel_recess_depth,
        )

        frame = WoodFrame(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            frame_wood_thickness=self.frame_wood_thickness,
            panel_wood_thickness=self.panel_wood_thickness,
            cabinet_depth=self.cabinet_depth,
            roof_front_overhang=self.roof_front_overhang,
            roof_rear_overhang=self.roof_rear_overhang,
            corner_radius=self.corner_radius,
        )

        glazing = GlassFrame(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            frame_wood_thickness=self.frame_wood_thickness,
            glazing_wood_width=self.glazing_wood_width,
            glazing_wood_depth=self.glazing_wood_depth,
        )

        brackets = CornerBrackets(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            frame_wood_thickness=self.frame_wood_thickness,
            cabinet_depth=self.cabinet_depth,
            corner_radius=self.corner_radius,
        )

        window = Window(
            opening_height=self.opening_height,
            frame_wood_thickness=self.frame_wood_thickness,
        ).move(
            y=self.glazing_wood_depth + GLASS_THICKNESS / 2,
        )

        return panels + frame + glazing + brackets + window


WoodenHub75Box()
