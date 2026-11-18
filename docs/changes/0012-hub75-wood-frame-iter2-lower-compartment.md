# 0012 — Wooden HUB75 frame iteration 2 lower compartment

Issue: #154

## Problem

`WoodenHub75BoxIter2` was intentionally created as a copy of the verified first
wooden HUB75 enclosure. The second design now needs to start following the
older full display-case concept, beginning with the storage space below the
screen.

The OpenSCAD reference project
`brainboxemb/2026-006-02.cad.HUB75-display-case` uses a 70 mm clear lower
compartment. The SolidCraft design uses 12 mm frame plywood, so that reference
dimension must be combined with the current 12 mm material choice rather than
copying the old material thickness.

## Decision

Name this design as iteration 2 of the existing wooden frame: Python directory `models/advanced/hub75_wood_frame_iter2/`, top-level class `WoodenHub75BoxIter2`, and public catalog/URL slug `hub75-wood-frame-iter2`. Python paths use snake_case; the published slug uses kebab-case.

Keep Z=0 at the outside bottom face and use this vertical stack:

1. 12 mm bottom board;
2. 70 mm clear lower compartment;
3. 12 mm intermediate shelf;
4. 362 mm display opening;
5. 12 mm roof board.

Default total cabinet height is therefore 468 mm and the display opening starts
at Z=94 mm.

Add `lower_compartment_height = 70.0` as an editable native SolidCraft
parameter. The opening bottom is derived from that parameter and
`frame_wood_thickness`.

The side boards run continuously from the top of the bottom board to the
underside of the roof. The intermediate shelf sits between the two side walls
at the top of the lower compartment.

Add two vertical 12 mm lower-compartment dividers. The requested 30% / 40% /
30% ratio applies to the clear openings after subtracting both divider
thicknesses. At the default 844 mm internal width, 820 mm remains for the clear
bays, giving 246 mm / 328 mm / 246 mm. The divider centre-lines are therefore
X=-170 mm and X=+170 mm.

All display-dependent geometry must follow the derived opening datum:

- HUB75 panels;
- glazing frame;
- plexiglass window;
- roof;
- rear-board height;
- top corner brackets.

No occurrence gets a separate hard-coded 70, 82 or 94 mm placement.

Replace the previous rear-edge recess and roundwood-handle experiment with
closed hand openings cut directly into the plywood.

Use these hand-opening dimensions:

- side walls remain full 120 mm deep;
- each side-wall opening is 30 mm wide in Y;
- keep 20 mm of plywood between the opening and the 120 mm rear edge, so the
  opening spans Y=70..100;
- use **R10** rounded corners;
- keep the same vertical opening zone as before: local Z=162..364 by default;
- remove the separate roundwood, plastic rings and `SideHandles` assembly.

Keep the inset rear-board construction:

- bottom stays 120 mm deep;
- intermediate shelf and both lower dividers stop at 110 mm;
- 9 mm rear board occupies Y=111..120 between the side walls;
- roof remains 131 mm total: 10 mm front overhang + 120 mm cabinet + 1 mm rear;
- rear board gets two matching 30 mm wide R10 vertical openings, each 20 mm
  from its nearest side edge.

## Scope

This change creates the basic lower compartment, including its two vertical
divider plates. It does not yet add the 3 mm divider grooves/tongues, doors,
removable ground panels, hardware or other lower-compartment service details
from the OpenSCAD reference.

## Verification

- regression tests check the new native parameter;
- tests check the 12 + 70 + 12 stack and dependent command expressions;
- tests check two divider occurrences and the 30% / 40% / 30% clear-bay calculation;
- tests check the 50 mm side recess, R20 profile and the two 80 mm full-depth end zones;
- the five-panel X layout remains unchanged;
- a native mutation changes `lower_compartment_height` to 90 mm and verifies
  that the saved SolidCraft design rebuilds from the parameter;
- normal targeted CAD CI builds only the affected model and required dependencies.
