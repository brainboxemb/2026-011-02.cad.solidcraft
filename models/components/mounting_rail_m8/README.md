# Mounting Rail M8

Reusable generic component for a light perforated M8 installation C-profile.

## Classification

- model family: `components`;
- source path: `models/components/mounting_rail_m8`;
- public model id: `mounting-rail-m8`;
- manufacturer names are reference provenance only.

## Geometry contract

Product facts from the supplied DRESSELHAUS/HORNBACH reference:

- 1000 mm long;
- galvanized steel;
- 1.25 mm sheet;
- intended for M8 installation hardware.

Generic 27/18 reference geometry:

- 27 × 18 mm outer section;
- 15 mm C-opening;
- native sheet-metal contour flange;
- one authored four-profile punch unit:
  `round -> horizontal slot -> round -> vertical slot`;
- one native feature pattern repeats that complete unit;
- editable 25 mm feature pitch gives a 100 mm default repeat pitch;
- standalone default repeat count: 2; 10 reproduces the full 1000 mm reference;
- Ø12.5 round hole;
- 10 × 6.4 mm horizontal slot;
- 15 × 8.4 mm vertical slot.

## Open verification

Before treating this as manufacturer-accurate geometry, verify against either a
DRESSELHAUS dimensional drawing or a physical rail:

- section width/height and clear opening;
- inside bend radius;
- perforation dimensions;
- end offset and pitch;
- material bend rule.

Do not rename the generic component to the reference brand.

## Parametric pattern contract

The physical source unit is one fixed reference punch sequence:

1. round opening;
2. longitudinal slot;
3. round opening;
4. transverse slot.

Each source opening remains its own native cut feature because SolidCraft
0.48.1 rejects a disconnected compound sheet recess and can also misclassify
symbolic sheet-cut geometry as reaching a bend.

Forge 0.15 allows `rectangular_pattern()` to receive a sequence of several
already-applied native features. The four source cuts are therefore passed
together to **one native Rectangular Pattern**.

The standalone model exposes exactly the repeat controls that should remain
editable:

- `length = 250 mm`;
- `repeat_count = 2`;
- `repeat_pitch = 100 mm`.

The source-unit dimensions remain the fixed generic 27/18 reference values.
For a full 1000 mm reference rail, use `length = 1000`,
`repeat_count = 10` and keep `repeat_pitch = 100 mm`; a product-end-aligned
version would use the corresponding 12.5 mm source offset rather than the
37.5 mm centred short-example offset.
