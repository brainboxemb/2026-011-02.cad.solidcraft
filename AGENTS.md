# CAD repository instructions

This repository contains product and project CAD models built with SCPF/SCPC.
Forge itself belongs in `brainboxemb/lib.py.solidcraft.forge`; do not work
around a Forge API/compiler problem in a product model.

## Write simply

Use normal engineering language. Use the names that exist in the code and in
SolidCraft. Avoid architecture jargon and invented terms.

## Model naming and scope

- Put reusable physical parts in `models/components/<name>/`.
- Put complete designs and assemblies in `models/advanced/<name>/`.
- Put small standalone examples in `models/basic/<name>/`.
- Prefer generic component names when the geometry represents a generic part.
  Brand names belong in the source/reference documentation when appropriate.
- A component owns its local geometry. The assembly owns placement.
- Lower-case class attributes are editable native CAD parameters.
- UPPER_CASE values are fixed model constants.
- A leading underscore is a Forge/build-time input, not a native parameter.

Do not commit third-party STEP/STL/CAD reference files unless their licence and
project need explicitly require it. Prefer source links and reproduce only the
geometry needed by our own model.

## Change records

For structural library, public-model API, CI/publication or reusable-component
behavior changes, create the GitHub issue and the numbered
`docs/changes/NNNN-short-name.md` record before implementation.

- Use the next four-digit number from `docs/changes/README.md`.
- One record describes one design decision and links its issue.
- Record the problem, decision/contract and verification.
- Update the index in the same change.
- Do not use `CHANGELOG.md` as a substitute for the design/change record.
- Small content-only documentation corrections that do not change a repository
  contract do not need a new numbered record.

## Add a new model

A new model is not complete when only `model.py` exists. Check every item
below before opening or merging the PR.

1. **Source**
   - Add the SCPF source under the correct `models/.../<name>/scpf/model.py`.
   - Add a README when dimensions, source measurements, assumptions or scope
     need explanation.
   - Keep the model small enough to understand from its own source.

2. **Model catalog**
   - Add one record to `scripts/ci/model_catalog.py:MODELS`.
   - Put the source path, section, site metadata, native flags and optional
     component/SCPC metadata in that record.
   - Do not create a second model list elsewhere. The derived source mappings,
     site sections and CI selections come from `MODELS`.

3. **Regression tests**
   - Add a focused test file under `tests/` for the important geometry and
     parameter behaviour.
   - For reusable components, include the class/path in
     `tests/test_cad_models.py:test_reusable_component_sources_own_component_decorator`.
   - Test dimensions and relationships from generated commands; do not merely
     assert that constants exist in the source.

4. **Normal CAD CI**
   - Models are compiled from the central catalog; do not add a slug to the
     workflow YAML.
   - The normal model regression and static-site smoke tests must pass.

5. **Native SolidCraft verification**
   - Set the model's native flags in the central catalog.
   - Put model-specific native evidence checks with that model or in the shared
     native-check runner when the check is genuinely cross-model. Do not add jq
     assertions or model semantics to workflow YAML.
   - Declare saved-design parameter mutations in
     `scripts/ci/native_cases.py`; `run_native_mutations.py` executes them.
   - Prefer checking the actual saved SolidCraft body rather than only generated
     command JSON.
   - Native verification runs inside the single `.github/workflows/cad.yml`
     pipeline; do not add a second user-facing native workflow or another model
     list in YAML.

6. **Results site**
   - Site title, description, parameters, stages and section belong in the
     central model record.
   - Add only presentation-specific artwork to `build-results.py:DIAGRAMS`
     when a schematic fallback is useful.
   - The site builder and smoke tests iterate the central catalog automatically.

7. **Repository model index**
   - Add a concise entry to `models/README.md` when the model is a reusable
     component or an important advanced model.

8. **Finish**
   - Run/inspect both the ordinary CAD CI and native SolidCraft CI.
   - Do not call the model complete while one of those checks is failing.
   - Keep one logical model change in one branch/PR.

## Targeted CI and publication

Build selection, tool versions and publication state are separate concerns.

### Reuse one immutable CAD toolchain image

Normal CAD CI must not reinstall the same heavy toolchain for every model run.

- Build one CAD CI image in a separate image workflow.
- The image contains the fixed runtime/toolchain only: the pinned Python base,
  system libraries, SolidCraft, and the exact SCPF/SCPC revisions selected by
  this repository.
- Repository model source is **not** baked into the image. Model changes must
  not rebuild the toolchain image.
- The normal `cad.yml` workflow pulls the immutable image and runs the
  selected repository source inside it. It does not download SolidCraft, run
  `vcs import`, or reinstall SCPF/SCPC on every run.
- Image identity is content-addressed from the versioned toolchain inputs.
  At minimum that includes the pinned Python image, SolidCraft version,
  `dependencies.repos`, the image Dockerfile and the small image-metadata
  resolver. Do not use a mutable `latest` tag as qualification identity.
- Keep the Python/SolidCraft image metadata in one versioned repository source;
  do not hide version literals only in workflow YAML. SCPF/SCPC revisions remain
  sourced from `dependencies.repos`; do not duplicate those commit pins.
- Build/publish the image only when one of those toolchain inputs changes.
- Smoke-test a newly built image before publishing it: check Python,
  SolidCraft, SCPF and SCPC versions/imports and run one small representative
  CAD compile/native operation.
- Record the immutable image reference/digest in each model's
  `verification.json` together with the exact SCPF, SCPC and SolidCraft
  versions used.
