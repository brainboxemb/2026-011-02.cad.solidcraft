# Simple MFT

This model is a photo-based study of the CRAFTMAKER ProStation S30 replacement
worktop. It models the **worktop plate only**.

## Reference photo

![CRAFTMAKER ProStation S30 front reference](https://cdn.myshoptet.com/usr/www.craftmaker.nl/user/documents/upload/Product_description/craftmaker_pro_station_s30_accessories.jpg)

This nearly front-on product image is the main visual reference because the
complete worktop, 9 × 7 hole grid and all eight clamp slots are visible at
once.

## 2D expectation

![Simple MFT expected top view](expected-top-view.svg)

The 2D expectation is kept next to the model so the inferred layout can be
reviewed without opening SolidCraft.

## Known dimensions

Published replacement-top dimensions:

- 805 × 555 × 18 mm;
- Ø20 mm dog holes.

The front photo supports a 9 × 7 hole grid. The current pitch estimate is
76 mm in X and Y.

## Photo-based slot estimate

The front photo was aligned against the known worktop envelope and the visible
hole grid. The values below remain estimates rather than manufacturer
dimensions.

Eight slots are visible: two in each quadrant.

Current nominal values:

- slot width: **24 mm**;
- end-cap centre distance: **80 mm**;
- overall slot length: about **104 mm**;
- slot angle: approximately **45°**.

The inferred pattern in each quadrant is:

- the inner slot has one round-end centre at diagonal grid ring 1
  (`±76, ±76`) and extends outward;
- the outer slot has one round-end centre at diagonal grid ring 3
  (`±228, ±228`) and extends inward;
- the four diagonal grid-ring-2 positions (`±152, ±152`) do **not** contain
  dog holes; they are the clear gap between the two slots.

The model uses 80 mm centre-to-centre × 24 mm wide as the simple nominal Slot
size. That gives approximately 104 × 24 mm overall.

The 76 mm pitch, 20 mm corner cut and Slot dimensions are still estimates.

## Native SCPF construction

The worktop starts as one native `Box`. The two TOP-attached Sketches are
created and cut first. The four 20 mm plan-view corner chamfers are then
applied as the final plate feature.

The nominal dog-hole grid has 9 × 7 = 63 Circle profiles. It is authored in the
same compact way as a manual SolidCraft model:

1. one `Circle2D` seed;
2. one associative 9 × 7 `Sketch.rectangular_pattern(...)`;
3. one selective through-cut using 59 profile points.

The four diagonal ring-2 profiles at `(±152, ±152)` remain uncut, leaving
**59 dog holes**. The sketch itself remains a complete editable 9 × 7 pattern;
nothing is deleted from the pattern.

The clamp geometry is also associative inside one `Clamp slots` Sketch:

- one native `SlotCenterToCenter2D` is the master Slot;
- one diagonal `Sketch.rectangular_pattern(...)` creates the second Slot on
  the same arm;
- three `Sketch.mirror(...)` operations create the other three arms.

The corner treatment uses the common named selector
`chamfer(..., edges=Edges.VERTICAL)`.

So the final SolidCraft history stays compact:

```text
Box
Dog holes Sketch
Dog holes cut
Clamp slots Sketch
Clamp slots cut
Chamfer
```

## Scope

Not included yet:

- frame or legs;
- fence;
- dogs or clamps;
- logos and printed markings.

The reusable generic guide rail lives under
`models/components/guide_rail/`; its length is a parameter. Placement is handled by
`models/advanced/simple_mft_assembly/`.

## Run

```powershell
python -m scpf models/advanced/simple_mft/scpf/model.py --out output/simple-mft.json
python -m scpf models/advanced/simple_mft/scpf/model.py --connect --new
```
