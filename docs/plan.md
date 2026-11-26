# Repository plan

This file contains unfinished work only.

## Now

### #160 — reduce Wall Hook rear screw-hole chamfer to elephant-foot relief

Keep the 1.0 mm screw-entry chamfer on the front/tool side of each Ø4.2
mounting hole, but reduce the wall-contact side to a 0.3 mm edge break.

Acceptance is owned by issue #160.

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
