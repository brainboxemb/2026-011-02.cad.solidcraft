# Bolted Flange

This basic model is based directly on the official SolidCraft **flange**
sample in `crates/engine/src/sample.rs` at SolidCraft source commit
`988dd21f6e0cec3c55c6a1221147ddcdc4fdfb7f`.

The extracted source command document is stored unchanged in:

`source/flange.json`

Its native feature history is deliberately compact:

1. `Disc` — Ø100 mm Sketch on XY, extruded 10 mm into body `Flange`;
2. `Hub` — Ø44 mm Sketch on the top face, joined 16 mm upward;
3. `Bore` — central Ø24 mm cut through the full 26 mm height;
4. `Bolt` / `BoltHole` — one Ø9 mm source hole at radius 35 mm;
5. circular feature pattern — `bolts = 6` instances around Z.

The source also declares `pcd = 70 mm`, but the original Bolt command uses
the literal centre `[35, 0]` rather than a `pcd / 2` expression.

## Implementations

### SCPF

`scpf/model.py` keeps the same one-source-feature design. The bolt hole is
created once and passed to `Shape.circular_pattern(...)`, which lowers to one
native `solid.pattern.circular` history feature.

The SCPF version deliberately connects the declared `pcd` parameter to the
bolt radius with `pcd / 2`. At the source defaults this is the same 35 mm
geometry, but changing `pcd` now does what the parameter name implies.

SCPF currently gives an explicit Sketch and its extrusion one shared name.
The SolidCraft source uses Sketch `Bolt` and extrusion `BoltHole`; the SCPF
version therefore names both `BoltHole`. The SCPC implementation below keeps
the original names exactly.

This model also exercises attached explicit Sketches on a non-rectangular
feature body. That is intentionally handled in Forge itself rather than by
rewriting the flange around a rectangular helper body.

### SCPC

`scpc/model.py` independently reproduces the original SolidCraft commands,
including the source's literal bolt centre `[35, 0]`. It keeps the original
`Disc`, `Hub`, `Bore`, `Bolt`, `BoltHole` names and the native circular
feature pattern.

## Why this is a basic model

The flange combines several ordinary CAD operations in a very small history:
stacked circular extrusions, a central bore, one bolt-hole source feature and a
native circular pattern. It is therefore a useful regression model for both
attached Sketch support and native circular feature patterns without bringing
in assembly complexity.
