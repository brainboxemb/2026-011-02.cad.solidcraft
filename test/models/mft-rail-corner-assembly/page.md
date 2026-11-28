## Qualification purpose

This model deliberately stays separate from the full Simple MFT assembly while
the bracket dimensions are still provisional.

The two short rail pieces reproduce the same corner orientation used on the MFT
support frame:

- one rail runs along +X with its C-opening toward −Y;
- one rail runs along +Y with its C-opening toward −X;
- both rail back webs meet at the inside corner;
- the bracket occupies the +X/+Y inside quadrant;
- the top bracket face is flush with the future MFT underside plane at Z=0.

The first two round rail perforations are used as the bracket fixing datum:
12.5 mm and 62.5 mm from each rail end.

The MFT underside screw position and all non-rail bracket dimensions remain
provisional until the real worktop/hardware are measured.


## Load-bearing foot and separate corner insert

The prototype bracket now continues underneath both rails. Each 75 mm rail end
rests on a 6 mm printed shoe. This gives the corner bracket a second function:
it becomes a small height-adjusting/support foot rather than only a side clamp.

The structural bracket still carries both rail ends on 6 mm printed support
feet, but the supplied native source refines the outside corner in two ways.

First, the bracket's own lower corner is an exact R18 quarter-round sector,
rather than the earlier segmented R22 approximation.

Second, the visible outside-corner filler is now a separate physical part:
`MFT Rail Corner Insert`. The insert has its own R18 outer arc, a source-shaped
inner relief and two integral PETG clip lips with sloped lead-ins. This makes
the exposed corner protection independently printable and replaceable while
the structural bracket remains unchanged in service.

## Native assembly reference

The supplied complete native model is preserved with this subassembly:

- `reference/hoek_assembly.sc`;
- `reference/hoek_assembly.json`.

Those files describe the complete rail/bracket/insert corner and are kept here
rather than duplicated under the individual component owners.
