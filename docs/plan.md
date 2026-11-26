# Repository plan

This file contains unfinished work only.

## Now

### #150 — simplify Wall Hook to sharp polygons plus native fillets

Rework the existing Wall Hook construction without changing its confirmed
dimensions or functional features.

Contract:

- author the outer XZ hook as a sharp-cornered `Polygon2D`;
- extrude first, then round the named profile sweep edges with native
  `fillet()`;
- author the triangular reinforcement relief as a sharp polygon cutter;
- fillet the cutter's named sweep edges before subtraction;
- remove the hand-authored 2D arc-center/tangent construction;
- preserve mounting holes, lower tool access, FRONT/BACK chamfer, STL and
  #FFD21A display appearance.

Acceptance is owned by issue #150.

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
