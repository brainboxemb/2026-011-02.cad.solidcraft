"""Eight printed corner-bracket occurrences."""

from scpf import assembly, component

from models.components.corner_bracket import CornerBracket


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
        bottom_z = 0.0

        bracket_half = self.bracket_width / 2
        front_y = bracket_half
        rear_y = self.cabinet_depth - bracket_half

        top_left_front = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
            _x_position=-outer_half,
            _y_position=front_y,
            _z_position=top_z,
            _x_sign=1,
            _z_sign=1,
        )
        top_left_rear = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
            _x_position=-outer_half,
            _y_position=rear_y,
            _z_position=top_z,
            _x_sign=1,
            _z_sign=1,
        )

        top_right_front = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
            _x_position=outer_half,
            _y_position=front_y,
            _z_position=top_z,
            _x_sign=-1,
            _z_sign=1,
        )
        top_right_rear = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
            _x_position=outer_half,
            _y_position=rear_y,
            _z_position=top_z,
            _x_sign=-1,
            _z_sign=1,
        )

        bottom_left_front = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
            _x_position=-outer_half,
            _y_position=front_y,
            _z_position=bottom_z,
            _x_sign=1,
            _z_sign=-1,
        )
        bottom_left_rear = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
            _x_position=-outer_half,
            _y_position=rear_y,
            _z_position=bottom_z,
            _x_sign=1,
            _z_sign=-1,
        )

        bottom_right_front = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
            _x_position=outer_half,
            _y_position=front_y,
            _z_position=bottom_z,
            _x_sign=-1,
            _z_sign=-1,
        )
        bottom_right_rear = Bracket(
            bracket_width=self.bracket_width,
            inside_corner_radius=self.corner_radius,
            _x_position=outer_half,
            _y_position=rear_y,
            _z_position=bottom_z,
            _x_sign=-1,
            _z_sign=-1,
        )

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
