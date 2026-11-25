# Repository plan

This file contains unfinished work only.

## Now

### #84 — sheet-metal latch hook

Active on `feature/84-latch-hook`.

Create the matching generic latch hook/keeper from the supplied dimensioned
drawing.

Source constraints:

- 2 mm sheet;
- 20 mm formed projection;
- free hook tip at X=13.5 mm;
- 10.5 mm formed height;
- R2.1 inside bend radius;
- 24 mm mounting width;
- 15 mm hook neck;
- two Ø4.3 mounting holes;
- 14 mm hole pitch;
- 5 mm hole-centre edge datum.

Implementation:

- owner: `models/components/latch_hook`;
- catalog: Components / Display;
- one native flat sheet blank;
- holes before forming;
- one native sheet fold for the hook;
- no fused-solid approximation.

Derived bend geometry:

- outside bend radius = 4.1 mm;
- fold centreline X ≈ 15.9 mm;
- bend angle ≈ 147.414°;
- flat blank extends to ≈ 25.10 mm before forming.

Acceptance:

1. Forge v0.16.0 compiles the native sheet history;
2. SolidCraft 0.49.0 replays it on runtime v0.3.6;
3. side view matches the supplied hook direction and approximate 20 / 13.5 /
   10.5 envelope;
4. top view retains 24 mm overall width, 15 mm neck and two Ø4.3 holes on
   14 mm pitch;
5. Pages publishes it as Latch Hook under Components / Display;
6. no Forge changes are introduced.

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