- A new Forge/SolidCraft pin may require a new image, but it still does **not**
  select the whole model catalog. Model selection and toolchain selection are
  independent. Use explicit `all` mode only when the complete library is
  deliberately being qualified.

### Select only the models that need work

- Normal model work uses targeted builds. A change to one model should compile,
  test and native-build that model only.
- Model selection comes from the central catalog and the shared selector under
  `scripts/ci/`; do not reimplement path filtering in workflow YAML.
- Shared component dependencies must be declared in the catalog so a component
  change selects its actual dependants.
- Adding a new model should normally build only that model.
- Changing `dependencies.repos` or the configured SolidCraft version does not
  automatically mean "build the whole catalog".
- Use an explicit full-build mode when deliberately testing every model against
  a new Forge revision/release or SolidCraft version.
- Keep explicit modes for changed models, named model(s), and all models.

### Keep build output separate from Pages

Use `build` as the durable store of verified model build results.
The build item path is the catalog source-file path without the `.py` suffix.
This makes every item unique and prevents one item directory from being the
parent of another. Do not flatten model output to a slug-only directory.
`gh-pages` is generated publication output, not the source of truth for CAD
verification.

The output branch has two states:

- `pr/<number>/<model-root>/` for branch/PR staging output;
- `main/<model-root>/` for accepted output from a successful `main` build.

Each model output directory contains its own `verification.json` with the CAD
source commit, Forge revision/release, SolidCraft version, workflow run and
native file format that actually produced that model.

The canonical primary native screenshot is `native/model.png`. Legacy
`native/native.png` must be normalized during migration/publication rather
than supported as a second permanent site input. Extra views such as
`front.png` and `rear.png` keep their model-specific names.

Do not describe an unchanged model as verified against a newer Forge,
SolidCraft or CAD revision merely because another model was rebuilt.

### Preview/staging rules

- Every PR/branch writes only to its own preview namespace.
- A preview must never overwrite `build/main/`.
- Build and validate candidate output before publishing the preview.
- Preview Pages are generated from the branch catalog/source, that preview's
  freshly built models and stable output for unchanged models where needed.
- A failed preview build must not replace the previous preview or any stable
  output.
- Preview namespaces may be cleaned up after a PR closes or merges.

### Stable promotion rules

- Only a successful accepted `main` build may update stable model output.
- Build selected models into a temporary/candidate directory first.
- Run all selected-model checks against that candidate.
- Only after every required check is green, replace those selected model
  directories in `build/main/`.
- Preserve every unchanged stable model directory byte-for-byte.
- Regenerate the stable site from the current catalog plus the complete stable
  output set and publish that assembled site to the root of `gh-pages`.
- A failed main build must never partially update stable output or the stable
  Pages root.
- `build` and `gh-pages` may have legitimate concurrent writers, such as
  stable promotion and closed-PR cleanup. Publish with normal non-force pushes;
  on a non-fast-forward, fetch the target branch, rebase the prepared generated
  commit, and retry a bounded number of times. Never force-push generated
  branches or discard the other writer's change.
- Docker CAD output and host publication have different ownership boundaries.
  Stable Pages must be built and tested in a host-owned temporary directory,
  not below the container-owned `output/` tree. Do not repair this with broad
  chmod/chown operations.

### Site/catalog scaling

- Model pages stay at `/models/<slug>/`.
- Generate category pages from the central catalog, for example
  `/models/basic/`, `/models/components/` and `/models/advanced/`.
- The home page is a curated view, not an eventual list of every model.
- Use one catalog flag such as `featured`/`show_on_home`; do not maintain a
  second hand-written home-page list.
- Category pages, home page and navigation may be regenerated cheaply even when
  no model geometry needs rebuilding.

See issue #129 for the current CI/publication implementation work.

## When a model exposes a Forge problem

Do not add a CAD-specific workaround just to get the model green.

1. Confirm the expected behaviour from the current Forge API/docs.
2. Reproduce the problem with the smallest useful Forge unit test.
3. Fix Forge in its own issue/PR.
4. Cover sibling API variants when the same underlying behaviour applies.
5. Merge the Forge fix through its normal CI.
6. Pin the CAD repository to the exact qualified Forge commit when the fix has
   not yet reached a normal release.
7. Re-run the downstream CAD native verification.

A downstream product model is evidence for a Forge bug, not the place where the
Forge bug should be hidden.

## Workflow structure

Expose one normal user-facing workflow:

- `cad.yml` — the complete CAD pipeline: select, cheap checks, native checks,
  candidate build, preview/stable publication and closed-PR cleanup.

Keep `image.yml` separate only because building and caching the immutable CAD
toolchain image is a performance optimization. Do not split normal CAD
operation into separate native, publish or cleanup workflows merely because
those are separate implementation phases.

Workflow YAML owns triggers, permissions, checkout, image pull/login and calls
into tested Python. Git diff logic, model selection, model loops, JSON policy,
model-specific checks, publication decisions and branch mutation policy belong
in tested Python modules under `scripts/ci/` or with the model that owns the
check.

The normal development flow is:

`source change -> build plan -> selected cheap checks -> selected native checks -> candidate output -> publish/promote`

A deliberate full-library run uses the same commands with explicit `all`
selection; it is not a separate CI implementation.

## Git workflow

Prepare the complete logical patch before pushing when practical. Avoid a
separate commit/workflow run for every small file edit. If CI exposes several
related failures, collect them and make one bundled follow-up fix.

Do not mix unrelated model work into an existing PR merely because that branch
is already open.
