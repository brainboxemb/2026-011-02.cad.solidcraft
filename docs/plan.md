# Repository plan

This file contains unfinished work only.

## Now

### #166 — add two-panel HUB75 screen subassembly

Add a separate 320 × 320 mm nominal two-panel HUB75 screen next to the existing
five-panel `hub75-screen`.

Contract:

- reuse the detailed `Hub75Panel` component;
- use 160 mm X pitch;
- place panel centres at X=-80 and X=+80 mm, Z=160 mm;
- left panel uses the normal upright placement;
- right panel uses the existing alternating reversed orientation;
- keep the existing five-panel subassembly unchanged.

Acceptance is owned by issue #166.

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
- Forge v0.19.0 / SolidCraft 0.49.0 / runtime v0.3.6 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- Basic / Components / Sub Assemblies / Assemblies taxonomy;
- metadata-driven Display / MFT grouping.
