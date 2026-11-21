# CAD repository plan

This file is the current source of truth for unfinished model work in
`2026-011-02.cad.solidcraft`.

Permanent model requirements and design decisions belong with the owning model.
Forge API/compiler limitations belong in `lib.py.solidcraft.forge` and are
linked here when they block downstream CAD work.

## Current work

### Latch

Branch: `feature/latch`

Source reference: `models/advanced/latch/reference/latch.sc`

Goal: reconstruct the supplied native SolidCraft latch as readable SCPF while
preserving the native fabrication intent. Do not replace sheet-metal operations
or revolved fasteners with fused-solid approximations merely to make the model
compile.

Current source inventory:

- mounting foot: 2.0 mm sheet, 0.6 mm bend radius, K=0.4;
- operating handle: 1.6 mm sheet, 0.9 mm bend radius, K=0.4;
- pull bail: 2.0 mm sheet, 1.0 mm bend radius, K=0.4;
- locking spring/lip: 0.7 mm sheet, 0.8 mm bend radius, K=0.42;
- two pull-bail rivets and one countersunk locking-lip rivet use revolved
  profiles;
- one continuous hinge pin is cylindrical.

### Latch open design / Forge dependencies

The reference design deliberately stays authoritative while these API gaps are
open:

- Forge #567 — mixed line/arc closed Sketch profiles. Required by the sheet
  blanks; do not polygonize their arcs downstream.
- Forge #568 — native non-base sheet flange and sheet contour. Required by the
  mounting-foot hinge tabs and curled locking spring/lip.
- Forge #349 — `solid.revolve` coverage. Required by the three rivets.

Already available and expected to be reused:

- `Sketch.sheet_metal()` for native sheet bases and shared rules;
- `Shape.fold()` for the existing 25° and 90° folds;
- normal sketch cuts / Hole semantics where applicable;
- `Cylinder` for the hinge pin.

## Latch execution order

1. Keep the supplied `latch.sc` byte-identical in the model reference folder.
2. Record dimensions, feature history and sheet rules in the model README.
3. Add the SCPF model structure and parameter vocabulary without fake geometry.
4. Complete/qualify Forge #567 and use the resulting generic curve-profile API.
5. Rebuild the three primary sheet blanks and their existing folds.
6. Complete/qualify Forge #568 and add the hinge-tab flange and locking contour.
7. Complete the needed Revolve coverage under Forge #349 and model the rivets.
8. Add assembly placement/relationships from the native reference.
9. Add focused regression tests and native saved-design mutations.
10. Only then add the model to the normal native catalog and call it verified.
