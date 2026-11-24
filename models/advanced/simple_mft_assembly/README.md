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
- the 800 mm GuideRail is shifted 340 mm toward +X from its original assembly
  position.

The extension starts at the MFT right edge (X=+402.5 mm) and ends at
X=+597.5 mm, exactly matching the right ends of the 1000 mm support rails.

The support-rail openings remain outward and their upper edges remain at Z=0,
so both top sections can rest on the rails.
