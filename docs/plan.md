# Repository plan

This file contains unfinished work only.

## Now

### #31 — adopt Forge v0.15.0 and restore HUB75 component replay

The migrated repository must use the same accepted Forge baseline as the
historical `dev-cad` source:

- Forge v0.15.0;
- commit `efc88bfcaf452051d721347f2e5ca561decad654`;
- SolidCraft 0.48.1 / runtime v0.3.5.

This fixes Forge #753: component context is restored across headless replay
phases so component-local joined Cylinder features remain attached to copied and
rotated HUB75 occurrences.

Acceptance rebuilds `hub75-panel` and `hub75-screen` and compares the
resulting screen preview against the known-correct historical `dev-cad` image.

### #39 — add generic M8 mounting rail component

Active on `feature/mounting-rail-m8`.

Model a 1000 mm galvanized light installation rail under
`models/components/mounting_rail_m8`.

Accepted source split:

- product facts: 1000 mm, galvanized steel, 1.25 mm sheet, M8 application;
- generic 27/18 reference: section and repeating perforation geometry;
- explicit model assumptions: bend radius and K-factor.

Use native sheet metal. Keep the component/model name generic; DRESSELHAUS and
HORNBACH are provenance only.

### #43 — make Mounting Rail M8 perforation one parametric repeat unit

Active on `fix/mounting-rail-m8-repeat-unit`.

Replace the three independent perforation feature patterns with the actual
product design intent:

- one attached four-profile repeat-unit Sketch;
- one through-all unit cut;
- one native rectangular pattern of that complete cut;
- editable `repeat_count`, `feature_pitch` and individual profile dimensions.

No Forge change is required.

### #12 — migrate remaining historical CAD issues and open pull requests

The full CAD catalog is accepted on stable `main`.

Stable baseline:

- source: `128f71fd0bdb85f92752b7e77ff3937157341332`;
- Forge v0.15.0;
- SolidCraft 0.48.1 / runtime v0.3.5;
- 16 real physical owners / 18 real build variants;
- generated CAD artifacts owned only by the `build` branch.

Active transferred model work is tracked in #13 through #22. Generic gallery
and embedded-viewer work is routed to the template project (#84/#85 there).

Next:

1. close or update historical issue copies with explicit pointers;
2. assess the remaining historical open PRs listed in #12;
3. port only relevant model-owned source/data onto the new contracts;
4. integrate every branch exclusively through local `/merge`.

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
- Forge v0.15.0 / SolidCraft 0.48.1 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- compact model `ci.yml` with optional primary snapshot camera;
- physical model owners may expand into multiple build variants;
- Pages links durable CAD artifacts from `build` and never republishes them;
- Pages publishes stable `/` and development `/dev/` presentation as one generated `gh-pages` tree.
