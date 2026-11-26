# Repository plan

This file contains unfinished work only.

## Now

### #125 — add Basic Hinge from supplied native source

Active on `feature/125-basic-hinge`.

Forge v0.19.0 now provides the released native bounded revolute relationship
required by this model.

Source and behavior contract:

- preserve supplied `Hinge Assembly.sc` and `Hinge Assembly.json`;
- keep two independent reusable leaf occurrences;
- each leaf is 40 × 30 × 3 mm with an Ø8 × 40 mm X-axis knuckle;
- Leaf A is grounded;
- native joint name is `Hinge`;
- preserve 60° value and 0–180° limits;
- qualify the model on the released Forge v0.19.0 baseline.

Acceptance is owned by issue #125. Do not replace the native revolute
relationship with fixed occurrence transforms.

### #133 — Wall Hook yellow display appearance

After #125, apply the released Forge v0.19.0 display-only appearance API to the
existing Wall Hook.

Contract:

- use `Shape.with_appearance("#FFD21A")`;
- change presentation only;
- preserve geometry, mounting-hole behavior, STL and engineering semantics;
- verify generated preview/snapshot reflects the yellow appearance.

Acceptance is owned by issue #133.

## Mandatory integration rule

Every source-branch integration uses a PR conversation comment:

```text
/merge
```

Direct merge API calls, auto-merge and UI/manual merge fallback are forbidden.

## Accepted architecture

- work branch selection from matching `build.yml`;
- incremental `dev` CI from the last successful integration baseline;
- full `main` CI;
- Forge v0.19.0 / SolidCraft 0.49.0 / runtime v0.3.6 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- Basic / Components / Sub Assemblies / Assemblies taxonomy;
- metadata-driven Display / MFT grouping.
