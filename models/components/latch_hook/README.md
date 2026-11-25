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

The drawing does not separately dimension the outer mounting-lobe radius. The
model resolves that contour from the supplied 24 mm overall width, 14 mm hole
pitch and 5 mm left-edge datum, giving a 5 mm lobe radius with straight tangent
transitions to the 15 mm neck.

## Bend derivation

With 2 mm sheet and R2.1, the outside bend radius is 4.1 mm. Matching the
20 mm formed projection places the bend centreline at X=15.9 mm. Tangency from
that outside-radius circle to the dimensioned free tip at X=13.5 mm / Z=10.5 mm
gives a bend angle of approximately 147.414 degrees.

The blank therefore extends beyond the bend centreline so SolidCraft can form
the returned hook lip from the same sheet body.
