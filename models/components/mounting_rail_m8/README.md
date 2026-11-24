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
- 1.25 mm sheet;
- R1.25 bend radius and K=0.40 development rule;
- one authored four-profile punch unit:
  `round -> horizontal slot -> round -> vertical slot`;
- one native feature pattern repeats that complete unit;
- editable 25 mm feature pitch gives a 100 mm default repeat pitch;
- standalone default repeat count: 2; 10 reproduces the full 1000 mm reference;
- Ø12.5 round hole;
- 10 × 6.4 mm longitudinal slot;
- 15 × 8.4 mm transverse slot.

## Fabrication-order model

The rail is deliberately authored in fabrication order:

1. develop one flat sheet blank from the requested 27 × 18 mm outer section,
   15 mm opening and the shared bend rule;
2. cut the four source perforations while the sheet is flat;
3. repeat those four native cuts as one rectangular feature pattern;
4. fold both free lips;
5. fold both side walls to form the final C-profile.

SolidCraft therefore owns the four bend zones and their bend allowance instead
of Forge approximating the formed section as solid geometry.

For a 90° centreline fold the flat development uses:

`BA = π/2 × (R + K × T)`

and the bend-centre projection from the outside virtual sharp:

`projection = (R + T) - BA/2`.

With R=1.25 mm, T=1.25 mm and K=0.40, native SolidCraft 0.48.1 measurement
confirms the formed standalone rail as exactly 27.0 mm wide × 18.0 mm high.
The two free lip inner faces are at X=-7.5 and X=+7.5 mm, preserving the
15.0 mm opening.

This flat-first order also avoids SolidCraft 0.48.1's in-memory sheet-panel
attachment defect exposed by Forge #845: a valid recess attached to an
already-bent contour-flange face can be falsely classified as reaching a bend.
The product model no longer depends on that failing operation.

## Parametric pattern contract

The physical source unit is one fixed reference punch sequence:

1. round opening;
2. longitudinal slot;
3. round opening;
4. transverse slot.

The four source openings remain separate native cut features and are passed
together to one native Rectangular Pattern.

The standalone model exposes the repeat controls that should remain editable:

- `length = 250 mm`;
- `repeat_count = 2`;
- `repeat_pitch = 100 mm`.

For a full 1000 mm reference rail, use `length = 1000`,
`repeat_count = 10` and `repeat_pitch = 100 mm`. The source unit is centred
inside the requested initial length, giving a 37.5 mm end offset for the
250 mm / 2-repeat example and 12.5 mm for the 1000 mm / 10-repeat rail.

Forge 0.15 currently requires `Shape.fold()` point-based fold lines to use
fixed numeric coordinates. The component therefore resolves the fold-line
length when the component instance is built. Changing the native SolidCraft
`length` parameter after generation does not yet move those fold-line
endpoints; associative fold-line authoring is a separate Forge improvement.

## Open verification

Before treating this as manufacturer-accurate geometry, verify against either a
DRESSELHAUS dimensional drawing or a physical rail:

- section width/height and clear opening;
- inside bend radius / production bend rule;
- perforation dimensions;
- end offset and pitch.

Do not rename the generic component to the reference brand.
