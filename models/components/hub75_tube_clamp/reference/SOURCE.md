# Source reference

This directory retains the exact SolidCraft authoring reference for the HUB75
tube clamp.

## Retained files

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

The JSON file is the official SolidCraft authoring export. It is not Forge
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

Only the active source features are reconstructed:

1. `Open klemring met afgeronde lippen` + `Elastische klemring`;
2. `Afgeronde rug voor de schuifgleuf` + `Lage geïntegreerde rug`;
3. `Schuifgleuf met aanloop en printflanken` +
   `Schuifgleuf met vaste eindaanslag`.

Earlier transition/dovetail experiments in the source timeline are suppressed
and are intentionally not carried into the production geometry.

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
