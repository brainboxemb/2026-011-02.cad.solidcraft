# 0001 — Targeted model builds and incremental publication

**Tracks:** issue #129  
**Scope:** model selection, verified output storage, Pages assembly and per-model verification metadata.

## Problem

The CAD library must scale beyond rebuilding every model for every model change.
Model selection, toolchain selection and publication state are separate concerns.

## Decision

Use one central model catalog and one tested selector.

Normal modes are:

- `changed` — build only affected models;
- `models` — build explicitly named model slugs;
- `all` — deliberate full-library regression.

A Forge or SolidCraft version change does not by itself select the full catalog.

Verified technical output lives on `model-output`, separate from `gh-pages`:

```text
stable/models/<slug>/
previews/<preview-key>/models/<slug>/
```

Each model owns a `verification.json` recording the exact CAD source commit,
Forge/SCPC revisions, SolidCraft version, workflow run and achieved verification.

Stable promotion replaces only selected model directories and preserves unchanged
verified output byte-for-byte. Pages is regenerated from the complete promoted
stable set plus current catalog/source.

## Verification

Tests cover path-to-model selection, dependency selection, explicit build modes,
per-model verification metadata, incremental replacement and complete site
assembly.
