class CsgCube:
    size = 50

    def build(self):
        body = Sphere(self.size / 1.5) & Box(self.size, self.size, self.size)

        half = self.size / 2
        diameter = self.size / 1.5

        hole_x = Cylinder(d=diameter, h=self.size, axis=Axis.X).at(
            -half, 0, 0
        )
        hole_y = Cylinder(d=diameter, h=self.size, axis=Axis.Y).at(
            0, -half, 0
        )
        hole_z = Cylinder(d=diameter, h=self.size, axis=Axis.Z).at(
            0, 0, -half
        )

        return body - (hole_x + hole_y + hole_z)
