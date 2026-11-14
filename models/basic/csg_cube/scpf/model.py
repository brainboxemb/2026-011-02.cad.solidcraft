class CsgCube:
    size = 50

    def build(self):
        body = Sphere(self.size / 1.5) & Box(self.size, self.size, self.size)
        diameter = self.size / 1.5

        hole_x = Cylinder(d=diameter, h=self.size, axis=Axis.X).at(body)
        hole_y = Cylinder(d=diameter, h=self.size, axis=Axis.Y).at(body)
        hole_z = Cylinder(d=diameter, h=self.size, axis=Axis.Z).at(body)

        return body - (hole_x + hole_y + hole_z)
