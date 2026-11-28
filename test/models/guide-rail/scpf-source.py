"""Reusable guide rail with interchangeable fixed cross-sections.

`length` is the only native CAD parameter. `profile` is a non-parametric
component input selecting one fixed measured reference cross-section.
"""
from scpf import Polygon2D, Sketch, component

from models.components.guide_rail.scpf.profiles import get_profile


@component(include=("length",))
class GuideRail:
    length = 600.0
    profile = None

    def build(self):
        profile_data = get_profile(self.profile or "festool")
        points = [
            (f"p{index:03d}", point)
            for index, point in enumerate(profile_data.POINTS)
        ]

        with Sketch(
            name=f"Guide rail profile - {profile_data.PROFILE_NAME}",
            plane="XZ",
        ) as profile_sketch:
            Polygon2D(points, plane="XZ", world=True)

        return profile_sketch.extrude(
            self.length,
            sym=True,
        ).with_material(
            "Aluminium",
            density_g_cm3=2.70,
            color="#C4C8CB",
        )
