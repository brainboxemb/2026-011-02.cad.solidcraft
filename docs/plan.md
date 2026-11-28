# Repository plan

This file contains unfinished work only.

## Now

### #250 — adopt Forge v0.26 / SolidCraft 0.50 configuration baseline

Adopt released Forge v0.26.0 and immutable runtime v0.3.8 / SolidCraft 0.50.0.
Keep HUB75 tube-clamp Free/Installed on direct Parameter configuration and
migrate the real frame-coupler panel-pin history cut to scoped
`feature(..., suppressed=True)` authoring.

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
- `process: false` keeps a model owner discoverable and explicitly selectable
  on a matching work branch while excluding it from automatic/full permanent-lane
  model selection and automatic dependent expansion;
- Forge v0.26.0 / SolidCraft 0.50.0 / runtime v0.3.8 baseline after #250;
- generated `build` branch with `dev/` and `main/` scopes;
- Basic / Components / Sub Assemblies / Assemblies taxonomy;
- metadata-driven Display / MFT grouping.
