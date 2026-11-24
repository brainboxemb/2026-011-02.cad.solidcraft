# Repository handoff

~~~text
Continue work on brainboxemb/2026-011-02.cad.solidcraft.NEW.

Read AGENTS.md and docs/plan.md first.

Repository purpose:
- this is the migrated SolidCraft CAD model catalog;
- the historical brainboxemb/2026-011-02.cad.solidcraft repository remains the
  geometry/design source only while unfinished model work is still being ported;
- generic CI/build/Pages behavior comes from template.cad.model-project and
  should not be re-invented locally.

Current state:
- the full catalog migration is accepted: 16 physical model owners / 18 build variants;
- generated CAD artifacts are owned by the generated build branch, not source branches;
- Forge v0.15.0 / SolidCraft 0.48.1 / runtime v0.3.5 is the accepted CAD baseline;
- HUB75 component-local replay regression #31 is fixed and closed;
- dev now uses the simplified Forge release contract from template #97:
    forge.repository: brainboxemb/lib.py.solidcraft.forge
    forge.version: v0.15.0
  with no SHA, plus root bootstrap.ps1 for local development (PR #55);
- main still reflects the previous exact-SHA dependency contract until the accepted
  dev state is promoted;
- PR #52 is the active Simple MFT assembly correction: both 1 m support-rail
  C/open sides face outward and reusable components receive realistic materials;
  re-check it against the latest dev state before integration;
- #12 remains the umbrella for transferring relevant historical CAD issues/PRs;
  focused migrated model work is tracked in #13 through #22.

Immediate continuation:
1. reconcile/finish the open Simple MFT assembly work (#52) against current dev;
2. integrate source branches only through the repository-local /merge policy;
3. promote accepted dev to main with a merge commit when the development state is ready;
4. continue #12 by porting only relevant model-owned source/data from historical work;
5. do not copy historical CI/site plumbing into this repository.

Core branch rules:
- main is stable; dev is the only permanent development source branch;
- short-lived branch -> dev is squash;
- dev -> main promotion is a merge commit;
- main -> dev happens only for real stable-only content, never merely to copy a
  promotion merge commit;
- agents never choose the merge method directly: post /merge on the PR and let
  .github/workflows/merge-policy.yml execute it;
- do not use direct merge API, auto-merge, UI merge, or manual fallback;
- docs/handoff.md is maintained directly on main as handoff metadata; do not
  create a main -> dev sync merely for a handoff-only update.

Work-branch/CI rules:
- root ci.yml owns stable toolchain, permanent/generated branches and repository roots;
- root build.yml selects the exact temporary work branch and only the items/tasks
  needed for that branch;
- a stale build.yml is ignored rather than treated as a CI error;
- dev uses changed-item selection from the last successful dev integration baseline;
- main ignores build.yml and runs full;
- generated model output is published below build/{dev,main};
- Pages runs separately after successful permanent build publication.

Model ownership:
- every CAD model is a physical owner root below models/ and is discovered from
  model-local ci.yml;
- one physical owner may expand into multiple build variants;
- model.yml owns presentation metadata;
- model-local ci.yml owns source/build identity and variants;
- optional page.md and extra_views extend presentation without model-name
  branches in shared Hugo layouts;
- models default to self impact; physical dependencies must be explicit rather
  than encoded through directory priority;
- directory priorities are ordering only: basic 10, components 20, advanced 30.

Local development:
- after the release-tag/bootstrap change is present on the branch:
    .\bootstrap.ps1
    python -m scpf models/.../scpf/model.py --connect --new
- do not manually install or pin Forge by SHA for normal released CAD work.
~~~
