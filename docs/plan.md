# Repository plan

This file contains unfinished work only.

## Now

### #1 — staged model migration

The repository has accepted the self-contained CAD model-project architecture
and is migrating the historical catalog from
`brainboxemb/2026-011-02.cad.solidcraft`.

Accepted migration stages:

1. one real model — `plate`;
2. five real models — `plate`, `vent-plate`, `csg-cube`, `bracket`,
   `sample-plate`.

Current work:

1. sync the accepted template catalog presentation:
   - Recently updated models on the landing page;
   - Models / Basic / Components / Advanced navigation;
   - grouped model catalog;
   - real category index pages;
   - Git-derived last-modified dates;
   - Pages PR verification against the matching durable build scope;
2. accept that sync on `dev`;
3. continue to the ten-real-model stage.

## Stage 3 — ten real models

Target five additional roots:

- `plastic-enclosure`;
- `plastic-enclosure-pi`;
- `bolted-flange`;
- `guide-rail`;
- `flex-bench-dog`.

The ten-model acceptance branch must select all ten real models, not only the
five newly added roots.

`bolted-flange` retains historical issue #135 about replacing the Python
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

The historical repository
`brainboxemb/2026-011-02.cad.solidcraft` remains the source for existing model
geometry and open model-design issues until each model is migrated.

Do not copy its repository-local CI/site architecture or its historical
CAD-specific `model.yml` schema.

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

After the template catalog sync is accepted, build and validate the ten-model
stage. Do not widen beyond ten real models until PR CI, durable `dev`, build
publication and Pages are all green.
