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

The perforation is not three independent patterns.

Forge authors one attached Sketch containing all four profiles, creates one
web-through cut from that Sketch, and patterns that cut as one native history
feature. `repeat_count` remains dimensionless/editable and the native repeat
spacing is the expression `4 * feature_pitch`.

The standalone example defaults to **250 mm** with **2 complete repeat units**
and an editable **37.5 mm end offset**, which centres those units in the short
example.

`end_offset` is a separate native parameter. For the full 1000 mm reference,
use `repeat_count = 10` and `end_offset = 12.5 mm`. This keeps length,
repeat count, pitch and offset independently editable in SolidCraft without
relying on unsupported Expression × Expression arithmetic in Forge 0.15.
