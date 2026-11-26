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

Small/Medium/Large adoption remains CAD #189. Released Forge v0.23.0 can drive
the numeric child parameters, but parent suppression of an authored feature
inside a reusable child still requires Forge #380.

Until that public contract is released, this owner stays explicitly
Medium-only. Do not emulate Small/Large with CAD-local Python branching.

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

The extracted `source_data.py` loops are normalized to each reusable
coupler's **physical local (X, Z)** frame. The historical production source
uses negative Z as the inward direction for the top Edge and Corner variants.

SolidCraft's native `XZ` sketch coordinates use the opposite sign for sketch
V versus physical Z. Forge therefore applies one boundary conversion:

```text
physical (x, z) -> native XZ sketch (x, -z)
```

Arc winding reverses at the same reflection boundary.

Durable review after PR #187 proved why this conversion must not be omitted:
the Edge T profile retained the outside stem while its world-XYZ bushing
supports remained at the inward mounting positions, leaving two detached round
features. Edge, Corner Left and Corner Right must all use this same conversion
for source-derived loops; primitive supports, mounting cuts and locator pads
remain in ordinary world XYZ.

## Tube-ready Edge / Corner variants

The retained assembly source later adds loose-clamp interfaces to the accepted
Medium Edge and Corner components. The final active source state is deliberately
narrower than several earlier experiments in the same timeline.

The tube-ready Edge variant ports the final active chain:

- feature 189, `Vrijloop voor naar binnen geplaatste klemmen`, 3 mm cut;
- feature 191, `Z-schuifrails op 40 mm hartafstand`, 14.75 mm join;
- feature 195, `Vrijloop voor klemboog aan de binnenzijde`, 0.45 mm cut;
- feature 198, `Tapse invoer zwaluwstaartrails`, native asymmetric
  0.18 / 0.65 mm chamfer;
- features 226/227, `Symmetrische bulten met R5-overgangen`, 2.45 mm join;
- features 228/229, `Doorgetrokken basisplaat rondom de twee klemmen`,
  3.9 mm join;
- feature 230, `Referentiepatroon op symmetrische rug`, which re-cuts source
  sketch-147 loops l93–l100 in the newly added rear material.

The tube-ready Corner variants port only:

- feature 213, `Inschuifuitsparingen voor hoekschuifklemmen`, 18.2 mm cut;
- feature 214, `Vrijloop Ø10 buis in de corner brackets`, Ø10.5 mm clearance;
- feature 216, `Zwaluwstaartrails voor de hoekschuifklemmen`, 14.75 mm join;
- features 217/218, native asymmetric 0.18 / 0.65 mm entry chamfers.

The rail profile is the same authored eight-line profile in all three variants.
Its center is X=±20 mm for Edge and local X=+7/-7 mm for left/right Corner.
The source component placements normalize the source sketch planes from world
Z=321.8 / 322 / 323.55 mm to local Z=1.8 / 2 / 3.55 mm.

Suppressed source experiments 177, 179, 185, 187, 193, 197, 207, 208 and 211
are not production geometry and are intentionally absent. Features 226–230 are
the later active replacement for those abandoned rear/base experiments and are
therefore retained.

The loose clamp remains a separate physical component. Free / Installed state
belongs to the assembly/configuration layer and is not fused into these
couplers.



## Alternate female receiver tube interface

New supplied total-model evidence:
- JSON `hub75-screen-2panel-couplers-clamp(1).json`;
  SHA-256 `876bd8032ee18318bb06955be2400f72554c4f6d2f33615bfb10258287080a53`;
- SolidCraft container `hub75-screen-2panel-couplers-clamp(1).sc`;
  SHA-256 `f91124cd49369d261e8ad1dc271e77ff60c5ec09341266e48b4a68a0e867fa92`.

The connected repository write path cannot stream these large/binary source
files byte-for-byte, so their exact supplied filenames and digests are retained
here rather than committing a partial or reconstructed source file.

The source keeps the common tube clearances/support history but suppresses the
older protruding rail interface:
- Edge rail #191 and entry chamfer #198 are suppressed;
- Corner rail #216 and chamfers #217/#218 are suppressed.

The final alternate interface is:
- #234 `Voeten voor ontvangende zwaluwstaarten`, normalized local Z=1.2 mm;
- #235 join depth 15.55 mm;
- #236 `Zwaluwstaartprofielen met speling`, normalized local Z=1.8 mm;
- #237 `Vrouwelijke zwaluwstaartgroeven met aanslag`, cut depth 18.7 mm.

`dove_fit = 0.2 mm`. One shared 12-point receiver template reproduces all
four source instances exactly. Edge centers are local X=±20 mm; Corner centers
are local X=+7/-7 mm. The 16 mm receiver support template is shared as well.

This is an alternate physical interface, not additive geometry: the existing
public tube variants keep their protruding rails, while the new receiver
variants replace those rails with female grooves for the male clamp.
