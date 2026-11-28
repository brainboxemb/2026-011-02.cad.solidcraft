# Model project manual

## Stable configuration

Root `ci.yml` defines permanent source branches (`main`, `dev`, `exp`),
the generated build branch, Forge/SolidCraft versions and repository roots. Forge is selected by its
released Git tag, for example `version: v0.16.0`. Local bootstrap and CI use
that same release version.

## Local bootstrap

Run the repository bootstrap after cloning or whenever the pinned Forge release
changes:

```powershell
.\bootstrap.ps1
```

The bootstrap reads `dependencies.forge.version` from root `ci.yml`,
installs SCPF directly from that release tag's `cadlib/` package and checks the installed package
version plus the SolidCraft version qualified by that Forge release.

After bootstrap, models can be sent directly to an open SolidCraft GUI:

```powershell
python -m scpf models/assemblies/simple_mft_assembly/scpf/model.py --connect --new
```

No Forge SHA is part of the normal model-project workflow.

## Temporary Forge qualification

A temporary work branch may qualify the real catalog against one unreleased
Forge commit without changing the released Forge baseline in `ci.yml`.

Use an exact immutable commit SHA in a matching root `build.yml`:

```yaml
schema: 1
branch: chore/forge-exp-qualification

modules: all
models: all
tasks: [test, build]

qualification:
  forge:
    ref: 0123456789abcdef0123456789abcdef01234567
```

The override is accepted only when `build.yml.branch` matches the current
work branch. `ref` must be exactly 40 lowercase hexadecimal characters;
branches and tags are rejected so qualification evidence cannot move.

The normal `ci.yml.dependencies.forge.version` remains the released
`vX.Y.Z` baseline. Generated `build-plan.json` records that version and
adds `forge.qualification_ref` for the exact candidate used by the temporary
run.

Permanent `dev`, `exp` and `main` CI ignore work-branch `build.yml`, and
`bootstrap.ps1` remains release-only.

## Rolling test output

A temporary work branch can make its generated CAD result reviewable without
creating a permanent source branch or a per-PR output directory.

Add this to the matching root `build.yml`:

```yaml
output:
  scope: test
```

The request requires the `build` task. A successful PR build remains bounded
to its selected models. Publication then creates a fresh complete
`build/test` scope from the current durable `build/dev` catalog and overlays
the selected candidate model outputs before rebuilding Pages at `/test/`.

There is deliberately only one rolling test output. A later successful test
publication replaces the earlier one. Unselected active model artifacts and
their own `built_source_sha` evidence come from the durable dev baseline;
candidate rows replace only the models rebuilt by the PR. Nothing is retained
under a PR-specific directory, so no PR-close cleanup process exists.

The test `build-plan.json` records the exact source branch and source SHA plus
the normal released Forge baseline and, when used, the exact
`qualification.forge.ref`. This makes `/test/` suitable for visually
reviewing an unreleased Forge candidate or a CAD work branch before integration.

Ordinary PRs remain verification-only unless they explicitly request
`output.scope: test`.

## Experimental lane

`exp` is a permanent source lane, not a test-output alias. It has its own
`build/exp` generated scope and Pages presentation at `/exp/`.

Normal work branches may target `exp` for isolated experimental development.
Permanent `dev -> exp` synchronization and `exp -> dev` integration use merge
commits through the repository-local merge policy. `exp -> main` is not an
allowed route; accepted experimental work returns through `dev` before any
stable `dev -> main` promotion.

## Branch integration

All source-branch integrations are executed through the repository-local merge
policy. After the PR-specific central `ci` check is green, post:

```text
/merge
```

on the PR conversation. `.github/workflows/merge-policy.yml` then validates
the PR and selects the merge method.

Agents must never call GitHub's direct merge API, enable auto-merge, use the UI
merge button as a fallback, or manually choose squash/merge/rebase. If the
`/merge` path fails, fix that path instead of bypassing it.

The merge-policy owns:

- short-lived branch -> `dev` or `exp`: squash;
- `dev` <-> `exp`: merge commit;
- `dev` -> `main`: merge commit;
- exceptional `main` -> `dev`: merge commit;
- `exp` -> `main`: rejected.

Promote accepted development with a merge-commit PR from `dev` to `main`.

Do not routinely merge `main` back into `dev` after that promotion. The
promotion merge commit itself does not need to be copied back.

Use `main` -> `dev` only when `main` contains real content that `dev`
does not have, such as a stable-branch hotfix. That integration also uses a
merge commit.

## CI modes

### Work branch / PR

A matching root `build.yml` controls exactly what runs:

```yaml
schema: 1
branch: issue/15-ci-change

modules:
  - ci
models: []
tasks:
  - test
  - build
```

If the branch field does not match the actual work branch, the file is ignored
and CI falls back to full.

### dev / exp

