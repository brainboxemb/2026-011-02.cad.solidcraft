# Simple MFT

This model is a photo/video-based study of the Craftmaker Pro Station S30
replacement worktop. It models the **worktop plate only**.

## 2D expectation

![Simple MFT expected top view](expected-top-view.svg)

The 2D expectation is the geometry reference for the SCPF model. It is kept
next to the model so slot placement can be reviewed without opening SolidCraft.

## Current geometry

Published replacement-top envelope:

- 805 × 555 × 18 mm;
- Ø20 mm dog holes.

Current design estimates:

- 9 columns × 7 rows;
- 76 mm pitch in X and Y;
- 20 mm straight corner cuts;
- slot width currently estimated at 24 mm;
- four diagonal arms;
- three diagonal dog-hole positions per arm;
- two slot segments per arm: grid index 1 -> 2 and grid index 2 -> 3;
- no slot from the plate centre to grid index 1.

The 76 mm pitch, corner-cut size and slot width are not presented as
manufacturer specifications.

One diagonal grid step is:

```text
sqrt(2) × 76 mm = 107.48 mm
```

That is the centre-to-centre distance used for each Slot segment.

## Native construction

The model targets the pinned **SCPF 0.6.1** release.

The plate starts as one eight-point polygon and is extruded to 18 mm.

The dog holes use one native source hole and one two-direction rectangular
feature pattern for the complete 9 × 7 grid.

The clamp layout uses eight native `SlotCenterToCenter2D` profiles. Each
diagonal arm contains two segments connecting three dog-hole positions:

```text
centre
  |
  |   no slot
  |
index 1 ===== index 2 ===== index 3
```

The four arms are mirrored around the plate centre.

## Scope

Not included:

- frame or legs;
- guide rail;
- fence;
- dogs or clamps;
- logos and printed markings.

## Run

```powershell
python -m scpf models/advanced/simple_mft/scpf/model.py --out output/simple-mft.json
python -m scpf models/advanced/simple_mft/scpf/model.py --connect --new
```
