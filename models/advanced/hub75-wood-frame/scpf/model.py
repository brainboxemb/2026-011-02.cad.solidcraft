"""Wooden HUB75 Basic Box — one readable, parametrized SolidCraft assembly.

All design dimensions are in millimetres and collected on WoodenHub75Box.
Only the general-purpose Hub75PanelBasic and CornerBracket live in the
shared components/ package; wood and glazing are defined *here*, where
they belong. SCPF describes the placement; SolidCraft builds the geometry.

Coordinate system:
    X = left/right across the display
    Y = front (-) / rear (+)
    Z = vertical; inner opening starts at Z=0

Parts shown are a design concept; fastening details remain to be verified.
"""
from scpf import Box, Polygon2D, Direction, component
from scpf.core import value_of
from components.hub75_basic import Hub75PanelBasic
from components.corner_bracket import CornerBracket

Panel = component(Hub75PanelBasic)
Bracket = component(CornerBracket)


class SideWall:
    """One vertical sheet: thickness × cabinet depth × opening height."""
    thickness = 12.0
    depth = 100.0
    height = 362.0

    def build(self):
        return Box(self.thickness, self.depth, self.height).with_material(
            "LIGHTPLY side wall", density_g_cm3=0.55, color="#CBA36B"
        )


class BottomBoard:
    """The outside bottom corners need R4 to clear the bracket's R4 fillet."""
    width = 868.0
    depth = 100.0
    thickness = 12.0
    corner_radius = 4.0

    def build(self):
        # Box spans X=-width/2..+width/2 and Z=0..thickness.
        # These Y-parallel outside edges mate with the printed brackets.
        half = value_of(self.width) / 2
        body = Box(self.width, self.depth, self.thickness)
        body = body.fillet(self.corner_radius, edges=[
            [-half, 0, 0], [half, 0, 0],
        ])
        return body.with_material(
            "LIGHTPLY bottom", density_g_cm3=0.55, color="#CBA36B"
        )


class RoofBoard:
    """12 mm roof, with R4 only at the two top outer Y-parallel edges."""
    width = 868.0
    depth = 120.0
    thickness = 12.0
    corner_radius = 4.0

    def build(self):
        half = value_of(self.width) / 2
        height = value_of(self.thickness)
        body = Box(self.width, self.depth, self.thickness)
        body = body.fillet(self.corner_radius, edges=[
            [-half, 0, height], [half, 0, height],
        ])
        return body.with_material(
            "LIGHTPLY roof", density_g_cm3=0.55, color="#CBA36B"
        )


class BackBoard:
    """One 9 mm sheet on the REAR of the 100 mm-deep frame."""
    width = 868.0
    height = 374.0
    thickness = 9.0

    def build(self):
        return Box(self.width, self.thickness, self.height).with_material(
            "LIGHTPLY rear", density_g_cm3=0.55, color="#A87D4D"
        )


class Window:
    """4 mm glass panel, separate from its four wooden retainers."""
    width = 840.0
    height = 360.0
    thickness = 4.0

    def build(self):
        return Box(self.width, self.thickness, self.height).with_material(
            "Plexiglass", density_g_cm3=1.19, color="#B7DAEF"
        )


class GlassStrip:
    """ONE mitred retaining-strip type, used vertically and horizontally.

    The long dimension is local X; the 15 mm trim width is local Z.
    The XY-independent section lies in XZ and extrudes symmetrically in Y.

    Both end cuts are straight 45-degree mitres: NO rounded corners here.
    `finish=1` is a darker visual finish for vertical strips; `finish=0`
    is lighter for horizontal strips. It is not a prescribed timber species.
    The assembly, not this component, determines the final orientation.
    """
    length = 844.0
    width = 15.0
    depth = 15.0
    finish = 0

    def build(self):
        if not 0 < value_of(self.width) < value_of(self.length) / 2:
            raise ValueError("GlassStrip width must be less than half its length")
        # Keep the actual native SolidCraft sketch symbolic: editing the
        # native GlassStrip_length / GlassStrip_width parameters changes
        # the corresponding XZ profile, not merely the Python preview.
        half = self.length / 2
        inset = half - self.width
        # Outside edge z=0, both end cuts retreat by 'width' at z=width.
        profile = Polygon2D([
            (-half, 0), (half, 0),
            (inset, self.width), (-inset, self.width),
        ], plane="XZ", world=True)
        dark = value_of(self.finish) >= 0.5
        return profile.extrude(
            self.depth, direction=Direction.SYMMETRIC,
        ).with_material(
            "LIGHTPLY glazing vertical" if dark else "LIGHTPLY glazing horizontal",
            density_g_cm3=0.55,
            color="#A9793E" if dark else "#E3BF80",
        )


