# Repository plan

This file is the canonical repository plan on stable `main` and contains
unfinished work only. Agents working on any lane must read this `main` copy;
branch-local copies are not independent plans.

Governance-only changes to `AGENTS.md`, `docs/plan.md` and
`docs/handoff.md` use a short-lived `docs/*` branch created from `main`
and return directly to `main` through repository-local `/merge`. Do not
create a `main -> dev` sync merely to copy plan/handoff metadata.

## Now

### #285 — adopt permanent exp lane and rolling test output

Adopt the stable `template.cad.model-project#133` contract in the real CAD
catalog without a CAD-local fork:

- add permanent source/output lane `exp`;
- add one rolling generated `test` scope requested explicitly from matching
  temporary `build.yml` with `output.scope: test`;
- keep `test` as output only, never as a source branch;
- publish Pages at `/exp/` and `/test/` beside stable `/` and `/dev/`;
- retain exact Forge work-branch qualification and record its SHA in test
  build evidence;
- keep Forge v0.26.0 / SolidCraft 0.50.0 / runtime v0.3.8 as the released
  baseline;
- qualify the adoption with a bounded real model before permanent-lane setup.

After the capability is accepted on CAD `dev`, initialize CAD `exp` through
an explicit `dev -> exp` checkpoint and qualify its build/Pages output.

## Mandatory integration rule

Every source-branch integration uses a PR conversation comment:

```text
/merge
```

Direct merge API calls, auto-merge and UI/manual merge fallback are forbidden.

## Accepted architecture

- stable `main` owns the canonical repository plan and handoff state;
- normal product/model/module work starts from `dev`;
- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- `process: false` keeps a model owner discoverable and explicitly selectable
  on a matching work branch while excluding it from automatic/full permanent-lane
  model selection and automatic dependent expansion;
- Forge v0.26.0 / SolidCraft 0.50.0 / runtime v0.3.8 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- Basic / Components / Sub Assemblies / Assemblies taxonomy;
- metadata-driven Display / MFT grouping;
- generic CAD CI/build/Pages behavior is inherited from
  `brainboxemb/template.cad.model-project` rather than reimplemented locally.

## Next

After #285 is accepted and CAD `exp` is qualified, use the rolling `/test/`
scope for the next exact Forge-exp catalog qualification so generated results
can be reviewed visually before any Forge `exp -> dev` checkpoint.
