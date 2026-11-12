"""Eight printed corner-bracket occurrences."""

from scpf import component, pv

from components.corner_bracket import CornerBracket


Bracket = component(CornerBracket)


class CornerBrackets:
    opening_width = 844.0
    opening_height = 362.0
    wood_thickness = 12.0
    cabinet_depth = 100.0
    frame_front_y = -25.0

    def build(self):
        width = pv(self.opening_width)
        height = pv(self.opening_height)
        ply = pv(self.wood_thickness)
        depth = pv(self.cabinet_depth)
        front = pv(self.frame_front_y)

        rear = front + depth
        outer_width = width + 2 * ply
        outer_half = outer_width / 2
        top_z = height + ply
        bottom_z = -ply

        bracket_half = CornerBracket.bracket_width / 2
        front_y = front + bracket_half
        rear_y = rear - bracket_half

        upper_left = Bracket().move(
            x=-outer_half,
            y=front_y,
            z=top_z,
        )
        brackets = upper_left

        corner_poses = (
            (outer_half, top_z, (0, 0, 1), 180),
            (-outer_half, bottom_z, (1, 0, 0), 180),
            (outer_half, bottom_z, (0, 1, 0), 180),
        )
        for x, z, axis, angle in corner_poses:
            brackets = brackets + upper_left.copy().move(
                x=x + outer_half,
                z=z - top_z,
            ).rotate(
                axis=axis,
                degrees=angle,
            )

        for x, z, axis, angle in (
            (-outer_half, top_z, None, 0),
            *corner_poses,
        ):
            occurrence = upper_left.copy().move(
                x=x + outer_half,
                y=rear_y - front_y,
                z=z - top_z,
            )
            if axis is not None:
                occurrence = occurrence.rotate(
                    axis=axis,
                    degrees=angle,
                )
            brackets = brackets + occurrence

        return brackets.group("CornerBrackets")
