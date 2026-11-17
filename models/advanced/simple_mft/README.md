# Simple MFT

This model is a photo-based study of the CRAFTMAKER ProStation S30 replacement
worktop. It models the **worktop plate only**.

## Reference photo

![CRAFTMAKER ProStation S30 front reference](https://cdn.myshoptet.com/usr/www.craftmaker.nl/user/documents/upload/Product_description/craftmaker_pro_station_s30_accessories.jpg)

Source: CRAFTMAKER ProStation S30 product page. This nearly front-on image is
used as the main geometry reference because the complete worktop, 9 × 7 hole
grid and all eight clamp slots are visible at once.

## 2D expectation

![Simple MFT expected top view](expected-top-view.svg)

The 2D expectation is the geometry reference for the SCPF model. It is kept
next to the model so slot placement can be reviewed without opening SolidCraft.

## Known dimensions

Published replacement-top dimensions:

- 805 × 555 × 18 mm;
- Ø20 mm dog holes.

The front photo also supports a 9 × 7 hole grid. The current grid estimate is
76 mm pitch in X and Y.

## Photo measurement

The front image was calibrated against the known worktop size and the visible
9 × 7 hole grid. A projective fit of the unaffected dog-hole centres gives a
mean image-fit error of about 1 pixel, so the slot geometry can be estimated in
worktop millimetres rather than raw image pixels.

Eight slots are visible: two on each diagonal arm.

Measured across the eight slots:

- slot width: about **24 mm**;
- end-cap centre distance: about **80 mm**;
- overall slot length: about **104 mm**;
- slot angle: approximately **45°**;
- inner slot: one round end is centred on diagonal grid ring 1
  (\`±76, ±76\`) and the slot extends outward;
- outer slot: one round end is centred on diagonal grid ring 3
  (\`±228, ±228\`) and the slot extends inward;
- diagonal grid ring 2 (\`±152, ±152\`) remains a normal Ø20 dog hole between
  the two slots.

The measured individual slot lengths vary by a few millimetres in the image
because of perspective, edge contrast and manual end-cap picking. The model
therefore uses the simple nominal estimate **80 mm centre-to-centre × 24 mm
wide**, equivalent to roughly **104 × 24 mm overall**.

The 76 mm pitch, 20 mm corner cut and slot dimensions are still estimates, not
manufacturer specifications.

## Pattern

For one diagonal arm:

\`\`\`text
centre

      Ø ring 1
       \
        \  inner slot, 80 mm c2c
         \
          Ø ring 2        <- normal Ø20 hole remains
           \
            \ outer slot, 80 mm c2c
             \
              Ø ring 3
\`\`\`

The same pattern is mirrored into all four quadrants. There is no Slot through
ring 2 and no Slot from the plate centre to ring 1.

## Native SCPF construction

The model targets the pinned **SCPF 0.6.1** release.

The plate starts as one eight-point polygon and is extruded to 18 mm.

The dog holes use one native source hole and one two-direction rectangular
feature pattern for the complete 9 × 7 grid.

The clamp geometry uses eight native \`SlotCenterToCenter2D\` profiles:

- four inner Slots start at ring 1 and extend 80 mm outward along the 45°
  diagonal;
- four outer Slots end at ring 3 and extend 80 mm inward along the same
  diagonal.

This keeps the SCPF model close to the visible product geometry without
inventing a 75 mm Slot length or a Slot through the middle diagonal hole.

## Scope

Not included:

- frame or legs;
- guide rail;
- fence;
- dogs or clamps;
- logos and printed markings.

## Run

\`\`\`powershell
python -m scpf models/advanced/simple_mft/scpf/model.py --out output/simple-mft.json
python -m scpf models/advanced/simple_mft/scpf/model.py --connect --new
\`\`\`
