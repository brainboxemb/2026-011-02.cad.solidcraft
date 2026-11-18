class SamplePlate:
    """Build the sample plate from object-level CAD intent."""

    width = 80
    depth = 50
    thickness = 8

    def build(self):
        with Sketch(name="Base", plane="XY") as sketch:
            Rectangle2D(self.width, self.depth)
        plate = sketch.extrude(self.thickness)
        plate = plate.fillet(6, edges=Edges.VERTICAL)

        spacing = self.width - 24
        with Sketch(
            name="Holes",
            on=plate,
            parent=Anchor.TOP,
        ) as holes:
            holes.add(
                Circle2D(d=8),
                offset=(-(spacing / 2), 0),
            )

        source_cut = holes.extrude(Depth.THROUGH_ALL)
        plate = plate - source_cut
        plate = plate.rectangular_pattern(
            source_cut,
            count=2,
            spacing=spacing,
            direction=Axis.X,
        )

        boss = Cylinder(d=24, h=14).attach(
            plate,
            parent=Anchor.TOP,
            child=Anchor.BOTTOM,
        )
        plate = plate + boss

        bore = Hole(d=12, depth=Depth.THROUGH_ALL).attach(
            plate,
            parent=Anchor.TOP,
        )
        return plate + bore
