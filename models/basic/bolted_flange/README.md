# Bolted Flange

This basic model uses the original SolidCraft flange sample only as its
dimension source. The CAD-library implementation intentionally does **not**
copy the sample's sketch-by-sketch construction history.

The dimensions are:

- flange: Ø100 × 10 mm;
- hub: Ø44 × 16 mm above the flange;
- bore: Ø24 mm through the complete 26 mm height;
- bolt circle: six Ø9 mm holes on a 70 mm PCD.

## SCPF

The SCPF model is deliberately small and uses the direct Forge primitives that
match the geometry:

- two `Cylinder` solids for the flange and hub;
- one `Hole` for the central bore;
- six `Hole` features for the bolt circle.

A `Hole` is added to the body with `+`; it is already a subtractive CAD
feature and is not represented as a subtraction cylinder.

The six bolt holes are generated in a short Python loop. This model is meant to
show clear CAD-library code, not to qualify SolidCraft's native circular
feature-pattern history.

## SCPC

The SCPC implementation follows the same simple construction directly with
`solid.cylinder` and `solid.hole` commands.

## Source

The original SolidCraft sample command document is retained unchanged in
`source/flange.json` as a reference for the dimensions and original example.
