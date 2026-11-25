"""Native reconstruction of the supplied SolidCraft over-centre latch.

The byte-identical source lives in ../reference/latch.sc.  This model keeps the
five physical metal parts separate and reproduces the source sheet-metal,
revolve and cylinder history with released Forge primitives.

World axes follow the native latch document:
    X: latch length
    Y: latch width
    Z: height
"""

from scpf import (
    Anchor,
    Axis,
    Box,
    Cylinder,
    Hole,
    Placement,
    Sketch,
    component,
)

STEEL = dict(
    material="Galvanized steel",
    density_g_cm3=7.85,
    color="#B7BDC2",
)
SPRING_STEEL = dict(
    material="Spring steel",
    density_g_cm3=7.85,
    color="#9EA5AB",
)


def _steel(shape, *, spring=False):
    props = SPRING_STEEL if spring else STEEL
    return shape.with_material(
        props["material"],
        density_g_cm3=props["density_g_cm3"],
        color=props["color"],
    )


@component(include="*")
class LatchPullBail:
    """2 mm pull bail reconstructed from native features 33–41."""

    thickness = 2.0
    bend_radius = 1.0
    k_factor = 0.40
    pin_hole_diameter = 4.1

    def build(self):
        with Sketch(name="Pull bail blank", plane="XY") as blank:
            contour = blank.profile(start=(-42.16287547531802, 2.2))
            contour.line_to((42.16287547531802, 2.2))
            contour.arc_center_to(
                (42.16287547531802, 11.5),
                center=(42.16287547531802, 6.85),
                clockwise=False,
            )
            contour.line_to((28.077433388230816, 11.5))
            contour.line_to((11.577433388230814, 7.1))
            contour.line_to((-11.577433388230814, 7.1))
            contour.line_to((-28.077433388230816, 11.5))
            contour.line_to((-42.16287547531802, 11.5))
            contour.arc_center_to(
                (-42.16287547531802, 2.2),
                center=(-42.16287547531802, 6.85),
                clockwise=False,
            )
            contour.close()

        bail = blank.sheet_metal(
            thickness=self.thickness,
            bend_radius=self.bend_radius,
            k_factor=self.k_factor,
            rule_name="Pull bail 2 mm",
        )

        for x in (-42.16287547531801, 42.16287547531801):
            bail = bail + Hole(
                d=self.pin_hole_diameter,
                direction=(0, 0, -1),
            ).at(x, 6.0, self.thickness)

        # Native Fold7..Fold12.  The local XY coordinates are the original
        # source Sketch coordinates; the occurrence rotation maps them back to
        # the source YZ plane.
        bail = bail.fold(
            line=((37.35211495915475, 2.2), (37.35211495915475, 11.5)),
            angle=25,
            fixed=(0, 4.0, 0),
            position="start",
            flip=True,
        )
        bail = bail.fold(
            line=((34.37743338823081, 2.2), (34.37743338823081, 11.5)),
            angle=25,
            fixed=(0, 4.0, 0),
            position="start",
        )
        bail = bail.fold(
            line=((8.75, 2.2), (8.75, 7.1)),
            angle=90,
            fixed=(0, 4.0, 0),
            position="start",
        )
        bail = bail.fold(
            line=((-37.35211495915475, 11.5), (-37.35211495915475, 2.2)),
            angle=25,
            fixed=(0, 4.0, 0),
            position="start",
            flip=True,
        )
        bail = bail.fold(
            line=((-34.37743338823081, 11.5), (-34.37743338823081, 2.2)),
            angle=25,
            fixed=(0, 4.0, 0),
            position="start",
        )
        bail = bail.fold(
            line=((-8.75, 7.1), (-8.75, 2.2)),
            angle=90,
            fixed=(0, 4.0, 0),
            position="start",
        )
        return _steel(bail)


