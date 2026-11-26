# Repository plan

This file contains unfinished work only.

## Now

### #152 — correct Basic Hinge native leaf placement and source pose

Correct the Basic Hinge against the retained authoritative native source rather
than tuning the preview visually.

Source contract:

- use `models/basic/hinge/reference/Hinge Assembly.sc` and
  `Hinge Assembly.json`;
- preserve two independent reusable leaf occurrences;
- each leaf remains a 40 × 30 × 3 mm plate with an Ø8 × 40 mm X-axis knuckle;
- Leaf A remains grounded;
- native joint remains named `Hinge`;
- joint remains revolute with a 60° source value and 0–180° limits.

Required correction:

- derive the exact Leaf B source pose from the retained native transform;
- make the Forge-generated occurrence placement match that pose;
- correct AnchorFrame / clocking / flip semantics rather than adding an
  arbitrary fixed visual rotation;
- keep both knuckle axes coincident and the relationship driveable.

Acceptance is owned by issue #152.

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
