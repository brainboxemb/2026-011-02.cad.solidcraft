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
   - Add a native BRep measurement check when the model has known physical
     dimensions. Prefer checking the actual saved SolidCraft body rather than
     only generated command JSON.
   - Do not add another model list to the workflow.

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

## Git workflow

Prepare the complete logical patch before pushing when practical. Avoid a
separate commit/workflow run for every small file edit. If CI exposes several
related failures, collect them and make one bundled follow-up fix.

Do not mix unrelated model work into an existing PR merely because that branch
is already open.
