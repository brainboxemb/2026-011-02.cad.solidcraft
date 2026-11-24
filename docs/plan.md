# Repository plan

This file contains unfinished work only.

## Now

### #1 — bootstrap and staged model migration

Bootstrap the accepted CAD model-project architecture, establish permanent
`dev` / `main` operation and migrate the historical CAD catalog in widening
accepted batches.

Current stage:

1. template baseline accepted on `main`;
2. permanent `dev` created from that exact baseline;
3. migrate one real model: `models/basic/plate`;
4. prove normal PR, `dev`, build publication and Pages behavior;
5. only then widen to five real models.

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

After the one-model Plate acceptance is green, migrate four additional basic
models as the five-model batch. Do not widen further until that batch is
accepted.