@component(include="*")
class LatchMountingFoot:
    """2 mm mounting foot and front hinge tabs from native features 44–51."""

    thickness = 2.0
    bend_radius = 0.6
    k_factor = 0.40
    mounting_hole_diameter = 4.2
    hinge_hole_diameter = 4.1
    locking_rivet_hole_diameter = 3.2

    def build(self):
        with Sketch(name="Mounting foot blank", plane="XY") as blank:
            contour = blank.profile(start=(27.0, -8.25))
            contour.line_to((40.0, -8.25))
            contour.line_to((40.0, -10.449114857512855))
            contour.line_to((41.75, -15.299114857512857))
            contour.arc_center_to(
                (49.25, -15.299114857512857),
                center=(45.5, -15.299114857512857),
                clockwise=False,
            )
            contour.line_to((51.0, -10.449114857512855))
            contour.line_to((51.0, -8.25))
            contour.line_to((55.5, -8.25))
            contour.arc_center_to(
                (58.5, -5.25),
                center=(55.5, -5.25),
                clockwise=False,
            )
            contour.line_to((58.5, 5.25))
            contour.arc_center_to(
                (55.5, 8.25),
                center=(55.5, 5.25),
                clockwise=False,
            )
            contour.line_to((51.0, 8.25))
            contour.line_to((51.0, 10.449114857512855))
            contour.line_to((49.25, 15.299114857512857))
            contour.arc_center_to(
                (41.75, 15.299114857512857),
                center=(45.5, 15.299114857512857),
                clockwise=False,
            )
            contour.line_to((40.0, 10.449114857512855))
            contour.line_to((40.0, 8.25))
            contour.line_to((27.0, 8.25))
            contour.line_to((25.5, 3.8))
            contour.line_to((15.5, 3.8))
            contour.line_to((15.5, -3.8))
            contour.line_to((25.5, -3.8))
            contour.line_to((27.0, -8.25))
            contour.close()

        foot = blank.sheet_metal(
            thickness=self.thickness,
            bend_radius=self.bend_radius,
            k_factor=self.k_factor,
            rule_name="Mounting foot 2 mm",
        )

        for x in (38.5, 52.5):
            foot = foot + Hole(
                d=self.mounting_hole_diameter,
                direction=(0, 0, -1),
            ).at(x, 0, self.thickness)

        for y in (-15.299114857512857, 15.299114857512857):
            foot = foot + Hole(
                d=self.hinge_hole_diameter,
                direction=(0, 0, -1),
            ).at(45.5, y, self.thickness)

        foot = foot.fold(
            line=((40.0, 8.25), (51.0, 8.25)),
            angle=90,
            fixed=(29.5, 0, 0),
            position="start",
        )
        foot = foot.fold(
            line=((51.0, -8.25), (40.0, -8.25)),
            angle=90,
            fixed=(29.5, 0, 0),
            position="start",
        )
        foot = foot.flange(
            edges=[(20.5, 3.8, 0), (20.5, -3.8, 0)],
            height=11.5,
            angle=90,
            position="outside",
            flip=True,
        )

        # Native feature 50/51 trims both raised hinge tabs with one XZ
        # profile and drills the common Ø3.9 front-hinge bore.
        with Sketch(
            name="Front hinge tab trim",
            plane="XZ",
            offset=-7.0,
        ) as trim:
            contour = trim.profile(start=(14.5, -7.3))
            contour.line_to((17.0, -7.3))
            contour.arc_center_to(
                (24.0, -7.3),
                center=(20.5, -7.3),
                clockwise=False,
            )
            contour.line_to((26.5, -7.3))
            contour.line_to((26.5, -13.3))
            contour.line_to((14.5, -13.3))
            contour.line_to((14.5, -7.3))
            contour.close()

        foot = foot - trim.extrude(14)
        foot = foot - Cylinder(
            d=3.9,
            h=14,
            axis=Axis.Y,
        ).at(20.5, 0, 7.3)

        # Native late locking-lip rivet hole plus its 0.4 mm underside seat.
        foot = foot - Cylinder(
            d=self.locking_rivet_hole_diameter,
            h=2.9,
            anchor=Anchor.BOTTOM,
        ).at(45.5, 0, 0, anchor=Anchor.BOTTOM)
        foot = foot - Cylinder(
            d=4.0,
            h=0.4,
            anchor=Anchor.BOTTOM,
        ).at(45.5, 0, 0, anchor=Anchor.BOTTOM)

        return _steel(foot)


