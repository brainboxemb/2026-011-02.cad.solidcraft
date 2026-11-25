# Latch Hook

Native sheet-metal reconstruction of the supplied latch-hook drawing.

The manufacturing intent is deliberately simple:

1. cut one flat 2 mm sheet blank;
2. drill/punch two Ø4.3 mounting holes;
3. form one hook bend.

## Dimensioned source constraints

| Dimension | Value |
| --- | ---: |
| sheet thickness | 2 mm |
| formed projection | 20 mm |
| free hook tip X | 13.5 mm |
| formed height | 10.5 mm |
| inside bend radius | R2.1 |
| mounting width | 24 mm |
| hook-neck width | 15 mm |
| mounting holes | 2 × Ø4.3 mm |
| hole pitch | 14 mm |
| hole-centre edge datum | 5 mm |

The drawing does not separately dimension the outer transition between the
mounting lobes and the 15 mm neck. The model keeps the R5 mounting lobes implied
by the 24 mm overall width / 14 mm hole pitch / 5 mm edge datum, then uses a
second circular blend tangent to both each R5 lobe and the straight 15 mm neck.
This removes the sharp polygonal transition from the first prototype while
preserving every dimensioned datum.

## Bend derivation

With 2 mm sheet and R2.1, the outside bend radius is 4.1 mm. Matching the
20 mm formed projection places the bend centreline at X=15.9 mm. Tangency from
that outside-radius circle to the dimensioned free tip at X=13.5 mm / Z=10.5 mm
gives:

- outside tangent point ≈ (18.108, 7.555) mm;
- straight returned lip ≈ 5.469 mm;
- bend angle ≈ 147.414°;
- bend allowance ≈ 7.461 mm at K=0.40;
- flat blank end X ≈ 25.100 mm for a centerline fold.

The 20 / 13.5 / 10.5 side projection is therefore solved from the formed
geometry rather than chosen by eye.
