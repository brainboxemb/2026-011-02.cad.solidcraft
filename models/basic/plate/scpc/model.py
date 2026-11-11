"""Plate described with native SolidCraft commands, independent of SCPF.

SCPC does NOT call Forge. Open this file next to ../scpf/model.py
to compare the high-level and native-command approaches.
"""
from scpc import Script

script = Script()
for name, value in (("length", 100), ("width", 60), ("thickness", 10)):
    script.add("parameters.add", name=name, expression=str(value), unit="mm")

script.add("sketch.create", plane="XY", name="Plate footprint")
script.add("sketch.rectangle.two_point",
           p0=["-length / 2", "-width / 2"],
           p1=["length / 2", "width / 2"])
script.add("sketch.finish")
script.add("solid.extrude", distance="thickness", body_name="Plate")
script.add("solid.fillet", body="Plate", radius=2,
           edges=[[-50, -30, 5], [50, -30, 5],
                  [50, 30, 5], [-50, 30, 5]])

for x, y in ((-35, -15), (35, -15), (35, 15), (-35, 15)):
    script.add("solid.hole", position=[x, y, 10],
               diameter=8, targets=["Plate"])
