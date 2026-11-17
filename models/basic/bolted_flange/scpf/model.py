"""Bolted flange from the official SolidCraft sample.

The model keeps one native source bolt-hole cut and repeats that feature with
one native circular history pattern. SCPF uses one name for an explicit Sketch
and its extrusion, so the source Sketch named "Bolt" is represented here as
"BoltHole"; SCPC keeps the original separate names exactly.
"""


class Flange:
    bolts = 6
    pcd = 70.0

    def build(self):
        with Sketch(name="Disc", plane="XY") as disc:
            Circle2D(d=100)
        flange = disc.extrude(10)

        with Sketch(name="Hub", on=flange, parent=Anchor.TOP) as hub:
            Circle2D(d=44)
        hub_feature = hub.extrude(16)
        flange = flange + hub_feature

        with Sketch(
            name="Bore",
            on=flange,
            plane="XY",
            origin=(0, 0, 0),
        ) as bore:
            Circle2D(d=24)
        bore_cut = bore.extrude(26)
        flange = flange - bore_cut

        with Sketch(
            name="BoltHole",
            on=flange,
            plane="XY",
            origin=(0, 0, 0),
        ) as bolt:
            bolt.add(
                Circle2D(d=9),
                offset=(self.pcd / 2, 0),
            )
        bolt_cut = bolt.extrude(10)
        flange = flange - bolt_cut

        return flange.circular_pattern(
            bolt_cut,
            axis=Axis.Z,
            count=self.bolts,
        )
