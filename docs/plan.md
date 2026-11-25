# Repository plan

This file contains unfinished work only.

## Now

### #76 — bracket STL and grouped category views

Active on `feature/76-grouped-category-views-stl`.

Follow up the accepted MFT corner subassembly and catalog taxonomy with two
presentation/output improvements:

- generate a durable STL for `mft-rail-corner-bracket`;
- render `group:` metadata as real grouped sections on the individual
  Components, Sub Assemblies and Assemblies pages.

Component ownership groups:

- Display: `corner-bracket`, `hub75-panel`;
- MFT: `simple-mft`, `flex-bench-dog`, both `guide-rail` variants,
  `mounting-rail-m8`, `mft-rail-corner-bracket`.

Acceptance:

1. bracket `ci.yml` declares `stl` and the durable build publishes
   `model.stl`;
2. the bracket model page exposes STL view/download links from the build plan;
3. category pages render group headings structurally from generic metadata;
4. one shared Hugo partial owns grouped model rendering for catalog/category
   pages;
5. ungrouped models remain supported under `Other` when a section also has
   groups;
6. Pages verification requires structural group markup, so a card label alone
   cannot satisfy the grouping contract;
7. no Hugo branch contains model-specific names.

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
- Forge v0.16.0 / SolidCraft 0.49.0 / runtime v0.3.6 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with optional primary snapshot camera;
- physical model owners may expand into multiple build variants;
- Pages links durable CAD artifacts from `build` and never republishes them;
- Pages publishes stable `/` and development `/dev/` presentation as one generated `gh-pages` tree.
