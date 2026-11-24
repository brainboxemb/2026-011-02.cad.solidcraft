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

The perforation is not three independent patterns and it is not one compound
multi-profile sheet extrusion.

The source unit consists of four native cut features:

1. round opening;
2. longitudinal slot;
3. round opening;
4. transverse slot.

Forge 0.15 allows `rectangular_pattern()` to receive a non-empty sequence of
already-applied feature Shapes. The model therefore passes all four source cuts
together to **one native rectangular feature pattern**. SolidCraft stores one
pattern history feature with the four source feature names in its `features`
list.

`repeat_count` remains dimensionless/editable and the native repeat spacing is
the expression `4 * feature_pitch`.

The standalone example defaults to **250 mm**, **2 complete repeat units** and
an editable **37.5 mm end offset**, centring the two units in the short example.

For the full 1000 mm product reference, use `repeat_count = 10` and
`end_offset = 12.5 mm`.
