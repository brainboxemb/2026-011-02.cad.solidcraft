# Repository handoff

This document is the easy-to-find handoff entrypoint for a new work session.
It contains one copyable handoff message below.

The handoff message is deliberately an entrypoint, not a second repository
plan. Current work must always be derived from live GitHub state and the
current stable `main:docs/plan.md`.

Shared SolidCraft/CAD documentation conventions live in
`brainboxemb/meta.cad.solidcraft`. Use `templates/docs/plan.md` and
`templates/docs/handoff.md` there as structural references.

## Handoff message

Copy the complete text block below into a new chat.

~~~text
You are continuing work on brainboxemb/2026-011-02.cad.solidcraft.

Repository role:

- this repository owns the migrated SolidCraft CAD model catalog;
- model-owned geometry, presentation and verification belong here;
- generic CAD CI/build/Pages behavior is owned by
  brainboxemb/template.cad.model-project and must not be re-invented locally;
- Forge compiler/API behavior remains owned by
  brainboxemb/lib.py.solidcraft.forge.

Use this handoff only as the entrypoint. Do not treat copied handoff text as
fresher than GitHub or the repository plan.

Start by:

1. inspecting the current issues, pull requests and branches;
2. reading AGENTS.md;
3. reading the current main version of docs/plan.md;
4. treating main:docs/plan.md as the single source of truth for unfinished work;
5. following the current work order from the plan rather than old handoff text;
6. creating an issue before implementation when the logical change has none;
7. keeping one logical change to one issue, branch and PR;
8. reconciling the main plan after merge or release.

Durable working rules:

- main is stable and dev is the permanent product/development lane;
- normal product/model/module changes start from dev;
- canonical docs/plan.md and docs/handoff.md are main-owned governance;
- governance-only docs/* branches originate from main and return directly to
  main through /merge; do not copy plan/handoff metadata to dev merely because
  it changed on main;
- all source integrations use the repository-local /merge policy; never choose
  or bypass the merge method manually;
- generated CAD artifacts belong to generated branches, not source branches;
- use template-owned generic behavior rather than repository-local CI/build/
  Pages forks.

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
