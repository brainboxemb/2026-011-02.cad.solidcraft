# 0012 — Migrate generic CAD CI lifecycle to tool.cad.ci

Issue: #155

## Problem

The CAD repository currently owns two different kinds of CI code in the same
`scripts/ci/` tree.

The first kind is CAD-specific:

- the model catalog;
- model and component dependencies;
- SCPF/SCPC compilation;
- native SolidCraft verification;
- verification metadata;
- CAD result-page content and styling.

The second kind is generic repository plumbing:

- changed-file planning;
- step execution and reruns;
- durable `build` branch layout;
- PR overlays and stable promotion;
- Pages stable/preview replacement;
- generated-branch push retries and source-freshness checks.

That second group now exists as a tested released product in
`tool.cad.ci v0.2.0`. Keeping a second implementation in this repository
would make the two CI systems drift again.

## Decision

Pin `tool.cad.ci v0.2.0` by exact commit in `dependencies.repos` and check it
out below `ext/cad-ci`.

The CAD repository invokes the tool through:

```text
python ext/cad-ci/cad-ci.py ...
```

Do not import the external `cad_ci` Python package from `scripts/ci/`.
This repository already has `scripts/ci/cad_ci.py`; keeping the executable
boundary avoids an ambiguous import during migration.

### Item ownership

A CAD model root is the CI item.

For example:

```text
models/basic/plate/
  ci.yml
  README.md
  scpf/
  scpc/
```

The model folder owns the commands and inputs needed to check that model.
Generic execution state is written by `tool.cad.ci`.

The durable item path mirrors the model-root source path:

```text
build/main/models/basic/plate/
build/pr/<number>/models/basic/plate/
```

This replaces the older generated path derived from the source filename
(`models/basic/plate/scpf/model/`) once the build-store cutover occurs.

The central model catalog remains the source for CAD/model metadata and public
site content. CI execution rules move to the owning item folder. Do not copy
model titles, descriptions or website metadata into `ci.yml`.

### Migration order

Do not switch the complete CAD pipeline in one unproved change.

1. Add the exact `tool.cad.ci` dependency and bootstrap it as external tooling.
2. Add one `ci.yml` to the simple Plate model.
3. Run the Plate item through `tool.cad.ci` in parallel with the current CAD
   checks. This first proof does not replace stable build or Pages output.
4. Compare generated commands/check results with the existing Plate pipeline.
5. Convert the remaining model items and their declared dependencies.
6. Migrate the durable build baseline from the old source-file-derived layout
   to model-root item paths without dropping verified evidence.
7. Switch generic build/PR promotion and Pages stable/preview publication to
   `tool.cad.ci`.
8. Remove the replaced generic planning/publication code only after the new
   end-to-end CAD run is green.

The parallel period is temporary migration evidence, not a permanent second CI
pipeline.

### Build and Pages boundary

`tool.cad.ci` owns:

- item planning and generic rerun state;
- `build/main` and `build/pr/<number>` mechanics;
- overlay resolution and promotion;
- normal-push generated-branch publication and retry;
- stable Pages root and `previews/pr-<number>` lifecycle;
- generic Pages provenance/framework where used.

The CAD repository keeps:

- native verification rules and fingerprints;
- CAD-specific `verification.json`;
- SolidCraft/SCPF/SCPC commands;
- model selection semantics that are genuinely CAD-specific during migration;
- CAD site page content;
- CAD stylesheet/theme.

The tool must not gain model slugs or SolidCraft-specific rules.

## Verification

Before the old generic path is removed:

- `dependencies.repos` pins the released v0.2.0 commit;
- local/CI bootstrap checks out that exact commit;
- Plate can be planned and run through `ext/cad-ci/cad-ci.py`;
- a Plate-only source change does not select unrelated models;
- a stale prerequisite prevents a partial rerun instead of rebuilding silently;
- the tool-produced Plate command/check output matches the current CAD path;
- a PR can publish only its selected model-root overlay;
- stable promotion preserves every unchanged model item;
- stable Pages publication preserves PR previews;
- build and Pages writes use normal pushes and source-freshness checks;
- existing verified CAD evidence is retained until its item has a proven
  replacement.
