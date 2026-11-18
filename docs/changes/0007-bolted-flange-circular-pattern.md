# 0007 — Bolted flange circular bolt pattern

**Tracks:** issue #135  
**Scope:** Bolted Flange SCPF feature history and regression contract.

## Problem

The Bolted Flange calculated six bolt-hole coordinates in Python and emitted six
independent `Hole` features. The geometry was correct, but the bolt circle was
not represented as a CAD relationship.

## Decision

The SCPF model uses one seed feature and one native circular pattern:

1. create the Ø100 flange cylinder;
2. attach one sketch to its TOP face;
3. place one Ø9 circle at `pcd / 2`;
4. cut that circle through the flange once;
5. pattern the applied cut around `Axis.Z` with `count=bolts`;
6. add the hub and central bore.

`bolts` and `pcd` are editable lowercase native parameters.

Forge currently requires a `Sketch.extrude()` feature as the source of
`Shape.circular_pattern()`; therefore the seed bolt is a sketch through-cut,
not a `Hole` primitive.

The independent SCPC model may continue to expand the six holes explicitly as a
geometry reference. Qualification compares final geometry as well as the SCPF
history contract.

## Verification

Focused command tests require one seed circle, one seed extrusion and one
`solid.pattern.circular`, with no Python coordinate loop.

The model-owned native check keeps the existing final-body bounds and volume
contract, proving that the six-hole flange geometry is unchanged.