`build.yml` is ignored on both permanent development lanes.

CI finds the most recent successful push/workflow_dispatch run on the same lane
and uses its SHA as the baseline. The current lane SHA is the target.

```text
git diff --name-only <successful-baseline> <current-lane>
```

Only changed items plus declared impact run.

Because superseded runs are cancelled, an unfinished run never becomes the
baseline. A later dev run therefore automatically catches all changes since
the last successful one.

### main

`build.yml` is ignored and the complete repository runs.

## Item impact

Item-local `ci.yml` may declare:

```yaml
impact: self
```

or:

```yaml
impact: models
```

or:

```yaml
impact: full
```

Items can add extra watched paths:

```yaml
watch:
  - .github/workflows/ci.yml
```

Model ids are discovered from model roots; they are never centrally listed in
Python.

### Model group priority

A directory above one or more model roots may define build ordering:

```yaml
schema: 1
kind: group
priority: 20
```

Models inherit the nearest ancestor group. Lower values build first; equal
values are ordered by physical owner id. If no group exists, priority `1000`
is used.

Typical migration ordering is:

```text
basic / fundamentals   10
components             20
advanced / assemblies  30
```

Priority controls ordering only. It does not imply a model dependency and does
not propagate selection.

### Model dependencies

A model that consumes another physical model owner declares that relationship
explicitly in its own `ci.yml`:

```yaml
dependencies:
  - hub75-panel
  - corner-bracket
```

Dependencies name physical owner ids, not build-variant ids. Unknown, self and
cyclic dependencies are invalid.

Any explicit or incremental model selection is closed transitively over
downstream dependents. A change to a reusable component therefore also rebuilds
every consuming assembly. The build plan orders selected dependencies before
their consumers; directory priority and owner id remain the deterministic order
among models that are otherwise ready.

## Output

Generated artifacts remain below root `build/`.


## Model builds

Root `ci.yml` pins the complete qualified CAD toolchain:

- Forge repository and released version tag;
- released SolidCraft runtime image and exact SolidCraft version.

Model-local `ci.yml` owns build execution. A minimal processed model declares
its id and Forge source. The primary `model.png` uses the normal SolidCraft
snapshot view unless the model explicitly owns a primary review camera.

The primary camera is optional and separate from additional named snapshots:

```yaml
snapshot:
  camera:
    target: [0, 0, 160]
    yaw: -0.24
    pitch: 0.20
    distance: 920
    fov: 0
```

Only optional build extras belong in the model config, for example STL or
additional named snapshots:

```yaml
schema: 1
id: simple-box
builder: forge
source: scpf/model.py
process: true

artifacts:
  - stl

snapshots:
  - name: top.png
    camera:
      target: [0, 0, 5]
      yaw: 0
      pitch: -1.55
      distance: 90
      fov: 0
```

If `snapshot` is omitted, the primary `model.png` uses SolidCraft's default
camera. If `snapshots` is omitted, no additional named PNGs are rendered.
Additional snapshots may provide their own camera independently of the primary
snapshot camera.

A physical model root may own multiple build variants. CI still selects the
physical owner once; the build plan expands all of its variants. Pages presents
a multi-variant root as one physical owner with the variants underneath it.
Existing variant detail URLs remain stable.

Owner-level `title`, `tagline` and `description` are optional presentation
metadata. `variant_groups` may group build-variant ids on the owner page:

```yaml
title: Guide Rail
tagline: Guide-rail family with multiple interface profiles
description: Shared guide-rail component family.
variant_groups:
  - title: Standard
    variants: [guide-rail]
  - title: Alternatives
    variants: [guide-rail-makita]

variants:
  guide-rail:
    title: Guide Rail
    tagline: Standard profile
    description: Standard guide-rail profile.
    parameters: 800 mm
  guide-rail-makita:
    title: Guide Rail — Makita
    tagline: Makita profile
    description: Makita-compatible profile.
    parameters: 800 mm
```

`variant_groups` is presentation-only and follows variant ids from `ci.yml`.
A variant may appear in at most one declared group. Variants not listed in a
group remain visible under `Other variants`. Without owner-level presentation
metadata, Pages falls back deterministically to the first declared variant.

The build configuration remains:

```yaml
schema: 1
id: guide-rail
builder: forge
process: true

variants:
  - id: guide-rail
    source: scpf/model.py
  - id: guide-rail-makita
    source: scpf/makita.py
```

`source` and `variants` are mutually exclusive. Owner-level `artifacts` and
`snapshots` apply to every variant. Variant output is stored by variant id,
while the plan also records the physical owner id.


CI selects physical model ids. The build module then performs one repository
scan and writes a deterministic `build-plan.json`.

For every selected model the normal build path is fixed:

