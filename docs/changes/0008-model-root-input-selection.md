# 0008 — Select model-root metadata in targeted CAD CI

Issue: #144

## Problem

Targeted CAD selection watches model source paths and explicit extra inputs, but
does not automatically watch model-root metadata such as `README.md` and
`check.py`.

A GuideRail README-only change therefore merged successfully without selecting
GuideRail. Pages was republished from the previous stable GuideRail output, so
the new measurement-source warning did not appear on the public model page.

The same gap can hide changes to a model-owned native `check.py`.

## Decision

Treat model-root metadata as an input of the **catalog models that own that root**:

- `<model-root>/README.md`
- `<model-root>/check.py`

Keep geometry/component dependency propagation separate. A README or snapshot
camera change in a reusable component must not force every dependent assembly
to rebuild.

Therefore:

- `direct_input_paths()` remains the geometry/source input set used through
  dependency closure;
- `model_metadata_paths()` returns the owning model's root metadata;
- `model_input_paths()` combines the owning metadata with geometry inputs from
  the model and its declared dependencies.

## Verification

- GuideRail README-only changes select both GuideRail profile pages that share the root;
- GuideRail README-only changes do not select Simple MFT;
- a model-root `check.py` change selects only that model;
- source changes still select all declared geometry dependants;
- unrelated README files select no CAD model;
- after merge, GuideRail is rebuilt/promoted and the public page contains the
  measurement-source warning.
