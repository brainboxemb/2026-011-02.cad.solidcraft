# Source reference

This directory retains the exact SolidCraft authoring reference for the HUB75
tube clamp.

## Retained files

### Female-slot source

- `HUB75 – losse 10 proefklem.sc`
  - canonical SolidCraft source container;
  - SHA-256:
    `75f5a9c68eda2beed218ec1d8cf0b4fcc92b2534f3b0f19c546581613d86fa97`.
- `HUB75 – losse Ø10 proefklem.json`
  - official SolidCraft JSON export of the authoring document;
  - format: `solidcraft/68`;
  - SHA-256:
    `c0ce8e3086fea322648c824f699077fdddf2b06e6a965327f6e3b5efc053d911`.

The supplied `.sc` upload was named
`HUB75 – losse 10 proefklem2.sc`, but its SHA-256 is exactly the SHA recorded
by the parent frame link metadata for `HUB75 – losse 10 proefklem.sc`.
It is therefore stored here under that canonical linked source name.

### Male-dovetail source

- `HUB75 – losse 10 proefklem2.json`
  - exact official SolidCraft JSON export supplied for the new male variant;
  - format: `solidcraft/68`;
  - SHA-256:
    `57fecc0c0df73d76b77f42a4172d646488e32fed1877b2228717f9f8c3e3ae14`.
- supplied SolidCraft container: `HUB75 – losse 10 proefklem2(1).sc`
  - exact supplied container SHA-256:
    `f6aae844a26502b84a60ddc8fd2d3e0ad78ce6dff5b0abaa60f6626d3479268f`;
  - the binary container is recorded by exact filename and digest; the retained
    JSON is the repository's directly diffable authoring reference.

The JSON files are official SolidCraft authoring exports. They are not Forge
compile/replay output and must not be confused with the generated catalog
`solidcraft.json` command document.

A SolidCraft `.sc` container also carries its own internal `document.json`
and evaluated cache files. The retained export JSON is kept separately because
it is directly readable/diffable while preserving the authored parameters,
feature history and configuration rows; the `.sc` remains the authoritative
source container.

The parent document also carries an imported STEP representation for the linked
component. That STEP payload is evidence of the linked result only; it is not
the source used to reconstruct the Forge model.

## Source parameters and physical state

The source defines:

- `tube_d = 10 mm`;
- `clamp_interference = 0.4 mm`;
- `clamp_bore = tube_d-clamp_interference` in the Free state.

The standalone SolidCraft source has two configuration rows:

- `Vrij – printstand` / public label `Free` (active in the source):
  `clamp_bore = tube_d-clamp_interference = 9.6 mm`;
- `Gemonteerd – Ø10` / public label `Installed`:
  `clamp_bore = tube_d = 10 mm`.

The catalog component is parameterized independently of the Ø10 default:
`tube_d`, `clamp_interference` and `clamp_bore` remain native model
parameters. The reusable component publishes all three values; the standalone
catalog root stores the Free base expression
`clamp_bore = tube_d-clamp_interference`, while an Assembly may provide one
shared `clamp_bore` dependency to every clamp occurrence.

Forge v0.23.0 authors the state as one independent native Configuration Rule:
`Installed` drives `clamp_bore = tube_d`. The standalone catalog document
keeps that rule disabled, so manufacturing output and STL remain Free by
default. No Python geometry branch implements the state.

## Active production features

The owner contains two physical interface variants sharing the same elastic
ring and fit parameters.

### Female slot

The existing production variant reconstructs:

1. `Open klemring met afgeronde lippen` + `Elastische klemring`;
2. `Afgeronde rug voor de schuifgleuf` + `Lage geïntegreerde rug`;
3. `Schuifgleuf met aanloop en printflanken` +
   `Schuifgleuf met vaste eindaanslag`;
4. the parent 0.14 mm slot-entry chamfer.

### Male dovetail

The newly supplied source suppresses the female back/slot extrudes and the
earlier male experiments. Its final active interface is:

1. feature 22, `Symmetrische groeven met vlakke bodem`, one 14-segment XZ
   profile at `-dove_run/2`;
2. feature 23, `Symmetrische zwaluwstaart met vlakke groefbodems`, joined for
   `dove_run = 16 mm`;
3. feature 24, `Spiegelbeeldige correctie van de rugflanken`, two symmetric
   correction loops at `-dove_run/2-0.1 mm`;
4. feature 25, `Rugflanken onder 45 graden`, cut for
   `dove_run+0.2 mm`.

The source keeps `dove_head = 12 mm`, `dove_depth = 2.05 mm`,
`dove_angle = 45 deg`, `dove_land_root = 0.65 mm`,
`dove_land_head = 0.8 mm`, `dove_round = 0.2 mm` and
`dove_groove_flat = 0.4 mm`. The resulting default neck is 10.8 mm.

No hybrid body is authored: each public variant includes only its own active
mechanical interface history.

## Local frame

The clamp keeps the standalone source frame:

- ring profile on SolidCraft XY;
- ring axis along local Z;
- integrated slide back/slot authored from SolidCraft XZ and running along local Y.

The frame subassembly owns rotation/translation of reusable clamp occurrences
into the Edge/Corner positions.

## Parent installed fit

The parent tube-frame document owns one shared `tube_d`,
`clamp_interference` and `clamp_bore` dependency for all eight reusable
clamp occurrences. Its independent `Installed` rule is enabled by default;
disabling the rule restores the active row's Free expression
`tube_d-clamp_interference`.

The frame remains physically Medium-only until #189 supplies real
Small/Medium/Large coupler geometry. The Installed rule is orthogonal to that
future row-axis expansion.

## Parent-level production amendment

The linked standalone file is exact, but the parent frame adds one active
feature immediately after import:

- feature 199, `Inloop in groef van Ø10 proefklem`;
- equal-distance chamfer: **0.14 mm**;
- three open-end slot edges at native edge-pick points:
  `(-7.975,-8,3.275)`, `(-7.1,-8,0)`, `(-7.975,-8,-3.275)`.

That amendment exists before the eight Edge/Corner copies are created, so the
catalog owner includes it as part of the production clamp geometry rather than
leaving it assembly-local.
