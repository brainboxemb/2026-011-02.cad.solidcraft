# Simple MFT assembly

Separate assembly owner for continued Simple MFT system development.

## Ownership

- owner id: `simple-mft-assembly`;
- catalog section: `advanced`;
- source: `scpf/model.py`;
- depends on `simple-mft`, `guide-rail` and `mounting-rail-m8`.

The perforated worktop geometry remains owned exclusively by
`models/components/simple_mft`. The plain right-hand extension plank is an
assembly-local component.

## Current layout

The system is 1000 mm wide overall:

- perforated MFT worktop: 805 × 555 × 18 mm;
- plain right extension: 195 × 555 × 18 mm;
- total top: 1000 × 555 mm;
- two 1000 mm support rails run underneath the complete width;
- the 800 mm GuideRail is shifted 414 mm toward +X from its original assembly
  position;
- one FlexBenchDog is placed in the bottom hole of the rightmost dog-hole
  column at X=+304 mm, Y=-228 mm.

The extension starts at the MFT right edge (X=+402.5 mm) and ends at
X=+597.5 mm, exactly matching the right ends of the 1000 mm support rails.

The support-rail openings remain outward and their upper edges remain at Z=0,
so both top sections can rest on the rails.


## Support-frame corners

The two long rails start 18 mm to the right of the left work-surface edge. A
third Mounting Rail M8 runs across the left short side between the inner edges
of those long rails:

- long-rail start X = -384.5 mm;
- left cross-rail outer edge X = -402.5 mm;
- left cross-rail inner edge X = -384.5 mm;
- cross-rail length = 519 mm;
- cross-rail opening faces outward toward -X.

The cross rail stops at the inner edges of the long rails rather than
overlapping their end faces. This keeps the channel ends/openings accessible
for slide-in hardware while giving the left corners a clean meeting point.

## Materials / presentation

The native component materials are intentionally distinct for visual review:

- MFT and extension plank: MDF, `#C8A46A`;
- M8 mounting rails: galvanized steel, `#9EA6AA`;
- GuideRail: aluminium, `#C4C8CB`.


## Bench dog

The assembly reuses `models/components/flex_bench_dog` rather than drawing a
decorative pin. It is inserted in the bottom existing hole of the rightmost
MFT dog-hole column:

- X = +4 × 76 mm = +304 mm;
- Y = -3 × 76 mm = -228 mm;
- worktop surface datum Z = 18 mm.

The dog therefore keeps its own 20 mm insertion depth below the top surface and
20 mm working height above it.
