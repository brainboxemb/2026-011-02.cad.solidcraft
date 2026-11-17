# Simple MFT assembly

This assembly combines the existing **Simple MFT worktop** with the reusable
**GuideRail** component.

The worktop and rail remain separate source models:

- worktop: `models/advanced/simple_mft/`;
- guide rail: `models/components/guide_rail/`.

## Guide rail

The assembly uses a **1080 mm** GuideRail occurrence.

Festool lists the **FS 1080/2** at 1080 mm and includes that rail with the
MFT/3 system. The current GuideRail cross-section remains the generic,
TSO-measured reference profile already documented with the component.

References:

- Festool FS 1080/2:
  https://www.festool.com/accessory/guide-rail-system/guide-systems/guide-rails/491504---fs-10802
- Festool MFT/3 documentation identifies FS 1080/2 as the supplied rail.

## Initial placement

This first assembly models only the spatial relationship needed to continue the
MFT design:

- worktop centre at X=0, Y=0;
- worktop top at Z=18 mm;
- rail long axis along world Y;
- rail length centred on Y=0;
- rail width centred on X=0;
- rail bottom rests at Z=18 mm.

The 1080 mm rail therefore overhangs the 555 mm worktop depth equally at the
front and rear.

The X position is intentionally a neutral centred starting position. A real MFT
guide rail can move along its support system; the support/swivel hardware is not
modelled yet, so this should not be read as a manufacturer-defined cutting
position.

## Scope

Included:

- Simple MFT worktop;
- one reusable GuideRail occurrence at 1080 mm;
- assembly-owned rail placement.

Not included yet:

- guide-rail support and swivel hardware;
- fence/angle stop;
- frame or legs;
- clamps, dogs or saw.

Those can be added to this assembly without changing the standalone component
models.
