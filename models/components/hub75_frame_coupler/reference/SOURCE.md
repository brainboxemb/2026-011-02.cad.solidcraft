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

The seam guide remains a straight source-footprint prism until public Forge
solid-loft authoring exists.  That bounded follow-up does not change owner or
public variant ids.


## Historical OpenSCAD frame contract

The migrated repository may use historical CAD only as geometry/design
reference. For Edge/Corner orientation the authoritative historical design is
`brainboxemb/2026-009-01.cad.HUB75-display-frame`.

Its horizontal-edge contract states:

- `X=0`: panel seam;
- `Y=0`: rear mounting plane;
- `Z=0`: nominal display edge;
- top-edge panel interior is **negative Z**;
- the base plate occupies the base side of the mounting plane;
- guides and reinforcement locators extend into the panel on the opposite
  depth side.

The Corner design uses the same rule: top always maps inward to negative Z;
left/right is supplied by the X-side orientation.

Do not fix visual orientation by mirroring individual holes, support rings or
paspads. The profile, guide shell, reinforcement features and surface pattern
must share one frame contract.
