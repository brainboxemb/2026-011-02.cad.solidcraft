# Repository plan

This file contains unfinished work only.

## Now

### #67 — split CAD catalog into subassemblies / assemblies with groups

Active on `feature/catalog-subassemblies-assemblies`.

Replace the ambiguous `advanced` model level with the repository/site taxonomy:

- `basic`;
- `components`;
- `subassemblies`;
- `assemblies`.

Add optional `group` metadata, initially `display` and `mft`, and keep the
Hugo catalog generic through `site/data/cad/catalog.yml`.

Current migration:

- `hub75_screen` -> `subassemblies / display`;
- `simple_mft_assembly` -> `assemblies / mft`;
- `hub75_wood_frame` -> `assemblies / display`;
- `hub75-display2` -> `assemblies / display`.

Acceptance:

1. no `models/advanced` source remains;
2. CI discovery priorities are 10/20/30/40 for basic/components/subassemblies/assemblies;
3. Pages navigation exposes the four sections;
4. grouped catalog sections render Display/MFT from metadata, not hardcoded model logic;
5. moved CAD models still build natively;
6. Pages PR verification passes for the dev scope;
7. corner-bracket WIP PR #63 remains separate and is updated onto this baseline only after promotion.

## Mandatory integration rule

Agents do not choose merge methods themselves.

Every source-branch integration uses a PR conversation comment:

```text
/merge
```

Direct merge API calls, auto-merge and UI/manual merge fallback are forbidden.
If merge-policy fails, repair it rather than bypassing it.

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- directory-local model build priority;
- explicit physical-model dependency graph for assembly impact;
- local merge-policy owns all source-branch integration and dispatches target CI;
- standalone cleanup removes merged temporary branches;
- direct Forge -> JSON -> one SolidCraft replay batch;
- Forge v0.15.0 / SolidCraft 0.48.1 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with optional primary snapshot camera;
- physical model owners may expand into multiple build variants;
- Pages links durable CAD artifacts from `build` and never republishes them;
- Pages publishes stable `/` and development `/dev/` presentation as one generated `gh-pages` tree.
