# 0015 — Remove legacy CAD publication code

Status: implementation

## Goal

Remove publication/store code that became dead after the successful
tool.cad.ci cutover.

## Changes

- native verification no longer builds a second temporary website;
- native verification no longer writes the old `output/publish.json` handoff;
- the pipeline requires an existing tool.cad.ci `build/main/build.json`
  baseline and no longer migrates legacy stores;
- `output_store.py` now owns only the native input fingerprint and temporary
  verified candidate used by the model-root package step;
- old promote, preview, prune and legacy Pages/store migration code is removed;
- stale diagnostic artifact paths for `output/site` and
  `output/publish.json` are removed;
- the model-root tool runner is named as the real item runner rather than a
  migration proof.

CAD-native verification and CAD website generation remain separate: native
verification runs in the immutable CAD image, while the host publisher renders
the website once from the complete resolved durable build view.