```text
model.py
  -> pinned Forge on the CI runner
  -> solidcraft.json
  -> one shared SolidCraft Docker replay batch
  -> model.sc
  -> model.step
  -> model.png
  -> optional model.stl / extra PNG snapshots
  -> optional native drawings/*.pdf declared by Forge
```

Forge compilation and SolidCraft replay are separate visible phases. The
stored `solidcraft.json` is exactly the document replayed by SolidCraft.

During a run, generated output is written below the checkout:

```text
build/
  main/
    build-plan.json
    models/
  dev/
    build-plan.json
    models/
  exp/
    build-plan.json
    models/
  test/
    build-plan.json
    models/
```

Successful permanent-branch runs then publish that scope to the generated
`build` branch. On that branch the repository root is:

```text
main/
  build-plan.json
  models/
dev/
  build-plan.json
  models/
exp/
  build-plan.json
  models/
test/
  build-plan.json
  models/
```

Ordinary PR/work-branch builds are verification-only. A PR that explicitly
requests `output.scope: test` publishes a fresh rolling `test/` scope by
copying the current durable `dev/` catalog and overlaying its selected
candidate model outputs. Incremental `dev` and `exp` publication replace only
selected model directories, preserve unselected active models, and remove model
directories that are no longer active. A full `main` build replaces the
complete `main/` scope.

Publication uses normal non-force pushes and checks that the source branch still
points at the source SHA being published.

Forge v0.17.0 drawing artifacts follow the same ownership boundary. Forge
compiles drawing intent and declares safe relative PDF artifacts in
`solidcraft.json`; the CAD build module projects those declarations into the
build plan, then the pinned SolidCraft runtime exports the vector PDF from the
saved native `.sc` design. Pages reads only the resulting durable build-plan
rows and never runs drawing export itself. A4 is Forge's default part sheet;
models may explicitly request `iso-a3-part` when a larger sheet is needed.

## Pages

Stable Pages use Hugo 0.169.0 with Hextra v0.13.0.

The site consumes source metadata and reads durable build metadata without
rebuilding CAD. Generated CAD artifacts remain owned exclusively by the
generated `build` branch; Pages never republishes those files into
`gh-pages`.

One Pages deployment contains the permanent presentations plus the current
rolling review when present:

```text
/        <- main source + build/main
/dev/    <- dev source  + build/dev
/exp/    <- exp source   + build/exp
/test/   <- exact source SHA recorded by build/test + build/test
```

Both scopes use the same Hugo/Hextra layouts. Each scope is verified against
its matching build plan before the combined generated site is published.

`model.yml` owns presentation text. `ci.yml` owns source/variant identity.
The generated `build/main` / `build/dev` / `build/exp` / `build/test`
scopes own JSON, SC, STEP, PNG,
optional STL, model-owned snapshot images and native drawing PDFs declared by
Forge.

Model pages link directly to those durable artifacts:

- normal GitHub `blob/build/<scope>/...` URLs for inspection and downloads;
- raw GitHub build URLs for inline preview images and SolidCraft Web input;
- STL blob URLs open in GitHub's native 3D viewer;
- native drawing PDFs use the durable build branch for inline sheet preview,
  GitHub inspection and direct download.

Only source-owned presentation resources such as `page.md` and declared local
reference assets are copied into the generated site.

The primary model layout is shared. Model-specific additions use optional
`page.md` for background prose and declarative `extra_views` in metadata for
reference/build images. Extra-view kinds distinguish ownership explicitly:
`url` renders a normal external provenance/reference link, `asset` renders a
source-owned local presentation asset, and `build` renders a durable generated
snapshot. Remote images used visually on a model page must be acquired once,
downscaled to an appropriate review size, stored beside the model source and
referenced through `asset`; the generated page must not depend on a remote
image URL. Do not add model-name branches to shared Hugo templates.

Pages runs in a separate workflow from CAD CI. After a successful permanent
build publishes its build scope, CI sends a `workflow_dispatch` for
`pages.yml` and then finishes. The Pages workflow independently rebuilds the stable root, `/dev/`, optional `/exp/`
and current `/test/` when available, then publishes the complete tree atomically to the
generated `gh-pages` branch.

The explicit dispatch is intentional: GitHub suppresses most chained workflow
events created by `GITHUB_TOKEN`, while `workflow_dispatch` is allowed. CAD
CI never waits for Hugo or Pages deployment.

PRs that change the site or Pages implementation get a separate read-only
Pages check. Development-target PRs and dev-to-main promotions use the durable
`build/dev` scope; other main-target PRs use `build/main`. Model-only changes
are verified by CAD CI and receive their published pages after permanent build
publication. Keep new-model migrations separate from Pages implementation
changes, because unpublished model variants do not have durable build rows.

Repository Pages uses the generated `gh-pages` branch as its publication source.
The workflow itself updates that branch; no `github-pages` deployment environment
or `actions/deploy-pages` path is part of the template contract.
