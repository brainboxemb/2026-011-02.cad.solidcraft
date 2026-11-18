# Flex bench dog

Reusable 3D-printable bench dog for a **20 mm MFT dog hole**.

The model uses a functional CAD orientation: the worktop surface is **Z=0**,
the insert extends downward and the working dog extends upward. Print
orientation is deliberately not encoded in the model.

## Passive clamping

There is no screw mechanism.

The main insert is nominally **20.00 mm**. At the free end, the final 2 mm
flares to **20.20 mm**. Two 1.5 mm crossing slots split the lower 14 mm into
four flexible legs. Those free ends can spring inward when inserted into the
hole, providing passive tension without separate hardware.

The initial **0.20 mm** flare is a prototype value. The useful fit will depend
on the actual dog-hole diameter, printer, filament and print settings.

## Shape

- **18 mm** insertion below the worktop;
- **20 mm** overall body height above the worktop, including the 3 mm rim;
- Ø24 × 3 mm stop rim;
- small fillet at the rim-to-dog shoulder;
- light chamfer around the upper edge;
- small **raised square box logo** on the top face;
- 2 mm long flared flex tips.

## Initial dimensions

| Parameter | Default |
| --- | ---: |
| Dog-hole diameter | 20.00 mm |
| Tip flare / interference | 0.20 mm |
| Height above worktop | 20 mm |
| Rim diameter | 24 mm |
| Rim thickness | 3 mm |
| Insertion length | 18 mm |
| Flared tip length | 2 mm |
| Cross-slot width | 1.5 mm |
| Cross-slot length | 14 mm |
| Top fillet | 1.0 mm |
| Top chamfer | 0.6 mm |
| Logo relief | 0.6 mm |

The physical body spans 38 mm from the bottom of the insert to the top face,
plus the 0.6 mm raised logo.

## Source and confidence

The overall construction is inferred from the supplied Mini-MFT image. Only
the nominal 20 mm dog-hole size and the later chosen 18/20 mm proportions are
project decisions. Rim size, flex-slot dimensions and the 0.20 mm tip flare
have not yet been verified by a physical fit test.

After a first print, the first value to tune is `interference`, followed by
`slot_width` if more or less spring movement is needed.
