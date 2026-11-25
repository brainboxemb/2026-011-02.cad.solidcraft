# Benchdog Clamp source

Source supplied by the project owner on 2026-11-25.

- `doghole_clamp2.sc`
  - native SolidCraft container
  - size: 745756 bytes
  - SHA-256: `ef1286929e74f63d1dced9d4c763aa4ba3202d71487047607c7df6ffb33d5cd4`
  - document format: `solidcraft/68`
  - source application cache: SolidCraft 0.49.1
- `doghole_clamp2.json`
  - exported source document JSON
  - size: 48859 bytes
  - SHA-256: `1821430f88036c04cde9bb5cd0a5e06f2b75c30e2a26637d67847ba65b49e19b`

The JSON is retained byte-for-byte in this directory. The binary `.sc`
container is tracked by hash here while this WIP branch is being established;
do not substitute a regenerated SolidCraft file for the supplied source.

## Current source-state interpretation

The final visible source state contains:

- `T-schuifstuk met vast middenoog`;
- `Scharnierarm links`;
- `Scharnierarm rechts`;
- `Scharnierpen laag Ø3`;
- `Dummyrailprofiel`;
- `Benchdog Ø20`.

The source visibility state hides the earlier dog-expansion and compact-fork
bodies. Features 67/68 and 82 are also explicitly suppressed. The first Forge
baseline follows that final visible state and keeps those older concepts only as
reference history.
