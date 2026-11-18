@dataclass
class AnchoredHoles:
    """Two through holes, each 20 mm from the center along the Y axis."""

    width: float = 100
    depth: float = 60
    thickness: float = 10
    spacing: float = 40

    def build(self):
        with Sketch(name="Base", plane="XY") as sketch:
            Rectangle2D(self.width, self.depth)
        plate = sketch.extrude(self.thickness)

        with Sketch(
            name="Hole",
            on=plate,
            parent=Anchor.TOP,
        ) as hole:
            hole.add(
                Circle2D(d=8),
                offset=(0, -(self.spacing / 2)),
            )

        source_cut = hole.extrude(Depth.THROUGH_ALL)
        plate = plate - source_cut

        return plate.rectangular_pattern(
            source_cut,
            count=2,
            spacing=self.spacing,
            direction=Axis.Y,
        )


AnchoredHoles()
