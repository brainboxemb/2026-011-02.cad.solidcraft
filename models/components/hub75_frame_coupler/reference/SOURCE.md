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

## Phase-1 geometry note

The source base/guide profiles are extracted from the retained native JSON.
The native edge/corner rail clearance and seam guide use shallow lofts; released
Forge v0.19 has no public solid-loft authoring API.  The initial Medium port uses
source entrance profiles as prismatic clearances and straight seam-guide prisms.
Those are bounded follow-up refinements within the same owner, not reasons to
split the family.
