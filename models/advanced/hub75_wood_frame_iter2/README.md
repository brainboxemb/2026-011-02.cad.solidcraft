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

Two 12 mm vertical dividers split the lower compartment into three clear bays.
The ratio applies to the free space after subtracting both divider thicknesses:
**30% / 40% / 30%**. With the default 844 mm internal width this gives
**246 mm / 328 mm / 246 mm** clear openings, with divider centre-lines at
**X = -170 mm and +170 mm**.

## Rear side-wall recess

Like the second reference design, the lower storage section keeps the full
**100 mm** cabinet depth. Only the rear edge of the display section is reduced.
The current iteration-2 values are:

- rear recess depth: **50 mm**, leaving a 50 mm deep middle section;
- transition radius: **R20**;
- full-depth side wall above the intermediate shelf before the recess: **80 mm**;
- full-depth side wall below the roof after the recess: **80 mm**.

The recess is cut as a real rounded YZ profile in each 12 mm side wall. The
front edge remains straight. The rear board is temporarily disabled while this
rear-access geometry is being developed.

## Current main dimensions

| Item | Value |
| --- | ---: |
| Opening | 844 × 362 mm |
| Lower compartment clear height | 70 mm |
| Lower compartment bays | 246 / 328 / 246 mm clear (30 / 40 / 30%) |
| Lower divider plates | 2 × 12 mm |
| Panel count | 5 |
| Panel pitch | 160 mm |
| Panel recess | 25 mm |
| Frame wood | 12 mm |
| Rear board | temporarily disabled |
| Side-wall rear recess | 50 mm deep, R20, 80 mm full-depth top/bottom zones |
| Cabinet depth | 100 mm |
| Roof overhang | 10 mm front / 1 mm rear |
| Window | 840 × 360 × 4 mm |
| Corner brackets | 8 |

World axes remain X left/right, Y front/back and Z up, with Y=0 at the wooden
cabinet front and Z=0 at the outside bottom face.
