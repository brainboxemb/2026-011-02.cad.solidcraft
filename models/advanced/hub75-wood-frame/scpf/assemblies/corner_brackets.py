"""Eight printed corner-bracket occurrences."""

from scpf import X, Y, Z, assembly, component

from components.corner_bracket import CornerBracket


Bracket = component(CornerBracket)


@assembly
class CornerBrackets:
    opening_width = 844.0
    opening_height = 362.0
    frame_wood_thickness = 12.0
    cabinet_depth = 100.0
    corner_radius = 4.0

    def build(self):
        rear = self.cabinet_depth
        outer_width = self.opening_width + 2 * self.frame_wood_thickness
        outer_half = outer_width / 2
        top_z = self.opening_height + self.frame_wood_thickness
        bottom_z = -self.frame_wood_thickness

        bracket_half = CornerBracket.bracket_width / 2
        front_y = bracket_half
        rear_y = rear - bracket_half

        top_left_front = Bracket(
            inside_corner_radius=self.corner_radius,
            z_position=top_z,
        ).move(
            x=-outer_half,
            y=front_y,
        )
        top_right_front = top_left_front.copy().move(
            x=2 * outer_half,
        ).rotate(Z, 180)
        top_left_rear = top_left_front.copy().move(
            y=rear_y - front_y,
        )
        top_right_rear = top_left_front.copy().move(
            x=2 * outer_half,
            y=rear_y - front_y,
        ).rotate(Z, 180)

        bottom_base = Bracket(
            inside_corner_radius=self.corner_radius,
        )
        bottom_left_front = bottom_base.move(
            x=-outer_half,
            y=front_y,
            z=bottom_z,
        ).rotate(X, 180)
        bottom_right_front = bottom_base.copy().move(
            x=outer_half,
            y=front_y,
            z=bottom_z,
        ).rotate(Y, 180)
        bottom_left_rear = bottom_base.copy().move(
            x=-outer_half,
            y=rear_y,
            z=bottom_z,
        ).rotate(X, 180)
        bottom_right_rear = bottom_base.copy().move(
            x=outer_half,
            y=rear_y,
            z=bottom_z,
        ).rotate(Y, 180)

        return (
            top_left_front
            + top_right_front
            + top_left_rear
            + top_right_rear
            + bottom_left_front
            + bottom_right_front
            + bottom_left_rear
            + bottom_right_rear
        ).group("CornerBrackets")
