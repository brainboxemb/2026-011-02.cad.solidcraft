# MFT Rail Corner Insert

Separate printable outside-corner insert from the supplied native
`hoek_assembly` model.

The native SolidCraft document creates this as a distinct body named
`PETG-hoekinzetstuk`. The repository promotes it to a separate component
because it is a physically independent, replaceable print part.

## Native geometry

The base body is taken directly from the source:

- exact R18 outer quarter arc;
- inner diagonal relief with the source rounded notch;
- Z range: -26.8 mm to -0.2 mm;
- two clip-lip profiles start at Z=-21.35 mm and extrude 15.7 mm upward;
- each clip lip has a short 0.8 mm diagonal lead-in.

The complete `hoek_assembly.sc` and `hoek_assembly.json` are retained by
the owning subassembly under
`models/subassemblies/mft_rail_corner_assembly/reference/`.
