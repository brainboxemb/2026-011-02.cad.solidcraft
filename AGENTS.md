# Agent guidance

## Purpose

This repository owns the migrated SolidCraft CAD model catalog.

Generic CAD CI, build and Pages behavior is inherited from
`brainboxemb/template.cad.model-project`. Do not re-invent generic template
behavior in model code or repository-local exceptions.

Models and Python capabilities use the same ownership pattern: each item has
its own directory, configuration and tests/verification.

## Canonical repository governance

`docs/plan.md` is canonical on stable `main` and is the single source of
truth for unfinished work. Agents working on any lane must read the current
`main` copy; branch-local copies are not independent plans.

`docs/handoff.md` is also maintained directly on `main` as handoff metadata.

Governance-only changes may use a short-lived `docs/*` branch created from
`main` and returned directly to `main` through the repository-local
`/merge` policy. Such a PR may change only:

- `AGENTS.md`;
- `docs/plan.md`;
- `docs/handoff.md`.

Do not create a `main -> dev` sync merely to copy plan or handoff metadata.

## Start work

Before changing anything:

1. inspect current issues, pull requests and branches;
2. read this file;
3. read the current `main:docs/plan.md`;
4. follow the current work order from that plan;
5. create an issue before implementation when the logical change has none.

Normal product/model/module work starts from `dev` on one short-lived branch.
Set root `build.yml.branch` to that exact branch, select only the required
modules/models/tasks, and keep generated output below `build/`.

## Branch model

Permanent source branches are `main` and `dev`.

Required integration:

- short-lived product branch -> `dev`: squash;
- `dev` -> `main`: merge commit for an explicit stabilization checkpoint;
- `main` -> `dev`: merge commit only for real stable-only product content;
- governance-only `docs/* -> main`: squash under the restricted path contract.

Do not routinely sync a `dev -> main` promotion merge commit back into
`dev`.

### Mandatory merge execution rule

Every source-branch integration above is executed by posting `/merge` on the
pull request and letting `.github/workflows/merge-policy.yml` choose the merge
method.

Agents must never:

- call GitHub's direct merge API;
- enable or use auto-merge;
- use a UI merge as fallback;
- manually choose squash, merge or rebase.

If `/merge` fails, repair the policy path instead of bypassing it.

Temporary branches use only prefixes configured in root `ci.yml`. Successful
same-repository temporary branches are cleaned by
`modules/branch-cleanup`. `main` and `dev` are never cleanup candidates.

The generated `build` and `gh-pages` branches are not source branches and
are never cleanup candidates.

## Change discipline

Keep one logical change to one issue, branch and PR.

Model geometry or behavior changes must be described and reviewed before
implementation when the issue/change process requires it. Do not patch Forge
compiler/API behavior in a CAD model; Forge behavior belongs in
`brainboxemb/lib.py.solidcraft.forge`.

## CI selection modes

### Work branch / PR

A matching root `build.yml` controls explicit module/model/task selection.
A stale branch field is ignored and falls back to full selection.

### process-disabled model owners

A model-local `ci.yml` may set `process: false` to park that physical owner.
The owner remains discoverable and explicitly selectable on a matching work
branch, but permanent automatic selection and dependent expansion do not add it.

### dev

`build.yml` is ignored. CI selects changes since the last successful
`dev` push/workflow_dispatch baseline, plus declared impact. If no safe
baseline exists, run full.

### main

`build.yml` is ignored and the complete repository runs.

## Build output

Successful permanent source builds publish generated CAD artifacts to the
branch configured by `ci.yml.generated.build_branch`.

Current durable scopes are:

```text
main/
  build-plan.json
  models/
dev/
  build-plan.json
  models/
```

PR/work-branch output is verification-only unless a separately accepted generic
template capability changes that contract. Incremental `dev` publication
preserves unselected active model output; `main` replaces its complete scope.

## Pages

Hugo/Hextra presentation lives below `site/`.

The page data boundary is explicit:

- `model.yml`: presentation metadata;
- model-local `ci.yml`: build/source identity and variants;
- generated build scopes: accepted CAD artifacts;
- optional `page.md`: model-owned background prose;
- optional `extra_views`: model-owned additional reference/build views.

Shared layouts must not branch on model names. Pages never runs Forge or
SolidCraft and never duplicates generated CAD artifacts into `gh-pages`.

Pages runs separately after successful permanent build publication. Stable
`/` uses `main + build/main`; `/dev/` uses `dev + build/dev`.

## Model ownership

Every CAD model has one physical owner root below `models/`, discovered from
model-local `ci.yml`. One physical owner may expand into multiple build
variants.

Directory priority controls build order only. Physical dependencies must be
declared explicitly rather than encoded through directory ordering.

## External ownership

- Forge compiler/API behavior: `brainboxemb/lib.py.solidcraft.forge`;
- generic CAD project CI/build/Pages behavior:
  `brainboxemb/template.cad.model-project`;
- model-owned geometry, presentation and verification: this repository.
