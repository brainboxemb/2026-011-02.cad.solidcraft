# MFT Rail Corner Bracket

Reusable prototype bracket for joining two `MountingRailM8` profiles at 90°.

## Design intent

The bracket is based on the functional layout visible in the supplied reference
images: two perpendicular vertical fixing faces, a stiff upper/lower corner
plate and a separate fixing into the worktop underside. It is not dimensioned
from the reference product.

Inspiration source:

- Etsy — STL Files for DIY MFT Brackets:
  https://www.etsy.com/listing/789200136/stl-files-for-diy-mft-brackets

## Rail-owned dimensions

The current Mounting Rail M8 controls the geometry that is not provisional:

- profile height: 27 mm;
- profile depth: 18 mm;
- first round opening: 12.5 mm from the rail end;
- second round opening: 62.5 mm from the rail end.

The bracket therefore uses 75 mm arms with two M8 clearance holes per arm at
12.5 and 62.5 mm.

## Provisional dimensions

Until the physical MFT underside and intended hardware are measured:

- bracket wall: 5 mm;
- load-bearing under-rail foot: 6 mm;
- rounded outside bumper radius: 22 mm;
- top/bottom triangular gusset leg: 55 mm;
- rail clearance: Ø8.5 mm;
- MFT underside screw: Ø5.5 mm;
- countersink: Ø10.5 mm / 90°;
- prototype material: PETG.

The top plate is flush with Z=0, which is the intended MFT underside plane.

The bracket also acts as a load-bearing foot. Two 6 mm-thick plastic shoes run
under the first 75 mm of both rail profiles, so the metal rails genuinely rest
on the printed bracket. This adds 6 mm of foot height below the rail system.

At the outside corner those two shoes merge into a low quarter-round bumper:
- 22 mm radius;
- about 4 mm plastic overhang beyond the 18 mm rail depth;
- only below the rail-bottom plane, so neither C-channel opening is blocked.

This first version makes the bumper integral with the bracket because that is
the strongest and simplest printable geometry. If impact wear becomes relevant,
the rounded nose can later be split into a replaceable insert without changing
the rail/bracket datums.

Both rail C-openings remain on the outside of the corner so slide-in hardware
is not blocked.
