"""Reusable loose Ø10 tube clamp from the retained native source."""

from scpf import Sketch, component

from models.components.hub75_tube_clamp.scpf.source_data import (
    BACK_LOOP,
    FREE,
    RING_LOOP,
    SLOT_LOOP,
)


def _add_loop(sketch, loop):
    contour = sketch.profile(start=tuple(loop["start"]))
    for segment in loop["segments"]:
        end = tuple(segment["end"])
        if segment["kind"] == "line":
            contour.line_to(end)
        elif segment["kind"] == "arc":
            contour.arc_center_to(
                end,
                center=tuple(segment["center"]),
                clockwise=segment["clockwise"],
            )
        else:
            raise ValueError(f"unsupported source segment {segment['kind']!r}")
    contour.close()


@component
class Hub75TubeClamp10mm:
    """Free/print-state loose clamp used by Edge and Corner tube interfaces."""

    def build(self):
        # Source feature 1/2: open elastic clamp ring in the native XY frame.
        with Sketch(
            name="Open clamp ring",
            plane="XY",
            offset=-FREE["clamp_width"] / 2.0,
        ) as ring_sketch:
            _add_loop(ring_sketch, RING_LOOP)
        body = ring_sketch.extrude(FREE["clamp_width"])

        # Source feature 12/13: low integrated rounded back for the slide slot.
        with Sketch(
            name="Integrated slide back",
            plane="XZ",
            offset=-FREE["dove_run"] / 2.0,
        ) as back_sketch:
            _add_loop(back_sketch, BACK_LOOP)
        body = body + back_sketch.extrude(FREE["dove_run"])

        # Source feature 14/15: rounded dovetail-style slide slot. The 1 mm
        # source stop remains closed at the positive-Y end.
        with Sketch(
            name="Slide slot",
            plane="XZ",
            offset=-FREE["dove_run"] / 2.0 - 0.05,
        ) as slot_sketch:
            _add_loop(slot_sketch, SLOT_LOOP)
        body = body - slot_sketch.extrude(
            FREE["dove_run"] - FREE["slot_stop"] + 0.05
        )

        return body


Hub75TubeClamp10mm()
