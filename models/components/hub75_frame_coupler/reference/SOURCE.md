# HUB75 frame-coupler source

The retained reference file `hub75-screen-2panel-couplers.json` is the native
SolidCraft design supplied for this family.

Source SHA-256:

```text
94d64ddeab1e1f3acce5840fc634c7233b1704c25f2e0fea4c509a215fbf4456
```

## Physical components

The native design contains four coupler definitions:

- `Middle coupler`;
- `Edge coupler`;
- `Corner coupler links`;
- `Corner coupler rechts`.

The CAD catalog maps those to one physical owner with four public build
variants.

## Active source configuration

The supplied native configuration table has rows `Small`, `Medium` and
`Large`.  The active row is `Medium`.

Medium values used by this initial Forge port:

| parameter | value |
| --- | ---: |
| `mid_size` | 80 mm |
| `mid_wall` | 4 mm |
| `mid_base` | 3 mm |
| `mid_guide` | 6 mm |
| `mid_fit` | 0.25 mm |

The native Medium row suppresses:

- feature 122, `Edge coupler doorvoer paneelpen`;
- feature 136, `Corner coupler rechts doorvoer paneelpen`.

These features are intentionally absent from the fixed Medium Forge port.

## Forge configuration follow-up

Native SolidCraft configuration-table authoring is tracked in
`brainboxemb/lib.py.solidcraft.forge#216`.

Until that capability is released, this owner stays explicitly Medium-only.
Do not emulate Small/Large with CAD-local Python branching.  The future change
must add the native configuration layer while preserving this owner and the
four public variant ids.

## Medium geometry mapping

The source base/guide profiles are extracted from the retained native JSON.

The late source reference pattern is also part of the Medium geometry:

- features 145–152 cut the shallow reference tick marks;
- features 153–164 cut Ø3 mm blind reference holes with tapered Ø2 mm bottoms;
- effective off-body suppression placeholders in those source sketches are not
  emitted as Forge cuts.

The native Edge and Corner rail clearance is a two-section shallow loft.
Released Forge v0.19 has no public solid-loft authoring API, so the CAD owner
uses twelve overlapping slices interpolated between the exact source entrance
and insertion-depth sections.  This preserves both native sections and removes
the visible fin/lip artifact produced by the former one-profile prism.

The Middle and Edge seam guides are native two-section loft joins. Released
Forge v0.19 has no public solid-loft authoring API, so both are represented by
overlapping slices interpolated between the exact native foot and tip sections.
Edge also applies the native guide-end rounding cut from features 137–138.

These bounded lowering details preserve the same owner and public variant ids.


## Edge / Corner base-guide split

The historical OpenSCAD production design in
`brainboxemb/2026-009-01.cad.HUB75-display-frame` is the geometry/design
reference for the Edge and Corner construction.

Its rear mounting plane separates two physical regions:

- the **3 mm base plate** extends away from the panel;
- the **6 mm guide walls/ridges** extend into the rear-panel geometry;
- screw bores and mounting-tube pockets belong to the base;
- reinforcement relief belongs to the guide region;
- locator pads/pins extend from the mounting plane into the panel.

The first Medium Forge port incorrectly extruded the complete Edge/Corner
profile through `mid_base + mid_guide` as one 9 mm stock and then cut into it.
That leaves profile material in the guide region where only fitted walls/ridges
should exist and makes the circular reinforcement/mounting features appear on
the wrong side of the part.

The corrected Forge construction keeps base and guide volumes separate and
joins them only after their own source-derived operations are complete.


## Edge T-profile boundary

Native feature 89, `Edge T-profiel begrenzen`, removes the outside (+Z) stem
of the pre-clip rounded plus.

Its absolute SolidCraft start is:

`panel_h - edge_outer_z + 1 mm`

so after normalization around the nominal panel-edge datum the local start is:

`-edge_outer_z + 1 mm`

For Medium, `edge_outer_z = -2.855 mm`, therefore the correct local cut starts
at **+3.855 mm**. A previous Forge lowering incorrectly used
`edge_outer_z + 1 mm = -1.855 mm`; that cut through the horizontal arm and
visibly separated the reinforcement volumes from the T body.

The historical TOP-edge clip below is the authoritative equivalent construction.


## Edge T-profile clip

The historical horizontal-edge production source first creates a rounded
`+` profile and then intersects it with a top-edge window:

```text
retain complete horizontal arm
retain only inward (-Z) vertical stem
remove the outside (+Z) half of the stem
```

The window top is
`hub75_horizontal_edge_coupler_outer_projection() + 1 mm`, matching the
historical source margin.

The retained native SolidCraft feature profile represented the pre-clip rounded
cross. Forge therefore applies this source window explicitly before mounting,
guide and surface-detail operations.


## Native XZ sketch frame

The retained SolidCraft source sketches use the native `XZ` origin plane.
On that native plane, sketch coordinates are oriented as:

- sketch U -> world +X;
- sketch V -> world -Z;
- positive extrusion -> world +Y.

The extracted `source_data.py` loops are intentionally stored in ordinary
physical local `(X, Z)` coordinates. Forge therefore lowers every source loop
through one shared boundary conversion:

```text
physical (x, z) -> native XZ sketch (x, -z)
```

Arc winding is reversed at the same reflection boundary.

This is essential for Edge/Corner source fidelity. Primitive cylinders and
locator pads already use ordinary world XYZ coordinates, so omitting this
single reflection places the source profile on the opposite Z side from its
reinforcement/mounting features.
