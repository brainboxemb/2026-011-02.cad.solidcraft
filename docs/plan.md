# Repository plan

This file contains unfinished work only.

## Now

### #133 — Wall Hook yellow display appearance

Apply the released Forge v0.19.0 display-only appearance API to the existing
Wall Hook.

Contract:

- use `Shape.with_appearance("#FFD21A")`;
- change presentation only;
- preserve geometry, mounting-hole behavior, STL and engineering semantics;
- verify generated preview/snapshot reflects the yellow appearance.

Acceptance is owned by issue #133.

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
