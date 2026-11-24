# Repository plan

This file contains unfinished work only.

## Now

### #1 — staged model migration

The repository is migrating the historical CAD catalog from
`brainboxemb/2026-011-02.cad.solidcraft` onto the accepted self-contained
CAD model-project architecture.

Accepted stages:

1. one real model — `plate`;
2. five real models — `plate`, `vent-plate`, `csg-cube`, `bracket`,
   `sample-plate`;
3. accepted template catalog presentation synced to this repository.

Current stage: **ten real model roots**.

The ten-root acceptance branch selects all ten physical owners:

- `plate`;
- `vent-plate`;
- `csg-cube`;
- `bracket`;
- `sample-plate`;
- `plastic-enclosure`;
- `plastic-enclosure-pi`;
- `bolted-flange`;
- `guide-rail`;
- `flex-bench-dog`.

`guide-rail` is one physical owner with two build variants:
`guide-rail` and `guide-rail-makita`.

`flex-bench-dog` retains STL export and its model-owned underside snapshot
through declarative `ci.yml` configuration.

`bolted-flange` retains historical issue #135 about replacing its Python
bolt-hole loop with a native circular pattern. Migration preserves the current
accepted source; do not silently solve that issue during transfer.

## Migration ordering

Directory priorities are:

```text
models/basic       10
models/components  20
models/advanced    30
```

Lower priority builds first. Equal priority is ordered by owner id.

This is ordering only. It does not imply dependencies or propagate selection.

## Source boundary

The historical repository remains the source for existing model geometry and
open model-design issues until each model is migrated.

Do not copy its repository-local CI/site architecture or historical CAD-specific
`model.yml` schema. Build/source identity belongs in model-local `ci.yml`;
presentation belongs in canonical `model.yml`.

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- directory-local model build priority;
- local merge-policy dispatches target CI and branch cleanup;
- standalone cleanup removes merged temporary branches;
- direct Forge -> JSON -> one SolidCraft replay batch;
- Forge v0.14.0 / SolidCraft 0.48.1 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with implicit primary snapshot;
- physical model owners may expand into multiple build variants;
- internal Python capabilities run directly from source;
- Pages runs separately from CAD CI and is explicitly dispatched after build publication;
- Pages publishes stable `/` and development `/dev/` as one generated `gh-pages` tree.

## Next

Accept the full ten-root batch on PR, durable `dev`, build publication and
Pages before widening to the remaining catalog.
