"""Wooden HUB75 display assembled from named parts and subassemblies."""

from assemblies.corner_brackets import CornerBrackets
from assemblies.glass_frame import GlassFrame
from assemblies.hub75_panels import HUB75Panels
from assemblies.wood_frame import WoodFrame
from parts.window import Window


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

    # Parameter intent:
    #   lower_case  = native editable SolidCraft model parameter
    #   _lower_case = Forge/build-time input; intentionally not native
    #   UPPER_CASE  = fixed constants in the owning part/assembly module
    #
    # Display / inside opening
    opening_width = 844.0
    opening_height = 362.0
    panel_recess_depth = 25.0

    # Wood
    frame_wood_thickness = 12.0
    panel_wood_thickness = 9.0
    cabinet_depth = 100.0
    roof_front_overhang = 10.0
    roof_rear_overhang = 1.0
    corner_radius = 4.0

    # Printed corner brackets
    bracket_width = 24.0

    # Glazing retainers
    glazing_wood_width = 12.0
    glazing_wood_depth = 12.0

    def build(self):
        opening_bottom_z = self.frame_wood_thickness

        panels = HUB75Panels(
            opening_height=self.opening_height,
            opening_bottom_z=opening_bottom_z,
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

        brackets = CornerBrackets(
            wood_frame=frame,
            frame_wood_thickness=self.frame_wood_thickness,
            bracket_width=self.bracket_width,
            corner_radius=self.corner_radius,
        )

        glazing = GlassFrame(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            opening_bottom_z=opening_bottom_z,
            glazing_wood_width=self.glazing_wood_width,
            glazing_wood_depth=self.glazing_wood_depth,
        )

        window = Window(
            opening_height=self.opening_height,
            opening_bottom_z=opening_bottom_z,
            front_y=self.glazing_wood_depth,
        )

        return panels + frame + brackets + glazing + window
