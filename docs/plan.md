# Repository plan

This file is the canonical repository plan on stable `main` and contains
unfinished work only. Agents working on any lane must read this `main` copy;
branch-local copies are not independent plans.

Governance-only changes to `AGENTS.md`, `docs/plan.md` and
`docs/handoff.md` use a short-lived `docs/*` branch created from `main`
and return directly to `main` through repository-local `/merge`. Do not
create a `main -> dev` sync merely to copy plan/handoff metadata.

## Now

### #307 — test a more efficient HUB75 Middle coupler authoring path

Run one bounded A/B experiment on the Middle coupler: replace its four
separate guide Sketch/extrude/join operations with one multi-profile
Sketch/extrude while preserving identical source loops and geometry. Measure
generated/history cost and artifact sizes. Keep further seam-guide/tessellation
experiments separate if this first change does not materially improve STL size.

## Mandatory integration rule

Every source-branch integration uses a PR conversation comment:

```text
/merge
```

Direct merge API calls, auto-merge and UI/manual merge fallback are forbidden.

## Accepted architecture

- stable `main` owns the canonical repository plan and handoff state;
- permanent source lanes are `main`, `dev` and `exp`; `test` is output
  only and never a source branch;
- normal short-lived product/model/module work may target `dev` or `exp`;
- temporary -> `dev`/`exp` uses squash; `dev <-> exp` uses explicit merge
  commits; `exp -> main` is forbidden; stable promotion is `dev -> main`;
- work branch selection comes from matching `build.yml`;
- incremental `dev` and `exp` CI use each lane's last successful
  push/workflow_dispatch baseline; `main` CI is full;
- `process: false` keeps a model owner discoverable and explicitly selectable
  on a matching work branch while excluding it from automatic/full permanent-lane
  model selection and automatic dependent expansion;
- Forge v0.27.0 / SolidCraft 0.50.0 / runtime v0.3.8 is the released baseline;
- generated `build` branch contains `main/`, `dev/`, `exp/` and one
  rolling `test/` scope;
- matching temporary `build.yml` opts into review publication with
  `output.scope: test`; PR execution remains bounded while publication
  materializes a complete rolling review catalog from durable `build/dev`
  plus selected candidate model replacements;
- rolling test evidence retains exact source branch/SHA plus optional exact
  Forge qualification SHA; no per-PR output directories or cleanup lifecycle;
- Pages publishes stable `/`, development `/dev/`, experimental `/exp/`
  and current rolling review `/test/` in one generated `gh-pages` tree;
- Basic / Components / Sub Assemblies / Assemblies taxonomy;
- metadata-driven Display / MFT grouping;
- generic CAD CI/build/Pages behavior is inherited from
  `brainboxemb/template.cad.model-project` rather than reimplemented locally.
