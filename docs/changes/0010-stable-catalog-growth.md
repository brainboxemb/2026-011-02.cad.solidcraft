# 0010 — Stable publication across catalog growth

Issue: #150

## Problem

The generated `build/main` branch is already the source of truth for stable
native model output. When a new native catalog model is added, however,
`stable_complete()` is false until that one model is promoted.

The publisher currently interprets every incomplete stable store as an
unfinished legacy migration and falls back to bootstrapping from gh-pages.
That is wrong after migration and failed when HUB75Display2 increased the
catalog from 17 to 18 models.

## Decision

Classify an incomplete modern stable store before considering legacy bootstrap.

- If no current catalog model exists in `build/main`, legacy migration or
  bootstrap may still run.
- If current stable models exist and every missing catalog model is part of the
  current verified candidate, skip legacy bootstrap and promote the candidate.
- If current stable models exist but another catalog model is missing outside
  the candidate, fail clearly instead of using gh-pages as an implicit recovery
  source.

After candidate promotion the existing complete-store check remains mandatory.

This keeps `build/main` authoritative after migration and makes adding a new
catalog model a normal targeted publication.

## Verification

Regression tests cover:

1. empty modern store -> bootstrap required;
2. catalog growth where the candidate covers every missing model -> no
   bootstrap;
3. incomplete modern store with an uncovered missing model -> explicit failure.

The existing promotion tests continue to prove that selected model promotion
preserves unrelated stable model output.
