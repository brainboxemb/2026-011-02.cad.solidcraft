# Simple MFT

This model is a photo/video-based study of the Craftmaker Pro Station S30
replacement worktop. It models the **worktop plate only**.

## Current geometry

Published replacement-top envelope:

- 805 × 555 × 18 mm;
- Ø20 mm dog holes.

Current design estimates derived from the visual references and the SolidCraft
reference model:

- 9 columns × 7 rows;
- 76 mm pitch in X and Y;
- 20 mm straight corner cuts;
- four diagonal clamp slots;
- slot width currently estimated at 24 mm;
- each slot follows three diagonal grid positions: index 1, 2 and 3 from the
  centre.

The 76 mm pitch, corner-cut size and slot width are not presented as
manufacturer specifications.

With a 76 mm square grid, two diagonal grid steps are:

```text
2 × sqrt(2) × 76 mm = 214.96 mm
```

That is the centre-to-centre distance between the round ends of each Slot. With
a 24 mm slot width, the resulting overall capsule length is about 238.96 mm.
There is therefore no separate 75 mm slot-length parameter.

## Native construction

The model targets the pinned **SCPF 0.6.1** release.

The plate starts as one eight-point polygon and is extruded to 18 mm.

The dog holes use one native source hole and one two-direction rectangular
feature pattern for the complete 9 × 7 grid.

The clamp slots use SolidCraft's native
`SlotCenterToCenter2D` construction. The end-cap centres are placed on grid
indices 1 and 3 on each diagonal arm; grid index 2 lies on the same slot axis.
This directly represents one continuous slot crossing three dog-hole positions
instead of patterning several unrelated short slots.

The four arms are:

- north-east: `(76, 76) -> (228, 228)`;
- north-west: `(-76, 76) -> (-228, 228)`;
- south-west: `(-76, -76) -> (-228, -228)`;
- south-east: `(76, -76) -> (228, -228)`.

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
