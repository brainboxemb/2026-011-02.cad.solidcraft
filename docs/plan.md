# Repository plan

This file contains unfinished work only.

## Now

### #259 — adopt digest-pinned runtime candidate qualification

Synchronize the accepted `template.cad.model-project#122` work-branch runtime
candidate contract. Permanent SolidCraft pins remain release-only; temporary
candidate replay is allowed only through an OCI digest in matching
`build.yml`.


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
- Forge v0.25.0 / SolidCraft 0.49.0 / runtime v0.3.6 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- Basic / Components / Sub Assemblies / Assemblies taxonomy;
- metadata-driven Display / MFT grouping.
