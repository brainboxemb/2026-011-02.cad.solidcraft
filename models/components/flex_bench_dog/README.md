# Flex bench dog

Reusable 3D-printable bench dog for a **20 mm MFT dog hole**.

The first version is based on the supplied Mini-MFT video still rather than a
manufacturer drawing or an existing downloadable CAD model. The visible design
idea is deliberately kept simple: one cylindrical dog, a small stop rim and an
insertion stem split by two crossing slots into four flexible quadrants.

## Passive clamping

There is no screw mechanism.

The default insertion stem is **20.20 mm** for a nominal **20.00 mm** hole.
Two 1.5 mm crossing slots leave four flexible segments. When the stem is pushed
into the dog hole those segments can flex inward and provide a light friction
fit.

The important tuning parameter is therefore `interference`. The initial
**0.20 mm** value is a design starting point, not a measured value from the
reference part. A first print should be used to determine the best value for
the printer, filament and actual dog-hole diameter.

## Initial dimensions

| Parameter | Default |
| --- | ---: |
| Dog-hole diameter | 20.00 mm |
| Interference | 0.20 mm |
| Working section height | 20 mm |
| Rim diameter | 24 mm |
| Rim thickness | 3 mm |
| Insertion length | 18 mm |
| Cross-slot width | 1.5 mm |
| Cross-slot length | 14 mm |

Total height is **41 mm**.

## Source and confidence

The overall construction is inferred from the supplied image. Only the nominal
20 mm dog-hole size was supplied explicitly. Rim size, lengths, slot dimensions
and the 0.20 mm interference are our first practical design values and have not
yet been verified against the physical part shown in the video.

The model should therefore be treated as a prototype for print/fit testing.
After a first test print, `interference`, `slot_width` and `slot_length`
are the first values to tune.