class WoodenHub75Box:
    """Central design parameters. All part sizes and positions derive here.

    Change these values to resize the complete frame. Component classes
    above are simple reusable *types*; the assembly passes their dimensions.

    Cabinet front and rear refer to the sidewall surfaces. Rear ply is
    attached *behind* the sidewalls. Roof overhangs are measured from
    the OUTER face of the front wood and the OUTER face of the rear ply.
    """

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
        # Extract ordinary numeric values only for CAD occurrence placement.
        # No custom rotations, transformation matrices or inverse transforms.
        w = value_of(self.opening_width)
        h = value_of(self.opening_height)
        ply = value_of(self.wood_thickness)
        back_t = value_of(self.back_thickness)
        depth = value_of(self.cabinet_depth)
        front = value_of(self.frame_front_y)
        rear = front + depth
        back_outer = rear + back_t
        roof_front = front - value_of(self.roof_front_overhang)
        roof_rear = back_outer + value_of(self.roof_rear_overhang)
        outer_width = w + 2 * ply
        outer_half = outer_width / 2
        radius = value_of(self.corner_radius)
        glass_t = value_of(self.glass_thickness)
        trim_w = value_of(self.glazing_width)
        trim_d = value_of(self.glazing_depth)
        top_z = h + ply
        bottom_z = -ply
        body_y = (front + rear) / 2

        # 1. Five identical lightweight HUB75 placements, one definition.
        #    Their flat front faces lie in world XZ; Z is up.
        panel_y = Hub75PanelBasic.depth / 2
        panel_z = (h - Hub75PanelBasic.height) / 2
        middle = Panel().move(y=panel_y, z=panel_z)
        panels = middle
        count = int(value_of(self.panel_count))
        if count < 1 or count % 2 != 1:
            raise ValueError("panel_count must be a positive odd number")
        pitch = value_of(self.panel_pitch)
        for col in range(count):
            if col == count // 2:
                continue
            x = (col - count // 2) * pitch
            panels = panels + middle.copy().move(x=x)
        panels = panels.group("HUB75Panels")

        # 2. Main 12 mm plywood frame, with a 9 mm back glued/fastened
        #    behind it. The roof extends 10 mm at the front and 1 mm
        #    beyond the back board, rather than beyond the bare sidewall.
        left = SideWall(
            thickness=ply, depth=depth, height=h,
        ).move(x=-(w / 2 + ply / 2), y=body_y)
        sides = left + left.copy().move(x=outer_width - ply)
        bottom = BottomBoard(
            width=outer_width, depth=depth, thickness=ply,
            corner_radius=radius,
        ).move(y=body_y, z=bottom_z)
        roof = RoofBoard(
            width=outer_width, depth=roof_rear - roof_front,
            thickness=ply, corner_radius=radius,
        ).move(y=(roof_front + roof_rear) / 2, z=h)
        back = BackBoard(
            width=outer_width, height=h + ply, thickness=back_t,
        ).move(y=rear + back_t / 2, z=bottom_z)
        box = (sides + bottom + roof + back).group("WoodBoxFrame")

        # 3. One GlassStrip class used for all four trims.
        #    Both local profiles point along X; turn the two vertical
        #    occurrences around world Y. Their 45° mitres meet exactly.
        #    Glass strips start FLUSH with the sidewall's front (Y=front),
        #    so they do not protrude from the wooden box.
        trim_y = front + trim_d / 2
        horizontal = GlassStrip(
            length=w, width=trim_w, depth=trim_d, finish=0,
        )
        bottom_trim = horizontal.move(y=trim_y)
        top_trim = horizontal.copy().rotate(
            axis=(1, 0, 0), degrees=180
        ).move(y=trim_y, z=h)

        vertical = GlassStrip(
            length=h, width=trim_w, depth=trim_d, finish=1,
        )
        left_trim = vertical.rotate(
            axis=(0, 1, 0), degrees=90,
        ).move(x=-w / 2, y=trim_y, z=h / 2)
        right_trim = vertical.copy().rotate(
            axis=(0, 1, 0), degrees=-90,
        ).move(x=w / 2, y=trim_y, z=h / 2)
        # Put the two horizontal occurrences first in the native browser.
        # They become GlassStrip:1/2; the vertical length is GlassStrip 2.
        glazing = (
            bottom_trim + top_trim + left_trim + right_trim
        ).group("WoodGlassFrame")

        # Glass is directly behind the retaining strips. With front=-25
        # and trim_d=15, the strip ends at Y=-10 and the glass occupies
        # Y=-10..-6: still clear of the display front at Y=0.
        glass_front = front + trim_d
        glass = Window(
            width=value_of(self.glass_width),
            height=value_of(self.glass_height),
            thickness=glass_t,
        ).move(y=glass_front + glass_t / 2,
               z=value_of(self.glass_bottom_clearance))

        # 4. EIGHT hole-free brackets: two on each physical X/Z corner.
        #    Front brackets start with the sidewall at Y=front.
        #    Rear brackets END with the sidewall at Y=rear, BEFORE the
        #    separately attached 9 mm backboard (Y=rear..back_outer).
        #    Each bracket is 24 mm wide in Y; none intersects the backboard.
        #    Shared source: components/corner_bracket.py.
        bracket_half = CornerBracket.bracket_width / 2
        front_bracket_y = front + bracket_half
        rear_bracket_y = rear - bracket_half
        upper_left = Bracket().move(
            x=-outer_half, y=front_bracket_y, z=top_z
        )
        brackets = upper_left
        corner_poses = (
            # X, Z, rotation axis, angle
            (outer_half, top_z, (0, 0, 1), 180),
            (-outer_half, bottom_z, (1, 0, 0), 180),
            (outer_half, bottom_z, (0, 1, 0), 180),
        )
        for x, z, axis, angle in corner_poses:
            brackets = brackets + upper_left.copy().move(
                x=x + outer_half, z=z - top_z
            ).rotate(axis=axis, degrees=angle)
        for x, z, axis, angle in (
            (-outer_half, top_z, None, 0), *corner_poses
        ):
            rear_occurrence = upper_left.copy().move(
                x=x + outer_half,
                y=rear_bracket_y - front_bracket_y,
                z=z - top_z,
            )
            if axis is not None:
                rear_occurrence = rear_occurrence.rotate(
                    axis=axis, degrees=angle,
                )
            brackets = brackets + rear_occurrence
        brackets = brackets.group("CornerBrackets")

        return panels + box + glazing + brackets + glass


WoodenHub75Box()
