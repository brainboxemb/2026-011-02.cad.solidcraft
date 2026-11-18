# WoodenHub75BoxIter2

WoodenHub75BoxIter2 is the second HUB75 enclosure design. It is developed **in
parallel** with the existing [Wooden HUB75 Basic Box](../hub75_wood_frame/README.md).

Iteration 2 started from the verified `hub75_wood_frame` geometry so both
iterations had a known comparison point. It now evolves independently.

## Independence

WoodenHub75BoxIter2 owns its own model-local:

- `scpf/model.py`;
- `scpf/parts/`;
- `scpf/assemblies/`;
- tests and native snapshot settings.

It does **not** import model-local assemblies from `hub75_wood_frame`.

Reusable physical parts remain shared from `models/components/`, including:

- `Hub75PanelBasic`;
- `CornerBracket`.

## Lower storage compartment

The first iteration-2 geometry change adds the lower compartment from the older
HUB75 display-case concept while keeping the SolidCraft design's 12 mm plywood.

Reference design:

- `brainboxemb/2026-006-02.cad.HUB75-display-case`;
- its lower compartment uses 70 mm clear internal height.

The SolidCraft vertical stack is:

| Section | Height |
| --- | ---: |
| Bottom board | 12 mm |
| Clear lower compartment | 70 mm |
| Intermediate shelf | 12 mm |
| Display opening | 362 mm |
| Roof board | 12 mm |
| **Total cabinet height** | **468 mm** |

The display opening therefore starts at **Z=94 mm**. The five HUB75 panels,
glazing frame and plexiglass all use that derived opening datum instead of a
fixed occurrence offset.

`lower_compartment_height` is an editable native SolidCraft parameter. Changing
it moves the intermediate shelf, display opening, roof, rear-board height and
top corner brackets together. The lower outside cabinet datum remains Z=0.

## Current main dimensions

| Item | Value |
| --- | ---: |
| Opening | 844 × 362 mm |
| Lower compartment clear height | 70 mm |
| Panel count | 5 |
| Panel pitch | 160 mm |
| Panel recess | 25 mm |
| Frame wood | 12 mm |
| Rear board | 9 mm |
| Cabinet depth | 100 mm |
| Roof overhang | 10 mm front / 1 mm rear |
| Window | 840 × 360 × 4 mm |
| Corner brackets | 8 |

World axes remain X left/right, Y front/back and Z up, with Y=0 at the wooden
cabinet front and Z=0 at the outside bottom face.
