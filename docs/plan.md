# Repository plan

This file contains unfinished work only.

## Now

### #79 — provisional 180-degree display hinge

Active on `feature/79-display-hinge`.

Create the first buildable hinge component for the wooden HUB75 display
enclosure without changing Forge.

Direction:

- owner: `models/components/display_hinge`;
- presentation: `Components / Display`;
- conventional external 180-degree hinge first;
- two printed PETG leaves with alternating knuckles;
- removable 4 mm metal pin;
- two provisional mounting holes per leaf;
- 36 mm hinge length used only as scale reference from the existing hinge
  concept survey;
- concealed multi-link/spider geometry remains a later variant, not a fake
  approximation in this component.

Acceptance:

1. Forge v0.16.0 compiles the hinge with native Box/Cylinder CSG only;
2. native SolidCraft 0.49.0 replay succeeds on runtime v0.3.6;
3. the two leaves remain distinct around one shared pin with explicit axial
   and radial clearances;
4. Pages publishes the owner under Components / Display;
5. top and barrel-end review views expose mounting holes, knuckle alternation
   and pin clearance;
6. dimensions and fastener choices remain marked provisional until physical
   enclosure fit review;
7. Forge itself is not modified as part of this work.

## Mandatory integration rule

Agents do not choose merge methods themselves.

Every source-branch integration uses a PR conversation comment:

```text
/merge
```

Direct merge API calls, auto-merge and UI/manual merge fallback are forbidden.
If merge-policy fails, repair it rather than bypassing it.

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- cancel-in-progress;
- item-local impact/watch metadata;
- directory-local model build priority;
- explicit physical-model dependency graph for assembly impact;
- local merge-policy owns all source-branch integration and dispatches target CI;
- standalone cleanup removes merged temporary branches;
- direct Forge -> JSON -> one SolidCraft replay batch;
- Forge v0.16.0 / SolidCraft 0.49.0 / runtime v0.3.6 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with optional primary snapshot camera;
- physical model owners may expand into multiple build variants;
- Pages links durable CAD artifacts from `build` and never republishes them;
- Pages publishes stable `/` and development `/dev/` presentation as one generated `gh-pages` tree.
