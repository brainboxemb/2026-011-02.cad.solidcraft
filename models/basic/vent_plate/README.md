# Vent Plate

This basic model is based directly on the SolidCraft **Vent Plate** example.

The original SolidCraft design is stored unchanged in:

`source/Vent Plate.json`

Its feature history is intentionally small and useful for library development:

1. `Box1` — 120 × 80 × 4 mm plate from corner `[0, 0, 0]`;
2. `Fillet1` — 8 mm fillet on the four vertical edges;
3. `Slot` — one 6 × 14 mm rectangular sketch at X=18..24, Y=12..26;
4. `Vent` — 4 mm positive cut extrusion;
5. `RectangularPattern1` — native two-direction feature pattern:
   - X: `cols = 6`, `pitch = 16 mm`;
   - Y: `rows = 3`, spacing `22 mm`.

## Implementations

### SCPF

`scpf/model.py` uses SCPF 0.6.1 native feature patterning. It creates one
source vent and passes that existing cut feature to
`Shape.rectangular_pattern(...)`, which lowers directly to
`solid.pattern.rectangular`. There is no Python loop and no repeated sketch
expansion.

The original SolidCraft source uses `Slot` for the sketch name and `Vent`
for its cut feature. SCPF 0.6.1 uses one name for an explicit Sketch and its
extrusion, so the SCPF source calls both `Vent`. The body geometry, source
rectangle, cut direction, pattern counts and spacing remain the same.

### SCPC

`scpc/model.py` independently describes the original native SolidCraft
commands, including the original `Slot` sketch name, `Vent` cut name and
`solid.pattern.rectangular`.

## Why this is a basic model

Basic models should, where practical, correspond directly to small SolidCraft
examples. That makes them useful both as documentation and as regression cases:
the expected native feature history already exists and does not have to be
invented specifically for Forge.
