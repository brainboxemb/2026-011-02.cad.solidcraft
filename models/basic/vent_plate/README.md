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

### SCPC

`scpc/model.py` describes the same five-step intent with native SolidCraft
commands, including `solid.pattern.rectangular`.

### SCPF

The SCPF implementation is deliberately **not** approximated with Python loops
or repeated sketches. Forge issue
`brainboxemb/lib.py.solidcraft.forge#215` tracks the missing native
rectangular feature-pattern API.

Once that API is available, the SCPF model should reproduce the same feature
history rather than only equivalent final geometry.

## Why this is a basic model

Basic models should, where practical, correspond directly to small SolidCraft
examples. That makes them useful both as documentation and as regression cases:
the expected native feature history already exists and does not have to be
invented specifically for Forge.
