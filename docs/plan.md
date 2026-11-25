# Repository plan

This file contains unfinished work only.

## Now

### #84 — replace inferred hook geometry with native source

Active on `fix/84-use-native-hook-source`.

Use the newly supplied `hook.sc` and `hook.json` as the source of truth for
the latch hook instead of continuing to infer missing geometry from the
dimensioned drawing.

Source contract:

- preserve `models/components/latch_hook/reference/hook.sc`;
- preserve `models/components/latch_hook/reference/hook.json`;
- mirror the three native features: sketch -> sheet_base -> sheet_fold;
- use the fixed native blank points/arcs directly;
- use fold X 15.9, 138.7667505744678°, position=start;
- use the native sheet rule: 2 mm, R2.1, K=0.44;
- keep two Ø4.3 holes at (5, ±7).

Important dimension interpretation:

- 15 mm = neck width in top view;
- 20 mm = formed projection in side view.

Acceptance:

1. top view follows the native R5 lobe + tangent-line contour from hook.sc;
2. no inferred second blend arc remains;
3. SCPF fold contract matches the native source exactly;
4. Forge v0.16.0 and SolidCraft 0.49.0 replay green;
5. generated model/top/side views visually match the native hook thumbnail;
6. Pages continues to publish Latch Hook under Components / Display;
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
