# 0002 — Tested CI orchestration

**Tracks:** issue #134  
**Scope:** CAD/native/publish workflow structure and model-owned checks.

## Problem

The workflows contain repository policy and model semantics: git-diff logic,
model loops, JSON parsing, model-specific assertions and publication decisions.
That logic is difficult to unit-test and easy to duplicate.

## Decision

GitHub Actions YAML is orchestration only:

`checkout -> setup/image -> tested Python command -> artifact/publisher`

Move policy into normal Python modules under `scripts/ci/` or beside the model
that owns the check.

Keep one central model catalog. Do not duplicate model lists in workflows.

Model-specific generated/native assertions live with the model or in a generic
model-check loader, not inline in YAML.

Use short workflow names:

- `cad.yml`
- `native.yml`
- `publish.yml`
- `pr-cleanup.yml`

## Verification

Contract tests reject inline Python/heredoc policy, model-specific JSON assertions
and duplicated change-selection logic in workflow YAML. Python modules receive
normal unit tests for selection, build planning, checks and publication rules.
