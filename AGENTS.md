# Agent guidance

## Purpose

This repository is a reusable, self-contained CAD model-project template.

Models and Python capabilities use the same ownership pattern: each item has
its own directory, configuration and tests/verification.

## Start work

Before changing anything:

1. read `docs/plan.md`;
2. create/switch to a short-lived branch from `dev`;
3. update root `build.yml.branch` to the exact branch name;
4. select only the modules/models this branch changes;
5. select only the required tasks;
6. keep generated output below `build/`.

## Branch model

Permanent source branches are only `main` and `dev`.

Required integration:

- short-lived branch -> `dev`: squash;
- `dev` -> `main`: merge commit when promoting accepted development;
- `main` -> `dev`: merge commit only when `main` contains actual content
  that is not already present on `dev`, for example a stable-branch hotfix.

Do not create a `main` -> `dev` PR merely to copy the promotion merge
commit back into `dev`.

Temporary branches use only configured prefixes from root `ci.yml`.

After a successful same-repository short-lived PR is merged into `dev`, its
source branch is removed by `modules/branch-cleanup`.

`main` and `dev` are never cleanup candidates.

The generated `build` branch is not a source branch. It stores generated technical
output for the permanent source scopes and is never a cleanup candidate.

The generated `gh-pages` branch is also not a source branch. Pages are built
from `main + build/main` and `dev + build/dev`, assembled as one tree, and
published there after successful build publication.

## CI selection modes

CI has three modes.

### Work branch / PR

If `build.yml.branch` matches the actual branch, use its explicit
module/model/task selection.

If it does not match, ignore `build.yml` and run full. A stale build file is
not a CI failure.

### dev

Ignore `build.yml`.

Use the last successful dev **push/workflow_dispatch** CI SHA as baseline and
the current dev SHA as target. Build/test the changed items in that Git range,
plus item-declared impact.

A cancelled dev run never advances the successful baseline. If two squash
merges arrive quickly, the newer run therefore includes changes not completed
by the cancelled run.

If no safe successful baseline exists, run full.

### main

Ignore `build.yml` and run full.

## Build output

Successful permanent-branch model builds publish to the generated branch
configured by `ci.yml.generated.build_branch`.

The generated branch contains complete build scopes:

```text
dev/
  build-plan.json
  models/
main/
  build-plan.json
  models/
```

PR/work-branch output is verification-only and is never published. Incremental
`dev` publication replaces only rebuilt model directories and preserves other
active model output. `main` is full and replaces its complete scope.

## Pages

Hugo/Hextra presentation lives below `site/`.

The page data boundary is explicit:

- `model.yml`: presentation metadata;
- `ci.yml`: build/source identity and variants;
- generated `build/main`: accepted model artifacts;
- optional model-local `page.md`: additional background prose;
- optional model metadata `extra_views`: additional reference/build views.

Shared layouts must not branch on model names. Model-specific content belongs in
model-owned metadata/resources. Pages never runs Forge or SolidCraft.

Pages runs separately from CAD CI. After successful permanent build
publication, CI dispatches `pages.yml` and finishes without waiting. That
workflow rebuilds both the stable root and `/dev/`, then publishes the complete
tree to `ci.yml.generated.pages_branch` (`gh-pages`).

## Item impact

Impact is declared by the item that owns it, not by a central model catalog.

- `modules/ci`: `impact: full`;
- `modules/build`: `impact: models`;
- other modules default to self;
- models default to self.

An item may add extra watched paths, for example its thin workflow YAML.

## Python modules

Every Python capability is a standalone item:

```text
modules/<id>/
  ci.yml
  pyproject.toml
  src/
  tests/
```

Tests for a capability live under that module. Root-level Python tests are not
allowed.

## Models

Every CAD model is a standalone item under `models/<id>/`.

Do not create a central model catalog in Python.

## Workflows

Workflow YAML stays thin and bootstraps only its owning module.

The CI workflow uses concurrency with cancellation so a newer run supersedes an
older run for the same Git ref.

## External ownership

Forge compiler/API behavior remains owned by
`lib.py.solidcraft.forge`.

Normal repository CI/build/merge/cleanup behavior is local to repositories
created from this template.
