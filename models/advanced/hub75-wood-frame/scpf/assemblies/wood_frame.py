"""Main plywood frame subassembly."""

from scpf import component, pv

from parts.board import BackBoard, BottomBoard, RoofBoard, SideWall


Side = component(SideWall)
Bottom = component(BottomBoard)
Roof = component(RoofBoard)
Back = component(BackBoard)


def build_wood_frame(
    *,
    opening_width,
    opening_height,
    wood_thickness,
    back_thickness,
    cabinet_depth,
    frame_front_y,
    roof_front_overhang,
    roof_rear_overhang,
    corner_radius,
):
    width = pv(opening_width)
    height = pv(opening_height)
    ply = pv(wood_thickness)
    back = pv(back_thickness)
    depth = pv(cabinet_depth)
    front = pv(frame_front_y)
    front_overhang = pv(roof_front_overhang)
    rear_overhang = pv(roof_rear_overhang)
    radius = pv(corner_radius)

    rear = front + depth
    back_outer = rear + back
    roof_front = front - front_overhang
    roof_rear = back_outer + rear_overhang
    outer_width = width + 2 * ply
    body_y = (front + rear) / 2

    left = Side(
        thickness=ply,
        depth=depth,
        height=height,
    ).move(
        x=-(width / 2 + ply / 2),
        y=body_y,
    )
    sides = left + left.copy().move(x=outer_width - ply)

    bottom = Bottom(
        width=outer_width,
        depth=depth,
        thickness=ply,
        corner_radius=radius,
    ).move(
        y=body_y,
        z=-ply,
    )

    roof = Roof(
        width=outer_width,
        depth=roof_rear - roof_front,
        thickness=ply,
        corner_radius=radius,
    ).move(
        y=(roof_front + roof_rear) / 2,
        z=height,
    )

    rear_board = Back(
        width=outer_width,
        height=height + ply,
        thickness=back,
    ).move(
        y=rear + back / 2,
        z=-ply,
    )

    return (sides + bottom + roof + rear_board).group("WoodBoxFrame")
