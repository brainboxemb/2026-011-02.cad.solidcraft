# 0014 — Move CAD build and Pages publication to tool.cad.ci

Status: implementation

## Goal

Make the model-root item output from tool.cad.ci the durable CAD build store and
remove Git publication mechanics from the CAD repository.

## Ownership after this change

CAD still owns:

- model selection and native SolidCraft verification;
- catalog metadata and model-specific checks;
- CAD result-page content and `results.css`;
- the conversion from a complete technical build view to public HTML.

tool.cad.ci owns:

- complete `build/main` manifests;
- sparse `build/pr/<N>` overlays;
- partial main updates;
- overlay resolution;
- safe build-branch publication;
- stable/PR Pages publication;
- closed-PR generated-output cleanup.

## Durable layout

Each physical model root is one build item. Catalog variants remain inside that
item:

```text
build/main/models/components/guide_rail/
  generated/
    guide-rail/
    guide-rail-makita/
  results/
    guide-rail/
    guide-rail-makita/
  checks/
  steps/
  item.json
```

The CAD site keeps its existing public stable URLs under `/models/<slug>/`.
PR previews use the common `/previews/pr-N/` namespace.

## Cutover

Every model-root `ci.yml` changes in this PR, so the first PR/main run produces
a complete local item set. The first stable publication uses
`cad-ci build prepare-main`. Later main runs use `cad-ci build update-main`
and replace only selected item roots.

The old per-model durable layout remains readable only as an input fallback
during the cutover run. It is no longer written by the CAD publisher.
