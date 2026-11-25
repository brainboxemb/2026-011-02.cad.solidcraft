# Latch Hook

Source-faithful native sheet-metal reconstruction of the supplied hook.

The owner preserves the supplied native sources:

- `reference/hook.sc` — authoritative SolidCraft container;
- `reference/hook.json` — readable native feature export.

The native source has only three features:

1. `Uitslag haak` — fixed 2D blank sketch;
2. `Vlakke plaat 2 mm` — native sheet base;
3. `Haak omvouwen` — one native sheet fold.

## Drawing dimensions

| Dimension | Value |
| --- | ---: |
| sheet thickness | 2 mm |
| formed projection in side view | 20 mm |
| free hook tip X in side view | 13.5 mm |
| formed height | 10.5 mm |
| inside bend radius | R2.1 |
| overall mounting width in top view | 24 mm |
| neck width in top view | 15 mm |
| mounting holes | 2 × Ø4.3 mm |
| hole pitch | 14 mm |
| hole-centre edge datum | 5 mm |

The **15 mm** and **20 mm** dimensions describe different directions:
15 mm is the neck width in the top view; 20 mm is the total formed projection
in the side view.

## Native blank geometry

The supplied SolidCraft source fixes the blank directly:

- left edge: `(0, 7) -> (0, -7)`;
- lower R5 lobe: centre `(5, -7)`, ending at
  `(7.209449, -11.485347)`;
- tangent straight transition to `(15.3, -7.5)`;
- straight 15 mm-wide strip to `x = 28.149287`;
- mirrored upper transition and R5 lobe;
- hole centres at `(5, -7)` and `(5, 7)`, radius 2.15 mm.

This is intentionally used directly instead of adding an inferred extra blend.

## Native fold

The supplied fold contract is also used directly:

- fold X: 15.9 mm;
- angle: 138.7667505744678°;
- position: `start`;
- fixed/stays side: left;
- sheet rule: 2 mm, R2.1, K=0.44.

No bend angle, blank length or transition radius is re-derived in the SCPF
model while the native source is available.
