# Repository handoff

This document is the easy-to-find handoff entrypoint for a new work session.
It contains one copyable handoff message below.

The handoff message is deliberately an entrypoint, not a second repository
plan. Current work must always be derived from live GitHub state and
`docs/plan.md`.

Shared SolidCraft/CAD documentation conventions live in
`brainboxemb/meta.cad.solidcraft`. Use `templates/docs/plan.md` and
`templates/docs/handoff.md` there as structural references.

## Handoff message

Copy the complete text block below into a new chat.

~~~text
You are continuing work on brainboxemb/2026-011-02.cad.solidcraft.

Repository role:

- this repository owns the migrated SolidCraft CAD model catalog;
- historical CAD source remains a geometry/design reference while unfinished
  model work is being ported, but historical CI/site plumbing is not a source
  for the migrated architecture;
- generic CAD CI/build/Pages behavior is owned by
  brainboxemb/template.cad.model-project and must not be re-invented locally.

Use this handoff only as the entrypoint. Do not treat copied handoff text as
fresher than GitHub or the repository plan.

Start by:

1. inspecting the current issues, pull requests and branches;
2. reading AGENTS.md;
3. reading the current `main` version of docs/plan.md;
4. treating `main:docs/plan.md` as the single source of truth for unfinished work;
5. following the current work order from the plan rather than from old handoff
   text;
6. creating an issue before implementation when the logical change has none;
7. keeping one logical change to one issue, branch and PR;
8. updating requirements/design documentation when behavior or architecture
   changes;
9. reconciling the plan after merge or release.

Durable working rules:

- main is stable and owns the canonical repository plan/handoff state;
- dev is the normal permanent development source branch and exp is the
  permanent isolated-experiment source branch;
- normal short-lived source work integrates to dev or exp through the
  repository-local /merge policy; dev <-> exp uses explicit permanent-lane
  checkpoints, accepted experimental work returns through dev, and dev promotes
  to main through that same policy; exp never promotes directly to main;
- governance-only changes limited to AGENTS.md, docs/plan.md and
  docs/handoff.md start from main on a docs/* branch and return directly to
  main through /merge;
- never choose a merge method directly or bypass
  .github/workflows/merge-policy.yml;
- model-owned source/data belongs here, while generic CI/build/Pages behavior
  belongs in brainboxemb/template.cad.model-project;
- generated CAD artifacts belong to generated branches, not source branches;
- generated build scopes are main/dev/exp plus one rolling test scope; test is
  output-only, and Pages exposes /, /dev/, /exp/ and /test/ when present;
- docs/plan.md and docs/handoff.md are main-owned governance state; do not
  create a main -> dev sync solely to copy plan/handoff metadata.

Shared document structures live in brainboxemb/meta.cad.solidcraft:
templates/docs/plan.md and templates/docs/handoff.md.

Do not copy exact current SHAs, runtime/release pins, active issue/PR status,
temporary migration phases or a short-lived "next actions" list into this
handoff. Those facts belong in GitHub and docs/plan.md.
~~~

## Maintenance

Keep this file as an entrypoint only. Repository-specific current state,
active workstreams and release/toolchain details belong in `docs/plan.md` and
GitHub.
