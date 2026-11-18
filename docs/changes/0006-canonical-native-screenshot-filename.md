# 0006 — Canonical native screenshot filename

**Tracks:** issue #140  
**Scope:** primary native screenshots stored under `build` and rendered on Pages.

## Problem

The new native runner writes the primary screenshot as
`native/model.png`. Legacy verified output used `native/native.png`.

The initial migration preserved the old filename, so migrated models remained
verified but the site builder could not find their screenshot. A freshly
rebuilt model such as `plate` displayed correctly while migrated models fell
back to schematic artwork.

## Decision

Use exactly one canonical primary screenshot path:

```text
<build item>/native/model.png
```

Stable publication normalizes any migrated `native/native.png` to
`native/model.png` before committing `build` and before rebuilding Pages.

If both names exist, keep the canonical `model.png` and remove the legacy
duplicate. Model-specific extra views such as `front.png` and `rear.png`
remain unchanged.

Legacy Pages bootstrap also writes the canonical filename directly.

Do not add a permanent dual-filename lookup to the site builder.

## Verification

Tests cover renaming an old primary screenshot, preserving verification
metadata, removing a duplicate legacy filename, idempotence and canonical
naming during future legacy bootstrap.
