# 0010 — Stable publication across catalog growth

Issue: #150

## Problem

The `build` branch is the durable store of verified native CAD output. When a
new native catalog model is added, `build/main` is temporarily incomplete
until that model has been built and promoted.

The pipeline currently assumes every catalog model already exists in stable
storage when it builds the results site. HUB75Display2 exposed this: the
existing 17 models were present, the new 18th model was not, and a later site
refresh failed before publication because there was no generated or stored
command JSON for the new model.

The publisher also treats any incomplete stable store as unfinished legacy
migration and falls back to gh-pages bootstrap. That is wrong once
`build/main` already contains modern per-model output.

## Decision

Catalog growth is a normal targeted-build state.

### Pipeline

After resolving the stable `build/main` baseline, compare the current native
catalog with the verification files present in that store.

Any missing current catalog model is automatically added to the current build
plan for every build kind it supports:

- SCPF compile;
- SCPC comparison where available;
- native SolidCraft verification;
- required native snapshot.

This comes entirely from the central `MODELS` catalog and its derived model
lists. No model name or catalog count is hardcoded.

The site refresh/publish flags are enabled when such missing models are added.

### Stable publication

Before stable promotion:

1. if no modern current-catalog model exists in `build/main`, legacy bootstrap
   may still run;
2. if a modern store exists and every missing model is included in the current
   verified candidate, promote that candidate normally;
3. if a modern store exists but another catalog model is missing outside the
   candidate, fail explicitly instead of silently using gh-pages as recovery.

After promotion the store must be complete for the current native catalog.

## Verification

Tests cover:

- deriving missing models from the catalog/store, not a literal count;
- extending a normal/smoke plan with a newly missing native model;
- preserving catalog order and build-kind eligibility;
- empty modern store still allows legacy bootstrap;
- catalog growth covered by the candidate skips legacy bootstrap;
- an incomplete modern store with uncovered missing models fails;
- existing stable model output remains untouched by promotion of the new model.
