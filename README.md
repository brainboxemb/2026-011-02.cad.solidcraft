# 2026-011-02.cad.solidcraft.NEW

SolidCraft CAD model repository rebuilt on the accepted self-contained CAD
model-project architecture.

The repository is being migrated from
`brainboxemb/2026-011-02.cad.solidcraft` in staged batches. The old repository
remains the source for existing model geometry and open model-design issues
until each model has been accepted here.

## Architecture

- permanent source branches: `dev` and `main`;
- generated technical output: `build`;
- generated site: `gh-pages`;
- Forge and SolidCraft are pinned in root `ci.yml`;
- every model owns its own `ci.yml`, `model.yml` and source;
- directory group priority controls build ordering only;
- Pages is rebuilt separately after successful permanent build publication.

The template `simple-box` remains as an explicit example while real CAD models
are migrated.

## Migration

Migration is tracked by #1 and expands only after each stage is green:

1. one real model;
2. five real models;
3. ten real models;
4. remaining catalog.

The first real acceptance root is `models/basic/plate`.
