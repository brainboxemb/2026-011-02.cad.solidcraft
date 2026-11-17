# Guide rail component

Reusable SCPF component for a simplified guide rail.

The component is intentionally named generically. The **current profile** is
based on measured Festool FS-style rail dimensions, but assemblies should depend
on a guide rail rather than on a brand-specific component name.

## Parameter

`length` is the only adjustable CAD parameter. The standalone default is
**1400 mm**. An assembly can instantiate another length without duplicating the
profile; the Simple MFT can therefore use a **1080 mm** occurrence.

## Current cross-section source

The dimensional basis for the current profile is:

- [TSO Products — Guide Rail Extrusion Comparison Guide](https://tsoproducts.com/content/guide-rail-extrusion-comparison-guide.pdf)

For the Festool rail measured by TSO:

| TSO dimension | mm |
| --- | ---: |
| A | 8.30 |
| B | 16.10 |
| D | 10.50 |
| E | 8.30 |
| F | 16.10 |
| G | 64.20 |
| H | 184.20 |

The SCPF component uses those dimensions directly for the two characteristic
guide/mounting features and the overall envelope. TSO describes the values as
field measurements from a small number of commercial rails, not manufacturer
tolerances.

The small wall thicknesses, base thickness and minor extrusion ribs are not
dimensioned in the TSO drawing. They are intentionally simplified here because
this component is meant for assembly/layout work, not manufacturing the
extrusion.

Additional visual references for the current profile:

- [Printables — Festool Track Profile by crashkg](https://www.printables.com/model/787210-festool-track-profile)
- [GrabCAD — Festool FS1400mm Guide Rail](https://grabcad.com/library/festool-fs1400mm-guide-rail-2)

These are useful sanity checks for the overall appearance, but they do not
override the TSO dimensions.

## Local axes

- X = cross-rail width;
- Y = rail length;
- Z = rail height;
- the component is centred along Y so assemblies own its placement.
