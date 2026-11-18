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

The second reference design also reduces the rear depth of the upper side-wall
section. Apply the same principle here while keeping the iteration-2 dimensions:

- bottom, intermediate shelf and lower dividers remain 100 mm deep;
- both side panels extend to 110 mm depth;
- the middle display-zone side wall is recessed 50 mm from the 110 mm rear
  edge, leaving 60 mm depth there;
- use R20 rounded transitions;
- keep at least 80 mm of full-depth side wall above the intermediate shelf;
- keep at least 80 mm of full-depth side wall below the roof;
- keep the lower storage-compartment side wall at the full 100 mm depth.

Model this as a separate `SideBoard` part with a rounded YZ recess. Do not
approximate the radius with straight polygon segments. The recess sketch is
attached to the side-wall body because Forge currently cannot use a standalone
`sketch_base_extrusion` as a boolean operand; that missing Forge capability is
tracked separately in Forge issue #354. The rear board remains temporarily
disabled while this rear-access shape is developed.

Add a first side-handle concept for visual evaluation. Each side gets one
vertical Ø22 mm beech roundwood rod centred in the 50 mm rear recess at Y=85.
Do not slot the roundwood around the 12 mm plywood. Instead keep the rod intact
and show two temporary printed sockets per side. The current sockets use a Ø34
outer sleeve, Ø22.6 bore and a short bridge to the recessed plywood edge. These
socket dimensions are concept values, not the final mounting design.

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
