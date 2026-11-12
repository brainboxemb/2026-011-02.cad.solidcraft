"""Eight placements of one reusable printed corner bracket."""

from scpf import assembly, component, pv

from models.components.corner_bracket.scpf.model import CornerBracket


Bracket = component(CornerBracket)


@assembly
class CornerBrackets:
    opening_width = 844.0
    opening_height = 362.0
    frame_wood_thickness = 12.0
    cabinet_depth = 100.0
    bracket_width = 24.0
    corner_radius = 4.0

    def build(self):
        outer_width = self.opening_width + 2 * self.frame_wood_thickness
        outer_half = outer_width / 2
        top_z = self.opening_height + 2 * self.frame_wood_thickness

        bracket_half = self.bracket_width / 2
        front_y = bracket_half
        rear_y = self.cabinet_depth - bracket_half

        # CornerBracket is modelled once in its neutral top-left orientation:
        # horizontal arm +X, vertical arm -Z. The other cabinet corners are
        # placements of the same component. 180-degree rotations around X, Y
        # or Z select the other three XZ corner orientations without mirroring.
        bracket = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
        )

        def place(x, y, z, rotation=None):
            occurrence = bracket.copy()
            if rotation is not None:
                axis, angle = rotation
                occurrence = occurrence.rotate(axis, angle)
            return occurrence.move(x=pv(x), y=pv(y), z=pv(z))

        top_left_front = place(-outer_half, front_y, top_z, 0)
        top_left_rear = place(-outer_half, rear_y, top_z, 0)

        top_right_front = place(outer_half, front_y, top_z, ("Z", 180))
        top_right_rear = place(outer_half, rear_y, top_z, ("Z", 180))

        bottom_right_front = place(outer_half, front_y, 0, ("Y", 180))
        bottom_right_rear = place(outer_half, rear_y, 0, ("Y", 180))

        bottom_left_front = place(-outer_half, front_y, 0, ("X", 180))
        bottom_left_rear = place(-outer_half, rear_y, 0, ("X", 180))

        return (
            top_left_front
            + top_left_rear
            + top_right_front
            + top_right_rear
            + bottom_right_front
            + bottom_right_rear
            + bottom_left_front
            + bottom_left_rear
        ).group("CornerBrackets")
