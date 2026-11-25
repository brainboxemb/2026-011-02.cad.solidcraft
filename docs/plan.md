# Repository plan

This file contains unfinished work only.

## Now

### #84 — refine latch-hook outline

Active on `fix/84-smooth-latch-hook-contour`.

Refine the already accepted native sheet-metal latch hook after visual review
against the supplied drawing.

Corrections:

- replace the sharp straight 24 mm lobe -> 15 mm neck transitions with smooth
  circular blends;
- retain R5 mounting lobes implied by the dimensioned 24 mm width, 14 mm hole
  pitch and 5 mm edge datum;
- keep a short straight 15 mm neck before the formed hook;
- derive the side projection exactly from the supplied 20 mm projection,
  13.5 mm free-tip X, 10.5 mm height, 2 mm sheet and R2.1 inner radius.

Derived side values:

- outside radius: 4.1 mm;
- fold X: 15.9 mm;
- outside tangent point: (18.108, 7.555) mm;
- straight returned lip: 5.469 mm;
- bend angle: 147.414°;
- flat blank end X: 25.100 mm at K=0.40.

Acceptance:

1. top view has no sharp corner between the mounting lobes and neck;
2. both upper and lower transitions are tangent circular blends;
3. neck remains 15 mm wide and mounting envelope remains 24 mm;
4. two Ø4.3 holes remain on 14 mm pitch with 5 mm edge datum;
5. side view retains the dimensioned 20 / 13.5 / 10.5 / R2.1 formed geometry;
6. native Forge v0.16.0 / SolidCraft 0.49.0 replay remains green;
7. no Forge changes are introduced.

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
- Forge v0.16.0 / SolidCraft 0.49.0 / runtime v0.3.6 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- Basic / Components / Sub Assemblies / Assemblies taxonomy;
- metadata-driven Display / MFT grouping.
