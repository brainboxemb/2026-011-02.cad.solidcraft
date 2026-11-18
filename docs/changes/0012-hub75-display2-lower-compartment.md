# 0012 — HUB75Display2 lower compartment

Issue: #154

## Problem

`HUB75Display2` was intentionally created as a copy of the verified first
wooden HUB75 enclosure. The second design now needs to start following the
older full display-case concept, beginning with the storage space below the
screen.

The OpenSCAD reference project
`brainboxemb/2026-006-02.cad.HUB75-display-case` uses a 70 mm clear lower
compartment. The SolidCraft design uses 12 mm frame plywood, so that reference
dimension must be combined with the current 12 mm material choice rather than
copying the old material thickness.

## Decision

Keep the Python model directory as `models/advanced/hub75_display2/`. The public model slug remains `hub75-display2`; the hyphen belongs in the URL/CI slug, not in a Python package path.

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
underside of the roof. The intermediate shelf spans the cabinet width at the
top of the lower compartment.

All display-dependent geometry must follow the derived opening datum:

- HUB75 panels;
- glazing frame;
- plexiglass window;
- roof;
- rear-board height;
- top corner brackets.

No occurrence gets a separate hard-coded 70, 82 or 94 mm placement.

## Scope

This change creates only the basic lower compartment volume. It does not yet
add divider walls, doors, removable ground panels, hardware or lower-compartment
service details from the OpenSCAD reference.

## Verification

- regression tests check the new native parameter;
- tests check the 12 + 70 + 12 stack and dependent command expressions;
- the five-panel X layout remains unchanged;
- a native mutation changes `lower_compartment_height` to 90 mm and verifies
  that the saved SolidCraft design rebuilds from the parameter;
- normal targeted CAD CI builds only the affected model and required dependencies.
