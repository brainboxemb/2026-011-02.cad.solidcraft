# Flex bench dog

Reusable 3D-printable bench dog for a **20 mm MFT dog hole**.

The model uses a functional CAD orientation: the worktop surface is **Z=0**,
with **20 mm above and 20 mm below** the worktop. Print orientation is
deliberately not encoded in the model.

## Passive clamping

There is no screw mechanism.

The main insert is nominally **20.00 mm**. At the free end, the final 2 mm
flares to **20.20 mm**. Two 1.5 mm crossing slots split the lower 16 mm into
four flexible legs. Those free ends can spring inward when inserted into the
hole, providing passive tension without separate hardware.

The initial **0.20 mm** flare is a prototype value. The useful fit will depend
on the actual dog-hole diameter, printer, filament and print settings.

## Shape

- **20 mm** insertion below the worktop;
- **20 mm** overall body height above the worktop, including the 3 mm rim;
- Ø24 × 3 mm stop rim;
- light **0.6 mm chamfer** around the upper edge;
- larger **1.0 mm chamfer** on the lower insertion edge as a lead-in;
- small **recessed square box logo** in the top face;
- 2 mm long flared flex tips;
- 16 mm flex slots, leaving 4 mm solid material below the rim.

## Initial dimensions

| Parameter | Default |
| --- | ---: |
| Dog-hole diameter | 20.00 mm |
| Tip flare / interference | 0.20 mm |
| Height above worktop | 20 mm |
| Insertion length | 20 mm |
| Rim diameter | 24 mm |
| Rim thickness | 3 mm |
| Flared tip length | 2 mm |
| Cross-slot width | 1.5 mm |
| Cross-slot length | 16 mm |
| Top chamfer | 0.6 mm |
| Bottom lead-in chamfer | 1.0 mm |
| Logo depth | 0.6 mm |

The physical body spans **40 mm** from the bottom of the insert to the top
face. That is intentionally slightly longer than an 18 mm worktop; the insert
does not need to stop flush with the underside. The square logo is recessed
0.6 mm into the top face.

## Source and confidence

The overall construction is inferred from the supplied Mini-MFT image. The
nominal 20 mm dog-hole size and the current symmetric 20/20 mm proportions are
project decisions. Rim size, flex-slot dimensions and the 0.20 mm tip flare
have not yet been verified by a physical fit test.

After a first print, the first value to tune is `interference`, followed by
`slot_width` if more or less spring movement is needed.
