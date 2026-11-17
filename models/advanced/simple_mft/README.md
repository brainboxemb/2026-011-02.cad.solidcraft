# Simple MFT

This model is a photo/video-based study of the Craftmaker Pro Station S30
replacement worktop. It models the **worktop plate only**.

## Current geometry

Published replacement-top envelope:

- 805 × 555 × 18 mm;
- Ø20 mm dog holes.

Current design estimates derived from the visual references:

- 9 columns × 7 rows;
- 76 mm pitch in X and Y;
- 20 mm straight corner cuts;
- eight diagonal clamp slots;
- slot size currently estimated at 75 × 24 mm.

The 76 mm pitch, corner-cut size and slot dimensions are not presented as
manufacturer specifications.

## Native construction

The plate starts as one eight-point polygon and is extruded to 18 mm.

The dog holes use one native source hole and one two-direction rectangular
pattern for the complete 9 × 7 grid.

The clamp slots use SolidCraft's native Slot geometry. Four master slots are
placed symmetrically at grid index 2 from the centre. Each master slot is
patterned one 76 mm grid step farther outward along its diagonal arm, producing
two slots per arm and eight slots total.

The slot axes follow the X arms:

- north-west / south-east: \\
- north-east / south-west: /

This deliberately avoids eight unrelated literal XY placements.

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
