## Reference basis

The Simple MFT worktop is a photo-based study of the CRAFTMAKER ProStation S30
replacement worktop. The model covers the worktop plate, not the complete
workbench.

The product photograph shown below identifies the replacement worktop. The original front reference was used to estimate the hole and slot pattern. The local
2D expectation is kept beside it so the inferred layout can be reviewed without
opening SolidCraft.

Product photograph source: [CRAFTMAKER replacement worktop](https://cdn.myshoptet.com/usr/www.craftmaker.nl/user/shop/big/181_craftmaker-pro-station-s30-vervangend-mdf-werkblad-met-gaten-voor-20-mm-bankhaken.jpg?ff=1&x=1024&y=1024&q=85&ts=69836430&sg=38cb01fe). The local source is `craftmaker_s30_worktop.jpg`; the page uses its `_w320` derivative.

## Known dimensions

Published replacement-top dimensions used by the model are:

- 805 × 555 × 18 mm;
- Ø20 mm dog holes.

The front reference supports a 9 × 7 hole grid. The current nominal pitch is
76 mm in X and Y.

## Photo-based slot estimate

The front reference was aligned against the known worktop envelope and visible
hole grid. These values are estimates, not manufacturer specifications.

Eight slots are visible: two in each quadrant.

Current nominal values:

- slot width: **24 mm**;
- end-cap centre distance: **80 mm**;
- overall slot length: about **104 mm**;
- slot angle: approximately **45°**.

For each quadrant, the inner slot starts at diagonal grid ring 1
(`±76, ±76`) and extends outward. The outer slot starts at diagonal grid ring
3 (`±228, ±228`) and extends inward. The four diagonal ring-2 positions
(`±152, ±152`) are intentionally left without dog holes.

The model therefore keeps a complete editable 9 × 7 sketch pattern but cuts
only 59 of the 63 circle profiles.

The 76 mm pitch, 20 mm corner cuts and slot dimensions remain photo-derived
estimates.

## Reuse

The standalone worktop is also a reusable SCPF component. The assembly variant
uses the same worktop definition and adds the generic GuideRail component with
the Festool profile at 800 mm. The rail is centred over X=0 and rests on the
worktop top face.