@component(include="*")
class LatchHandle:
    """1.6 mm operating handle from native features 52–56 and 75–76."""

    thickness = 1.6
    bend_radius = 0.9
    k_factor = 0.40

    def build(self):
        # The native sheet_base uses flip=true.  Mirror the in-plane Y
        # coordinates here and rotate the completed occurrence 180° around X;
        # that maps local +Z material back to the native -Z sheet side without
        # introducing a non-native solid approximation.
        with Sketch(name="Operating handle blank", plane="XY") as blank:
            contour = blank.profile(start=(73.0, -8.169026343264141))
            contour.line_to((57.0, -17.76902634326414))
            contour.line_to((26.3, -17.76902634326414))
            contour.line_to((20.5, -16.46902634326414))
            contour.arc_center_to(
                (20.5, -9.26902634326414),
                center=(20.5, -12.869026343264142),
                clockwise=True,
            )
            contour.line_to((25.3, -9.26902634326414))
            contour.line_to((25.3, -5.75))
            contour.line_to((25.3, 5.75))
            contour.line_to((25.3, 9.26902634326414))
            contour.line_to((20.5, 9.26902634326414))
            contour.arc_center_to(
                (20.5, 16.46902634326414),
                center=(20.5, 12.869026343264142),
                clockwise=True,
            )
            contour.line_to((26.3, 17.76902634326414))
            contour.line_to((57.0, 17.76902634326414))
            contour.line_to((73.0, 8.169026343264141))
            contour.line_to((73.0, -8.169026343264141))
            contour.close()

        handle = blank.sheet_metal(
            thickness=self.thickness,
            bend_radius=self.bend_radius,
            k_factor=self.k_factor,
            rule_name="Operating handle 1.6 mm",
        )

        for x, source_y, diameter in (
            (33.5, 14.169026343264141, 4.1),
            (45.5, 12.71902634326414, 4.1),
            (20.5, 12.869026343264142, 3.9),
            (33.5, -14.169026343264141, 4.1),
            (45.5, -12.71902634326414, 4.1),
            (20.5, -12.869026343264142, 3.9),
        ):
            handle = handle + Hole(
                d=diameter,
                direction=(0, 0, -1),
            ).at(x, -source_y, self.thickness)

        handle = handle.fold(
            line=((25.3, -5.75), (73.0, -5.75)),
            angle=90,
            fixed=(36.5, 0, 0),
            position="start",
        )
        handle = handle.fold(
            line=((73.0, 5.75), (25.3, 5.75)),
            angle=90,
            fixed=(36.5, 0, 0),
            position="start",
        )

        # Native rectangular locking-lip opening (feature 75/76).  In this
        # local mirrored sheet it remains symmetric about Y=0.
        opening = Box(
            3.8,
            9.0,
            2.0,
            anchor=Anchor.BOTTOM,
        ).at(58.45, 0, 0, anchor=Anchor.BOTTOM)
        handle = handle - opening

        return _steel(handle)


@component(include="*")
class LatchLockingLip:
    """0.7 mm native contour-flange spring from source features 73–74."""

    width = 8.4
    thickness = 0.7
    bend_radius = 0.8
    k_factor = 0.42

    def build(self):
        with Sketch(name="Locking lip contour", plane="XZ") as sketch:
            chain = sketch.chain(start=(43.0, -2.0))
            chain.line_to((56.85, -2.0))
            chain.tangent_arc_to((58.35, -3.5))
            chain.line_to((58.35, -16.3))
            chain.tangent_arc_to((56.41340572836789, -14.61654428313933))
            path = chain.finish()

        lip = path.contour_flange(
            distance=self.width,
            thickness=self.thickness,
            bend_radius=self.bend_radius,
            k_factor=self.k_factor,
            rule_name="Locking spring 0.7 mm",
        )

        # Source feature 78 cuts the same Ø3.2 rivet hole through foot and lip.
        lip = lip - Cylinder(
            d=3.2,
            h=2.9,
            anchor=Anchor.BOTTOM,
        ).at(45.5, 4.2, 0, anchor=Anchor.BOTTOM)

        return _steel(lip, spring=True)


