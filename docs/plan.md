# Repository plan

This file contains unfinished work only.

## Now

### #30 — native latch reconstruction

Active on `fix/30-restore-latch-source`.

Finish the generic latch component from the preserved native SolidCraft source.

Source contract:

- owner: `models/components/latch`;
- catalog classification only: `Components / Display`;
- authoritative binary: `reference/latch.sc` (498,569 bytes);
- readable export: `reference/latch.json`;
- source native history: sheet bases/folds/flange/contour, revolved rivets and
  one cylindrical hinge pin;
- no screenshot-derived or fused-solid substitute geometry.

Current implementation maps the source into separate physical components:

- 2.0 mm mounting foot, R0.6 / K0.40;
- 1.6 mm operating handle, R0.9 / K0.40;
- 2.0 mm pull bail, R1.0 / K0.40;
- 0.7 mm locking spring/lip, R0.8 / K0.42;
- two bail rivets, one locking-lip rivet and one continuous hinge pin.

Forge v0.16.0 provides all primitives required by this reconstruction,
including connected line/arc profiles, sheet metal and Sketch.revolve().

Acceptance:

1. source files are committed and retained unchanged;
2. the generic owner remains named `latch`, with only catalog group
   `display`;
3. Forge v0.16.0 compiles the full source-derived model;
4. SolidCraft 0.49.0 replays it on runtime v0.3.6;
5. model/top/side review views are visually consistent with the native source;
6. browser structure keeps physical metal parts separate;
7. no product-specific Forge change is introduced;
8. after qualification, remove the incorrect historical `display_hinge`
   branch/work item as superseded.

## Mandatory integration rule

Every source-branch integration uses a PR conversation comment:

```text
/merge
```

Direct merge API calls, auto-merge and UI/manual merge fallback are forbidden.

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- Forge v0.16.0 / SolidCraft 0.49.0 / runtime v0.3.6 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- Basic / Components / Sub Assemblies / Assemblies taxonomy;
- metadata-driven Display / MFT grouping.
