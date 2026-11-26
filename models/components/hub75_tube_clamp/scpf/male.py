"""Male-dovetail HUB75 tube-clamp variant from the retained SolidCraft source."""

from math import radians, tan

from scpf import (
    Always,
    ConfigRule,
    Configure,
    DriveParameter,
    Param,
    Sketch,
    component,
)

from models.components.hub75_tube_clamp.scpf.common import (
    CLAMP_WALL,
    CLAMP_WIDTH,
    DOVE_ANGLE,
    DOVE_DEPTH,
    DOVE_GROOVE_FLAT,
    DOVE_HEAD,
    DOVE_LAND_HEAD,
    DOVE_LAND_ROOT,
    DOVE_ROUND,
    DOVE_RUN,
    _open_clamp_ring,
)


def _closed_profile(sketch, points):
    """Add one exact straight-segment source loop."""
    profile = sketch.profile(start=points[0])
    for point in points[1:]:
        profile.line_to(point)
    profile.line_to(points[0])
    profile.close()


def _male_dovetail_profile(*, dove_datum, web_front):
    """Feature 22: Symmetrische groeven met vlakke bodem."""
    angle = radians(DOVE_ANGLE)
    dove_neck = DOVE_HEAD - 2.0 * (
        DOVE_DEPTH - DOVE_LAND_ROOT - DOVE_LAND_HEAD
    ) * tan(angle)

    root_x = -dove_datum - DOVE_LAND_ROOT
    groove_x = root_x + DOVE_GROOVE_FLAT
    head_transition_x = root_x + (
        DOVE_HEAD - dove_neck
    ) / (2.0 * tan(angle))
    outer_x = -dove_datum - DOVE_DEPTH

    points = [
        (outer_x + DOVE_ROUND, DOVE_HEAD / 2.0),
        (outer_x + DOVE_LAND_HEAD, DOVE_HEAD / 2.0),
        (root_x, dove_neck / 2.0),
        (groove_x, dove_neck / 2.0),
        (head_transition_x, DOVE_HEAD / 2.0),
        (-web_front, DOVE_HEAD / 2.0),
        (-web_front, -DOVE_HEAD / 2.0),
        (head_transition_x, -DOVE_HEAD / 2.0),
        (groove_x, -dove_neck / 2.0),
        (root_x, -dove_neck / 2.0),
        (outer_x + DOVE_LAND_HEAD, -DOVE_HEAD / 2.0),
        (outer_x + DOVE_ROUND, -DOVE_HEAD / 2.0),
        (outer_x, -DOVE_HEAD / 2.0 + DOVE_ROUND),
        (outer_x, DOVE_HEAD / 2.0 - DOVE_ROUND),
    ]

    with Sketch(
        name="Symmetrische groeven met vlakke bodem",
        plane="XZ",
        offset=-DOVE_RUN / 2.0,
    ) as sketch:
        _closed_profile(sketch, points)

    return sketch


def _male_flank_correction(*, dove_datum):
    """Feature 24: Spiegelbeeldige correctie van de rugflanken."""
    angle = radians(DOVE_ANGLE)
    dove_neck = DOVE_HEAD - 2.0 * (
        DOVE_DEPTH - DOVE_LAND_ROOT - DOVE_LAND_HEAD
    ) * tan(angle)

    root_x = -dove_datum - DOVE_LAND_ROOT
    mid_x = root_x + DOVE_GROOVE_FLAT / 2.0
    groove_x = root_x + DOVE_GROOVE_FLAT
    outer_x = groove_x + (
        (DOVE_HEAD - dove_neck) / 2.0 + 0.1
    ) / tan(angle)

    lower = [
        (mid_x, -dove_neck / 2.0 - 0.05),
        (groove_x, -dove_neck / 2.0),
        (outer_x, -DOVE_HEAD / 2.0 - 0.1),
        (mid_x, -DOVE_HEAD / 2.0 - 0.1),
    ]
    upper = [
        (mid_x, dove_neck / 2.0 + 0.05),
        (groove_x, dove_neck / 2.0),
        (outer_x, DOVE_HEAD / 2.0 + 0.1),
        (mid_x, DOVE_HEAD / 2.0 + 0.1),
    ]

    with Sketch(
        name="Spiegelbeeldige correctie van de rugflanken",
        plane="XZ",
        offset=-DOVE_RUN / 2.0 - 0.1,
    ) as sketch:
        _closed_profile(sketch, lower)
        _closed_profile(sketch, upper)

    return sketch


@component(include=("tube_d", "clamp_interference", "clamp_bore"))
class Hub75TubeClampMale:
    """Loose clamp with the final active protruding male dovetail interface."""

    tube_d = 10.0
    clamp_interference = 0.4
    clamp_bore = 9.6

    def build(self):
        clamp_r = self.clamp_bore / 2.0
        clamp_r_out = clamp_r + CLAMP_WALL

        dove_datum = (
            self.tube_d / 2.0
            + CLAMP_WALL
            - self.clamp_interference / 2.0
        )
        web_front = self.tube_d / 2.0 + 0.65

        ring_sketch = _open_clamp_ring(
            clamp_r=clamp_r,
            clamp_r_out=clamp_r_out,
        )
        body = ring_sketch.extrude(CLAMP_WIDTH)

        dovetail = _male_dovetail_profile(
            dove_datum=dove_datum,
            web_front=web_front,
        )
        body = body + dovetail.extrude(DOVE_RUN)

        correction = _male_flank_correction(dove_datum=dove_datum)
        body = body - correction.extrude(DOVE_RUN + 0.2)

        return body


class Hub75TubeClampMaleCatalog:
    """Standalone male-dovetail manufacturing document; Free by default."""

    tube_d = 10.0
    clamp_interference = 0.4
    clamp_bore = 9.6

    def build(self):
        clamp = Hub75TubeClampMale(
            tube_d=self.tube_d,
            clamp_interference=self.clamp_interference,
            clamp_bore=self.clamp_bore,
        )
        return Configure(
            clamp,
            active="Free",
            columns=(Param(self.clamp_bore),),
            rows={
                "Free": ("tube_d-clamp_interference",),
            },
            rules=(
                ConfigRule(
                    "installed",
                    "Installed",
                    enabled=False,
                    condition=Always(),
                    effect=DriveParameter(self.clamp_bore, self.tube_d),
                ),
            ),
        )


Hub75TubeClampMaleCatalog()
