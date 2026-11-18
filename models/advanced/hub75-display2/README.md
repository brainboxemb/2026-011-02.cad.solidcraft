# HUB75Display2

HUB75Display2 is the second HUB75 enclosure design. It is developed **in
parallel** with the existing [Wooden HUB75 Basic Box](../hub75_wood_frame/README.md).

The first revision intentionally starts from the same verified geometry and
parameter values as the current wooden display. That gives v1 and v2 a known
comparison point. From this baseline onward, changes to v2 do **not** need to
be copied back to v1.

## Independence

HUB75Display2 owns its own model-local:

- `scpf/model.py`;
- `scpf/parts/`;
- `scpf/assemblies/`;
- tests and native snapshot settings.

It does **not** import model-local assemblies from `hub75_wood_frame`.

Reusable physical parts remain shared from `models/components/`, including:

- `Hub75PanelBasic`;
- `CornerBracket`.

This avoids duplicating genuine cross-model components while allowing the
cabinet, glazing, placement and later v2-specific mechanics to diverge freely.

## Initial baseline

The initial v2 values are deliberately the same as the verified v1 design:

| Item | Baseline |
| --- | ---: |
| Opening | 844 × 362 mm |
| Panel count | 5 |
| Panel pitch | 160 mm |
| Panel recess | 25 mm |
| Frame wood | 12 mm |
| Rear board | 9 mm |
| Cabinet depth | 100 mm |
| Roof overhang | 10 mm front / 1 mm rear |
| Window | 840 × 360 × 4 mm |
| Corner brackets | 8 |

World axes and datums also start the same: X left/right, Y front/back and Z up,
with Y=0 at the wooden cabinet front and Z=0 at the outside bottom face.

## Parallel development

This page describes only the **parallel-development baseline**. New v2 design
choices should be documented here as they are introduced instead of silently
changing the v1 documentation.
