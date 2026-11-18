# 0001 — Targeted model builds and incremental publication

**Tracks:** issue #129  
**Scope:** model selection, verified build storage, Pages assembly and per-model verification metadata.

## Problem

The CAD library must scale beyond rebuilding every model for every model change.
Model selection, toolchain selection and publication state are separate concerns.

Generated output also needs to stay understandable. A separate `model-output`
branch and a flat `models/<slug>/` tree hide the relationship between source and
build output.

## Decision

Use one central model catalog and one tested selector.

Normal modes are:

- `changed` — build only affected models;
- `models` — build explicitly named model slugs;
- `all` — deliberate full-library regression.

A Forge or SolidCraft version change does not by itself select the full catalog.

The normal branch model is:

- `main` — editable source;
- `build` — verified technical CAD output;
- `gh-pages` — website only;
- active PR branches — temporary source work.

Do not introduce `model-output`, `qualified-output` or another generated
state branch.

The `build` branch has two scopes:

```text
main/<model-root>/...
pr/<number>/<model-root>/...
```

`<model-root>` mirrors the source model root. Examples:

```text
models/basic/plate/scpf/model.py
-> build/main/models/basic/plate/scpf/model/...

models/components/guide_rail/scpf/makita.py
-> build/main/models/components/guide_rail/scpf/makita/...

models/advanced/simple_mft/scpf/assemblies/guide_rail.py
-> build/main/models/advanced/simple_mft/scpf/assemblies/guide_rail/...
```

Each model directory owns its native/generated evidence plus
`verification.json` recording the exact CAD source commit, Forge/SCPC
revisions, SolidCraft version, workflow run, immutable toolchain image and
input fingerprint.

Stable promotion replaces only selected model directories and preserves
unchanged verified output byte-for-byte. A PR may replace only its own
`build/pr/<number>/` scope.

Pages is regenerated from the complete resolved build state. `gh-pages`
contains presentation only.

## Verification

Tests cover path-to-model selection, dependency selection, explicit build modes,
source-mirrored output paths, per-model verification metadata, incremental
replacement and complete site assembly.
