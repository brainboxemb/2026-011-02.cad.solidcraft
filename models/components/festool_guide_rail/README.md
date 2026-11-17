# Festool guide rail component

Reusable SCPF component for a Festool FS-style guide rail.

## Parameter

`length` is the only adjustable CAD parameter. The default is **1400 mm** so
the standalone component matches the length of the supplied GrabCAD FS1400
reference. An assembly can instantiate another length without creating another
profile definition; the Simple MFT can therefore use a **1080 mm** occurrence.

## Cross-section references

Primary dimensional reference:

- [TSO Products — Guide Rail Extrusion Comparison Guide](https://tsoproducts.com/content/guide-rail-extrusion-comparison-guide.pdf)

For Festool, TSO reports A=8.30, B=16.10, D=10.50, E=8.30, F=16.10,
G=64.20 and H=184.20 mm. TSO describes these as field measurements from a
small number of commercial rails, not manufacturer tolerances.

Geometry comparison references:

- [Printables — Festool Track Profile by crashkg](https://www.printables.com/model/787210-festool-track-profile), especially `Festool Track profile v13.step`;
- [GrabCAD — Festool FS1400mm Guide Rail](https://grabcad.com/library/festool-fs1400mm-guide-rail-2).

The current SCPF profile uses the TSO dimensions for the main envelope and the
two characteristic channel regions. Small wall thicknesses, local ribs and
recesses that TSO does not dimension are still a reconstruction. They must be
checked against the STEP reference before this component is described as an
exact profile reproduction.

## Local axes

- X = cross-rail width;
- Y = rail length;
- Z = rail height;
- the component is centred along Y so assemblies own its placement.

## Validation target

The STEP comparison should check at least:

- total width and total height;
- left guide-channel opening and outer width;
- second channel opening and outer width;
- 64.20 mm location of the second channel edge;
- base thickness, lip thicknesses and the smaller top/bottom ribs not specified
  by TSO;
- a section overlay of the STEP model and the generated SCPF body.
