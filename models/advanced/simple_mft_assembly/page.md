## Assembly intent

This is a separate assembly owner, not a build variant of the Simple MFT
component.

It reuses:

- `models/components/simple_mft` for the complete worktop;
- `models/components/guide_rail` for the rail profile and length.

The current assembly places an 800 mm Festool-profile GuideRail along the
worktop Y/depth direction. The rail is centred over X=0 and its bottom follows
the same `worktop_thickness` parameter used by the Simple MFT component.

This owner is classified under **Advanced Models** for now. It can evolve
independently as the MFT assembly gains more components and assembly logic.
