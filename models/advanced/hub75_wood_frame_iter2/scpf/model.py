"""Second iteration of the wooden HUB75 frame, assembled from named parts and subassemblies."""

from assemblies.corner_brackets import CornerBrackets
from assemblies.glass_frame import GlassFrame
from assemblies.hub75_panels import HUB75Panels
from assemblies.wood_frame import WoodFrame
from parts.window import Window


class WoodenHub75BoxIter2:
    """Second iteration of the wooden HUB75 frame with a lower storage compartment."""

    # Coordinate / datum conventions
    #
    # X = 0 : horizontal centre of the cabinet/opening.
    #           Changing frame wood thickness grows the cabinet outwards in ±X;
    #           the opening itself stays centred and keeps opening_width.
    # Y = 0 : front face of the wooden cabinet.
    #           cabinet_depth is the 120 mm base depth of the wooden cabinet.
    #           side_panel_depth is kept separately because the side-wall
    #           recess is defined from that rear edge.
    # Z = 0 : outside bottom face of the wooden cabinet.
    #
    # Vertical stack from Z=0:
    #   bottom board
    #   lower_compartment_height clear storage space
    #   intermediate shelf
    #   opening_height display opening
    #   roof board
    #
    # The bottom, intermediate shelf and roof all use frame_wood_thickness.
    # Therefore the display opening begins at:
    #   2 * frame_wood_thickness + lower_compartment_height
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

    # Lower storage compartment
    lower_compartment_height = 70.0

    # Wood
    frame_wood_thickness = 12.0
    panel_wood_thickness = 9.0
    cabinet_depth = 120.0
    side_panel_depth = 120.0
    roof_front_overhang = 10.0
    roof_rear_overhang = 1.0
    corner_radius = 4.0

    # Closed hand openings in the side walls and rear board.
    handle_opening_width = 30.0
    handle_opening_edge_clearance = 20.0
    handle_opening_radius = 10.0
    handle_opening_lower_keep = 80.0
    handle_opening_upper_keep = 80.0

    # Printed corner brackets
    bracket_width = 24.0

    # Glazing retainers
    glazing_wood_width = 12.0
    glazing_wood_depth = 12.0

    def build(self):
        opening_bottom_z = (
            2 * self.frame_wood_thickness
            + self.lower_compartment_height
        )

        panels = HUB75Panels(
            opening_height=self.opening_height,
            opening_bottom_z=opening_bottom_z,
            panel_recess_depth=self.panel_recess_depth,
        )

        frame = WoodFrame(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            lower_compartment_height=self.lower_compartment_height,
            frame_wood_thickness=self.frame_wood_thickness,
            panel_wood_thickness=self.panel_wood_thickness,
            cabinet_depth=self.cabinet_depth,
            side_panel_depth=self.side_panel_depth,
            roof_front_overhang=self.roof_front_overhang,
            roof_rear_overhang=self.roof_rear_overhang,
            corner_radius=self.corner_radius,
            handle_opening_width=self.handle_opening_width,
            handle_opening_edge_clearance=self.handle_opening_edge_clearance,
            handle_opening_radius=self.handle_opening_radius,
            handle_opening_lower_keep=self.handle_opening_lower_keep,
            handle_opening_upper_keep=self.handle_opening_upper_keep,
        )

        brackets = CornerBrackets(
            opening_width=self.opening_width,
            opening_height=self.opening_height,
            lower_compartment_height=self.lower_compartment_height,
            frame_wood_thickness=self.frame_wood_thickness,
            cabinet_depth=self.cabinet_depth,
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
