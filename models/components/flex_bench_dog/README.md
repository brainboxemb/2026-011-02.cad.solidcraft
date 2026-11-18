# Flex bench dog

Reusable 3D-printable bench dog for a **20 mm MFT dog hole**.

The model uses a functional CAD orientation: the worktop surface is **Z=0**,
with **20 mm above and 20 mm below** the worktop. Print orientation remains a
separate manufacturing choice.

## Passive clamping

There is no screw mechanism.

The complete 20 mm insert is a very shallow tapered cylinder (frustum):

- **Ø20.00 mm at the rim/worktop end**;
- **Ø20.20 mm at the free lower end**.

Two 1.5 mm crossing slots split the lower 16 mm into four flexible legs. Each
leg therefore inherits the slight outward taper and can spring inward when the
dog is inserted into a nominal 20 mm hole.

The initial **0.20 mm diameter increase over 20 mm** is a prototype value. The
useful fit will depend on the actual dog-hole diameter, printer, filament and
print settings.

## Shape

- 20 mm above the worktop;
- 20 mm tapered insert below the worktop;
- **Ø22 × 1.5 mm** stop rim, only 1 mm radial overhang around the Ø20 body;
- 0.6 mm chamfer around the upper edge;
- larger 1.0 mm chamfer on the lower insertion edge as a lead-in;
- two 16 mm cross slots, leaving a 4 mm solid flex root;
- shallow recessed **cube/box wireframe** in the top face.

## Initial dimensions

| Parameter | Default |
| --- | ---: |
| Dog-hole diameter | 20.00 mm |
| Insert diameter at rim | 20.00 mm |
| Insert diameter at free end | 20.20 mm |
| Height above worktop | 20 mm |
| Insertion length | 20 mm |
| Rim diameter | 22 mm |
| Rim thickness | 1.5 mm |
| Cross-slot width | 1.5 mm |
| Cross-slot length | 16 mm |
| Top chamfer | 0.6 mm |
| Bottom lead-in chamfer | 1.0 mm |
| Logo line width | 0.6 mm |
| Logo depth | 0.6 mm |

The body spans **40 mm** from the free end of the insert to the top face. The
insert may therefore extend below an 18 mm worktop; it does not need to finish
flush with the underside.

## Top mark

The top mark is not a filled square. It is a recessed isometric cube/box
wireframe based on the supplied reference: six outer edges plus three internal
edges meeting at the centre. Each line is modelled as a narrow rounded slot so
the mark remains printable at this scale.

## Source and confidence

The overall construction is inferred from the supplied Mini-MFT image. The
nominal 20 mm dog-hole size, 20/20 mm proportions, small rim and cube mark are
project design decisions. The 0.20 mm taper and flex-slot dimensions have not
yet been verified by a physical fit test.

After a first print, the first value to tune is `interference`, followed by
`slot_width` if more or less spring movement is needed.
