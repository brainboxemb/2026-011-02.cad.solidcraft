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
   - Keep `.github/workflows/native.yml` as orchestration only and do not add
     another model list there.

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
- Normal `cad.yml` and `native.yml` jobs pull the immutable image and run the
  selected repository source inside it. They do not download SolidCraft, run
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

Use `model-output` as the durable store of verified model build results.
`gh-pages` is generated publication output, not the source of truth for CAD
verification.

The output branch has two states:

- `previews/<preview-key>/models/<slug>/` for branch/PR staging output;
- `stable/models/<slug>/` for accepted output from a successful `main` build.

Each model output directory contains its own `verification.json` with the CAD
source commit, Forge revision/release, SolidCraft version, workflow run and
native file format that actually produced that model.

Do not describe an unchanged model as verified against a newer Forge,
SolidCraft or CAD revision merely because another model was rebuilt.

### Preview/staging rules

- Every PR/branch writes only to its own preview namespace.
- A preview must never overwrite `model-output/stable/`.
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
  directories in `model-output/stable/models/`.
- Preserve every unchanged stable model directory byte-for-byte.
- Regenerate the stable site from the current catalog plus the complete stable
  output set and publish that assembled site to the root of `gh-pages`.
- A failed main build must never partially update stable output or the stable
  Pages root.

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

Keep the caller workflows small and purpose-based:

- `image.yml` — build/smoke/publish the immutable CAD toolchain image;
- `cad.yml` — cheap model/unit/site checks for the selected scope;
- `native.yml` — selected native SolidCraft verification using the same image;
- `publish.yml` — trusted promotion to `model-output` and Pages;
- `pr-cleanup.yml` — remove closed PR preview namespaces.

Workflow YAML owns triggers, permissions, checkout, image pull/login, artifact
handoff and calls into tested Python. Git diff logic, model selection, model
loops, JSON policy, model-specific checks, publication decisions and branch
mutation policy belong in tested Python modules under `scripts/ci/` or with the
model that owns the check.

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