@component(include="*")
class LatchBailRivetLeft:
    def build(self):
        with Sketch(name="Left bail rivet profile", plane="XY") as profile:
            contour = profile.profile(start=(0.0, -6.25))
            for point in (
                (2.2, -6.25),
                (2.45, -6.45),
                (2.45, -6.63),
                (2.0, -6.63),
                (2.0, -10.47),
                (2.6, -10.47),
                (2.6, -10.92),
                (2.25, -11.12),
                (0.0, -11.12),
                (0.0, -6.25),
            ):
                contour.line_to(point)
            contour.close()
        return _steel(profile.revolve(axis=Axis.Y))


@component(include="*")
class LatchBailRivetRight:
    def build(self):
        with Sketch(name="Right bail rivet profile", plane="XY") as profile:
            contour = profile.profile(start=(0.0, 6.25))
            for point in (
                (2.2, 6.25),
                (2.45, 6.45),
                (2.45, 6.63),
                (2.0, 6.63),
                (2.0, 10.47),
                (2.6, 10.47),
                (2.6, 10.92),
                (2.25, 11.12),
                (0.0, 11.12),
                (0.0, 6.25),
            ):
                contour.line_to(point)
            contour.close()
        return _steel(profile.revolve(axis=Axis.Y))


@component(include="*")
class LatchHingePin:
    diameter = 3.8
    length = 16.9

    def build(self):
        return _steel(
            Cylinder(
                d=self.diameter,
                h=self.length,
                axis=Axis.Y,
            )
        )


@component(include="*")
class LatchLockingLipRivet:
    def build(self):
        # Source Sketch 71 uses +Z as its second in-plane direction.  Forge's
        # native XZ plane uses the opposite sketch-Y convention, hence the
        # negated second coordinates below.
        with Sketch(name="Locking lip rivet profile", plane="XZ") as profile:
            contour = profile.profile(start=(0.0, 0.0))
            for point in (
                (1.95, 0.0),
                (1.95, -0.37),
                (1.55, -0.37),
                (1.55, -2.72),
                (2.15, -2.72),
                (2.15, -3.04),
                (1.85, -3.24),
                (0.0, -3.24),
                (0.0, 0.0),
            ):
                contour.line_to(point)
            contour.close()
        return _steel(profile.revolve(axis=Axis.Z))


class Latch:
    """Complete source-faithful latch assembly."""

    def build(self):
        mounting_foot = LatchMountingFoot(
            placement=Placement(x=-36.5),
        )
        handle = LatchHandle(
            placement=Placement(
                x=-36.5,
                z=14.5,
                rotation=((1, 0, 0), 180),
            ),
        )
        pull_bail = LatchPullBail(
            placement=Placement(
                x=-36.5,
                rotation=((1, 1, 1), 120),
            ),
        )
        left_rivet = LatchBailRivetLeft(
            placement=Placement(x=-3.0, z=6.0),
        )
        right_rivet = LatchBailRivetRight(
            placement=Placement(x=-3.0, z=6.0),
        )
        hinge_pin = LatchHingePin(
            placement=Placement(x=-16.0, z=7.3),
        )
        locking_lip = LatchLockingLip(
            placement=Placement(x=-36.5, y=-4.2),
        )
        locking_rivet = LatchLockingLipRivet(
            placement=Placement(x=9.0),
        )

        return (
            mounting_foot
            + handle
            + pull_bail
            + left_rivet
            + right_rivet
            + hinge_pin
            + locking_lip
            + locking_rivet
        )


Latch()
