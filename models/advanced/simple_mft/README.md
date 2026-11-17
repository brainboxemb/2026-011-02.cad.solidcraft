# Simple MFT

This model is intentionally small in scope: **the worktop plate only**.

It uses the published Craftmaker replacement-top envelope as a convenient
plate size:

- 805 × 555 × 18 mm;
- 20 mm dog holes.

The hole layout is **not** presented as a measured Craftmaker S30 layout.
Instead this is our own simple MFT study with the standard 96 mm spacing:

- 7 columns × 5 rows;
- 96 mm pitch in X and Y;
- the complete grid is centred on the plate.

The earlier photo-based 80 mm estimate and the large clamp-slot placeholders
were removed. They were not verified dimensions and are not part of this
model.

## Native pattern

The SCPF source creates exactly one Ø20 through-hole and passes that cut
feature to `Shape.rectangular_pattern(...)`.

SolidCraft therefore owns one editable two-direction
`solid.pattern.rectangular` history feature. The 35 holes are **not** emitted
as 35 separate holes and are not expanded by a Python loop.

## Scope

Included:

- one 805 × 555 × 18 mm plate;
- one centred 7 × 5 MFT hole grid;
- Ø20 mm holes;
- 96 mm spacing.

Not included:

- clamp slots;
- frame or legs;
- guide rail;
- fence;
- dogs or clamps;
- claims about the actual Craftmaker S30 hole coordinates.

## Run

```powershell
python -m scpf models/advanced/simple_mft/scpf/model.py --out output/simple-mft.json
python -m scpf models/advanced/simple_mft/scpf/model.py --connect --new
```
