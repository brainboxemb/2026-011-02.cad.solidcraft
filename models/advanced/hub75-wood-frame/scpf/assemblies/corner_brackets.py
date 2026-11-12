"""Eight printed corner-bracket occurrences."""

from scpf import assembly, component

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
        rear_offset = rear_y - front_y

        top_left_front = Bracket(
            inside_corner_radius=self.corner_radius,
            x_position=-outer_half,
            z_position=top_z,
            x_sign=1,
            z_sign=1,
        ).move(y=front_y)
        top_left_rear = top_left_front.copy().move(y=rear_offset)

        top_right_front = Bracket(
            inside_corner_radius=self.corner_radius,
            x_position=outer_half,
            z_position=top_z,
            x_sign=-1,
            z_sign=1,
        ).move(y=front_y)
        top_right_rear = top_right_front.copy().move(y=rear_offset)

        bottom_left_front = Bracket(
            inside_corner_radius=self.corner_radius,
            x_position=-outer_half,
            z_position=bottom_z,
            x_sign=1,
            z_sign=-1,
        ).move(y=front_y)
        bottom_left_rear = bottom_left_front.copy().move(y=rear_offset)

        bottom_right_front = Bracket(
            inside_corner_radius=self.corner_radius,
            x_position=outer_half,
            z_position=bottom_z,
            x_sign=-1,
            z_sign=-1,
        ).move(y=front_y)
        bottom_right_rear = bottom_right_front.copy().move(y=rear_offset)

        return (
            top_left_front
            + top_left_rear
            + top_right_front
            + top_right_rear
            + bottom_left_front
            + bottom_left_rear
            + bottom_right_front
            + bottom_right_rear
        ).group("CornerBrackets")
