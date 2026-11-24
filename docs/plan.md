# Repository plan

This file contains unfinished work only.

## Now

### #48 — restore `gh-pages` publication

Keep Pages separate and asynchronously dispatched after build publication, but
publish the combined stable `/` and development `/dev/` site to the generated
`gh-pages` branch. Do not use `actions/deploy-pages` or a `github-pages`
environment.

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- local merge-policy dispatches target CI and branch cleanup;
- standalone cleanup removes merged temporary branches;
- direct Forge -> JSON -> one SolidCraft replay batch;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with implicit primary snapshot;
- physical model owners may expand into multiple build variants;
- internal Python capabilities run directly from source;
- Pages runs separately from CAD CI and is explicitly dispatched after build publication;
- Pages publishes stable `/` and development `/dev/` as one generated `gh-pages` tree.

## Next

After #48 is accepted, treat this template as the v1 baseline and start
migrating real CAD models. Add explicit model dependencies only when the first
advanced/assembly migration supplies a concrete dependency case.
