# Repository plan

This file is the canonical repository plan on stable `main` and contains
unfinished work only. Agents working on any lane must read this `main` copy;
branch-local copies are not independent plans.

Governance-only changes to `AGENTS.md`, `docs/plan.md` and
`docs/handoff.md` use a short-lived `docs/*` branch created from `main`
and return directly to `main` through repository-local `/merge`. Do not
create a `main -> dev` sync merely to copy plan/handoff metadata.

## Now

No active work selected.

## Mandatory integration rule

Every source-branch integration uses a PR conversation comment:

```text
/merge
```

Direct merge API calls, auto-merge and UI/manual merge fallback are forbidden.

## Accepted architecture

- stable `main` owns the canonical repository plan and handoff state;
- normal product/model/module work starts from `dev`;
- work-branch selection comes from matching root `build.yml`;
- incremental `dev` CI uses the last successful integration baseline;
- `main` CI is full;
- `process: false` keeps a model owner discoverable and explicitly selectable
  while excluding it from automatic permanent-lane selection;
- released Forge baseline is v0.26.0;
- SolidCraft baseline is 0.50.0 on immutable runtime image v0.3.8;
- generated `build` branch owns `main/` and `dev/` CAD artifact scopes;
- Pages reads durable build evidence and publishes stable `/` plus `/dev/`
  without duplicating generated CAD artifacts into `gh-pages`;
- physical model owners may expose multiple build variants;
- Basic / Components / Sub Assemblies / Assemblies is the catalog structure;
- Display / MFT grouping remains metadata-driven;
- generic CI/build/Pages behavior is inherited from
  `brainboxemb/template.cad.model-project` rather than forked locally.

## Next

No next work selected. Select an open issue deliberately before implementation;
do not infer work from stale branch-local plan text.
