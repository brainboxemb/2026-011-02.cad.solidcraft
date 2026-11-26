# Source reference

Primary source:

- `HUB75 – losse 10 proefklem.sc`
- SHA-256: `75f5a9c68eda2beed218ec1d8cf0b4fcc92b2534f3b0f19c546581613d86fa97`

The supplied parent document
`hub75-screen-2panel-couplers-clamp.sc` records that exact SHA-256 in its link
metadata for the component path `HUB75 – losse 10 proefklem.sc`. Therefore the
standalone upload is the exact linked clamp source used by the parent frame,
not merely a similar trial revision.

## Active source state

The standalone SolidCraft source has two configuration rows:

- `Vrij – printstand` (active): `clamp_bore = tube_d-clamp_interference = 9.6 mm`;
- `Gemonteerd – Ø10`: `clamp_bore = tube_d = 10 mm`.

The current catalog baseline uses Forge v0.19.0, before the public native
configuration-table API. This owner therefore makes the active **Free/print
state** authoritative and does not fake Installed as a second unrelated body.

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

- ring profile on native XY;
- ring axis along local Z;
- integrated slide back/slot authored from native XZ and running along local Y.

The frame subassembly is responsible for rotating/translating this reusable
component into Edge/Corner positions.

## Parent installed fit

The parent frame also contains a later feature named `Installed` targeting all
eight copied clamps. The native Free/Installed configuration should be adopted
when the catalog moves to a Forge release exposing configuration tables; until
then no consumer-side history branching is introduced here.
