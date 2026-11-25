# Repository plan

This file contains unfinished work only.

## Now

### #62 — MFT rail corner bracket and qualification subassembly

Active on `feature/62-mft-rail-corner-subassembly`.

Continue the accepted corner-bracket WIP from PR #63 on the current catalog
taxonomy and released CAD toolchain.

Ownership:

- reusable printable bracket: `models/components/mft_rail_corner_bracket`;
- two-rail qualification model:
  `models/subassemblies/mft_rail_corner_assembly`;
- presentation: `section: subassemblies`, `group: mft`.

Keep the already reviewed prototype intent:

- two perpendicular 75 mm rail-fixing arms;
- rail-hole datums at 12.5 and 62.5 mm;
- 6 mm load-bearing plastic shoes below both rail ends;
- integral rounded outside-corner bumper;
- upper/lower triangular gussets;
- provisional countersunk fixing into the MFT underside;
- both rail C-openings and rail ends remain accessible.

Acceptance:

1. bracket remains a reusable component and depends only on `mounting-rail-m8`;
2. qualification model is a real MFT subassembly, not an `advanced` model;
3. Pages places it under Sub Assemblies / MFT from generic metadata;
4. Forge `v0.16.0` compiles both new owners;
5. native SolidCraft 0.49.0 replay succeeds on runtime v0.3.6;
6. generated top/outside/underside views retain the reviewed fit and bumper;
7. obsolete PR #63 is closed as superseded after this branch is accepted.

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
