# 0002 — One tested CAD workflow

**Tracks:** issue #134  
**Scope:** CAD CI orchestration, native verification, publication and PR cleanup.

## Problem

The repository exposes several GitHub Actions workflows for what is one normal
operation: CAD CI. The operator has to understand separate CAD, native,
publication and cleanup actions, while repository policy is duplicated in YAML.

That is unnecessary for a one-person project.

## Decision

Expose one normal user-facing workflow:

```text
.github/workflows/cad.yml
name: CAD
```

One CAD run owns the normal chain:

```text
select
-> cheap source/command checks
-> native checks when selected
-> build verified candidate
-> publish build/Pages when allowed
```

A closed PR enters the same CAD workflow and removes that PR's generated
`build/pr/<number>/` and Pages preview.

The operator does not select separate `native`, `publish` or `cleanup`
workflows.

## Workflow versus Python

GitHub Actions YAML is wiring only:

```text
checkout -> reusable image -> tested Python entry point
```

Selection, path rules, model loops, native verification, publication target
validation, build promotion and cleanup live in tested Python under
`scripts/ci/` or in model-owned `check.py` files.

Keep one central model catalog. Do not duplicate model lists in workflows.

## Performance exception

`.github/workflows/image.yml` remains a separate workflow because it builds
and caches the immutable CAD toolchain image. Rebuilding that image inside each
CAD run would make normal CI substantially slower.

Additional workflows are allowed only for a similarly concrete performance or
technical-isolation reason. Do not split a workflow merely because the pipeline
has multiple stages.

## Verification

A change to the CAD pipeline itself automatically adds the `plate` model as one
real end-to-end native smoke. This proves the complete image -> compile ->
SolidCraft -> candidate -> preview chain without turning an infrastructure
change into a full-catalog rebuild.

Model-owned `check.py` modules are imported and shape-checked by cheap unit
tests. A CI refactor therefore does not need to native-build every model merely
to prove that those check modules load.

Contract tests require:

- one normal workflow named `CAD`;
- no separate normal native/publish/cleanup workflow;
- `image.yml` is explicitly the reusable toolchain-image performance worker;
- workflow YAML contains no model-specific assertions or publication policy;
- Python modules have unit tests for selection, build planning, native checks,
  promotion, cleanup and publication.
