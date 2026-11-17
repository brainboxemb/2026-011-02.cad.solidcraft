# Guide rail component

Reusable SCPF component for guide rails with a parametric length and a fixed
cross-section variant.

The component is intentionally named generically. Assemblies depend on
`GuideRail`, not on a brand-specific class.

## Inputs

`length` is the only editable native CAD parameter.

`profile` is a non-parametric component input selecting one fixed reference
cross-section:

- `festool` — default;
- `makita`.

Examples:

```python
GuideRail(length=1080)
GuideRail(length=1500, profile="makita")
```

Changing `profile` creates a different reusable component definition; it does
not add a text/string parameter to SolidCraft.

## Festool profile

The Festool profile shape is taken from the main aluminium extrusion in the
FS 1400/2 STEP reference. That STEP profile measures approximately
**183.60 × 10.50 mm**.

The profile is calibrated to the measured Festool envelope in:

- [TSO Products — Guide Rail Extrusion Comparison Guide](https://tsoproducts.com/content/guide-rail-extrusion-comparison-guide.pdf)

TSO reports **H = 184.20 mm** and **D = 10.50 mm**. The STEP X coordinates are
therefore scaled from 183.60 to 184.20 mm; the 10.50 mm height already matches.

Additional shape/reference checks:

- [GrabCAD — Festool FS1400mm Guide Rail](https://grabcad.com/library/festool-fs1400mm-guide-rail-2)
- [Printables — Festool Track Profile by crashkg](https://www.printables.com/model/787210-festool-track-profile)

## Makita profile

The Makita profile shape is taken from the main aluminium extrusion in a
Makita **199141-8** STEP reference. The STEP envelope is approximately
**183.00 × 10.40 mm**.

The same TSO comparison gives the Makita envelope as
**H = 182.50 mm** and **D = 10.28 mm**, so the STEP cross-section is calibrated
to those dimensions.

Makita lists part **199141-8** as a **1500 mm** guide rail:

- [Makita — 199141-8 guide rail product sheet](https://www.makitauk.com/data/sr/productinfo/generated/199141-8_2.pdf)

The standalone `guide-rail-makita` result therefore uses 1500 mm.

The Makita STEP contains a few small round edges. `Polygon2D` is line-based, so
those rounds are represented by short line segments. The important rail
features and overall envelope are retained.

## What is modelled

Both variants model the **main alumiium extrusion only**.

Separate splinter guards, anti-slip strips and running strips present in the
reference assemblies are intentionally not part of this component yet. They
can be added as separate physical parts later if an assembly needs them.

The third-party STEP/reference files themselves are not committed.

TSO describes its dimensions as field measurements from commercial rails, not
manufacturer production tolerances. These models are therefore assembly/layout
references, not extrusion manufacturing drawings.

## Local axes

- X = rail width;
- Y = rail length;
- Z = rail height;
- the component is centred along Y so the owning assembly controls placement.
