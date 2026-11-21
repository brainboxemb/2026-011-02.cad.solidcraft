# Latch

Work-in-progress reconstruction of the supplied native SolidCraft latch.

The reference file is kept unchanged at
`reference/latch.sc`. It is the geometry/history source of truth while the
SCPF reconstruction is incomplete.

## Reference design

SolidCraft document format: `solidcraft/63`.

Primary design parameters from the native file:

| Parameter | Value |
| --- | ---: |
| overall length | 73 mm |
| mounting-foot start | 15.5 mm |
| mounting-foot length | 43 mm |
| mounting-foot width | 16.5 mm |
| mounting-foot thickness | 2.0 mm |
| first mounting-hole offset | 23 mm |
| mounting-hole pitch | 14 mm |
| mounting-hole diameter | 4.2 mm |
| operating-handle width | 16.5 mm |
| nominal latch height | 14.5 mm |
| pull-bail width | 23.5 mm |
| main hinge X | 45.5 mm |
| main hinge Z | 7.45 mm |
| pull-bail pin X | 33.5 mm |
| pull-bail pin Z | 6.0 mm |
| pull-bail pin diameter | 4.0 mm |
| front hinge X | 20.5 mm |
| front hinge Z | 7.3 mm |
| front hinge pin diameter | 3.8 mm |
| nominal clearance | 0.1 mm |
| locking-lip width | 8.4 mm |
| locking-lip thickness | 0.7 mm |

## Native sheet rules

| Part | Thickness | Bend radius | K-factor |
| --- | ---: | ---: | ---: |
| Mounting foot | 2.0 mm | 0.6 mm | 0.40 |
| Operating handle | 1.6 mm | 0.9 mm | 0.40 |
| Pull bail | 2.0 mm | 1.0 mm | 0.40 |
| Locking spring/lip | 0.7 mm | 0.8 mm | 0.42 |

## Native history inventory

The supplied design contains:

- pull-bail flat blank, pin-hole cut and six sheet folds;
- mounting-foot flat blank, mounting/pin-hole cuts, two folds and a separate
  90° sheet flange for the front hinge tabs;
- front-hinge trimming/drilling;
- operating-handle flat blank, hole cuts and two folds;
- two revolved pull-bail rivets;
- one continuous cylindrical hinge pin;
- one revolved countersunk locking-lip rivet;
- one native sheet-contour locking spring/lip;
- rectangular locking-lip opening and final rivet-hole/countersink operations.

The blank sketches are not simple polygons: the pull bail, mounting foot and
handle all use connected straight segments plus circular arcs. Those arcs are
part of the intended native design and must not be replaced by faceted
approximations.

## Open design / Forge dependencies

This model intentionally waits for generic Forge capabilities instead of
carrying product-specific workarounds.

- [Forge #567](https://github.com/brainboxemb/lib.py.solidcraft.forge/issues/567)
  — connected mixed line/arc closed Sketch profiles.
- [Forge #568](https://github.com/brainboxemb/lib.py.solidcraft.forge/issues/568)
  — native sheet flange and sheet contour.
- [Forge #349](https://github.com/brainboxemb/lib.py.solidcraft.forge/issues/349)
  — remaining SolidCraft create-feature coverage, including Revolve.

Already usable: native sheet base creation, native fold, normal cuts/holes and
Cylinder.

See the repository-wide `docs/plan.md` for execution order.
