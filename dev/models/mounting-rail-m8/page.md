## Reference basis

This is a **generic Mounting Rail M8 component**. The model name and API do not
contain a manufacturer name.

The supplied product photograph is the DRESSELHAUS mounting rail sold by
HORNBACH for M8 threaded rods and pipe clamps. Its product listing provides the
facts used directly by this model:

- length: **1000 mm**;
- material: **steel**;
- surface: **galvanized**;
- material thickness: **1.25 mm**;
- application: **M8 threaded rods / pipe clamps**.

Product/photo source:
[HORNBACH — DRESSELHAUS Montagerail t.b.v. M8 draadeinden en buisklemmen, 1 meter](https://www.hornbach.nl/p/dresselhaus-montagerail-t-b-v-m8-draadeinden-en-buisklemmen-1-meter/12515908/).

The full local source image is `mounting_rail_m8_reference.jpg`. The page
renders the whitespace-cropped `mounting_rail_m8_reference_w320.jpg`.

## Generic 27/18 geometry reference

The supplied product page does not publish the full section or punch drawing.
For a workable generic component, the first model uses a published light
27/18/1.25 installation-rail drawing as a **reference class**, not as a claim
about the DRESSELHAUS production tooling.

Reference:
[MÜPRO MPC system rail 27/18/1.25 data sheet](https://www.muepro.de/out/media/DATENBLATT_MA_MPC-SYSS_VZ_DEU_DEU.PDF).

Possible supplementary generic reference:
[MÜPRO European Technical Assessment for MPC rails](https://www.muepro.de/out/media/EUROPAISCHE_TECHNISCHE_BEWERTUNG_ETA-25-1243_MPC-SCHIENEN.PDF).

Both MÜPRO documents are used only as generic installation-rail references.
They are **not** DRESSELHAUS specifications and do not prove that the reference
product uses identical production dimensions or tooling.

Nominal profile used by the model:

- outside width: **27 mm**;
- outside height: **18 mm**;
- sheet thickness: **1.25 mm**;
- clear C-opening: **15 mm**.

The rail is built as native sheet metal from one connected XZ contour and one
native contour flange along the 1000 mm length.

## Repeating perforation pattern

The supplied photo clearly shows a repeating four-feature sequence:

1. round opening;
2. longitudinal / horizontal slot;
3. round opening;
4. transverse / vertical slot.

The generic 27/18 reference drawing supplies a consistent first dimensional
interpretation:

- round hole: **Ø12.5 mm**;
- horizontal slot: **10 × 6.4 mm**;
- vertical slot: **15 × 8.4 mm**;
- feature centre pitch: **25 mm**;
- first centre from the end: **12.5 mm**;
- full four-feature repeat: **100 mm**.

For the 1000 mm rail this gives 40 perforation positions, ending 12.5 mm before
the far end. The implementation keeps the history compact: one face-attached Circle cut is
patterned at 50 mm pitch, while one horizontal and one vertical Slot cut are
each patterned at 100 mm pitch.

These are reference-derived generic dimensions. If a DRESSELHAUS drawing or a
physical measurement differs, the model should be corrected to the measured
values rather than preserving this reference.

## Sheet rule assumptions

No bend-radius or K-factor value is published in the available product
reference. The first native sheet rule therefore uses:

- bend radius: **1.25 mm**;
- K-factor: **0.40**.

Those two values are explicit modelling assumptions, not product
specifications.
