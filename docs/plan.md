# Repository plan

This file contains unfinished work only.

## Now

### #103 — SamplePlate native A4 drawing PDF and visual sheet evidence

Active on `issue/103-sample-plate-drawing-preview-v3`.

The PDF publication work from PR #108 is accepted on `dev`. Complete the
remaining visual-evidence requirement against Forge v0.18.0 / SolidCraft
0.49.0:

- keep `SamplePlate` as the existing reusable `@component`;
- keep drawing intent only in the final root design;
- retain Forge's default ISO A4 part template and explicit A3 support;
- retain durable native vector
  `models/sample-plate/drawings/SamplePlate.pdf`;
- project the replay-bound native first-sheet id from Forge;
- export that same SolidCraft sheet as
  `models/sample-plate/drawings/SamplePlate.png` at 144 dpi;
- validate both PDF and PNG signatures during the native build;
- render the PNG sheet preview generically on the model page while PDF remains
  the open/download publication artifact;
- link both artifacts from the durable build scope and copy neither into
  `gh-pages`;
- Pages remains compatible with the already-published pre-preview build scope
  until this PR is merged and its new scope is published;
- visually review the generated A4 sheet after CI, then close #103.

### #18 / #19 / #20 — HUB75 detailed follow-up

Current dev baseline includes corrected `hub75_improved_v2` via PR #116.

Accepted v2 source contract:

- middle reinforcement pair: (+mount_x,+11) and (-mount_x,-11);
- locator pins: (+75,+110) and (-75,-110);
- power connector on corrected +X side;
- two HUB75 data connector envelopes unchanged;
- four white orientation marks unchanged;
- outer envelope and mounting centres unchanged.

Open tracking remains under #18 parent with #19/#20 child issues. Any further work
must preserve this v2 asymmetric placement baseline and qualify both
`hub75-panel` and `hub75-screen`.

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

### #90 — native MFT corner insert and subassembly update

Active on `fix/90-corner-insert-notch-arc`.

Process the newly supplied `hoek_assembly.sc` / `hoek_assembly.json` as the
native source for the MFT rail corner subassembly.

Ownership:

- keep `mft-rail-corner-bracket` as the structural reusable component;
- add `mft-rail-corner-insert` as a separate printable component;
- integrate bracket + insert + two `mounting-rail-m8` occurrences in
  `mft-rail-corner-assembly`;
- preserve both supplied native files under the subassembly `reference/`
  directory.

Source-derived corrections:

- bracket walls extend continuously from Z=0 through the 6 mm foot to Z=-33;
- bracket lower outside corner remains the exact R18 quarter sector;
- remove the earlier R22 segmented approximation;
- latest v2 insert uses the revised inner notch, enlarged 17.5 mm clip lips,
  two additional upright C-profile lugs and R0.8 lip-root fillets;
- inner relief uses the opposite semicircle so the notch hollows toward the
  outside corner rather than bulging toward the MFT.
- preserve source assembly placements.

Acceptance:

1. bracket, insert and subassembly all replay on Forge v0.16.0 / SolidCraft
   0.49.0 / runtime v0.3.6;
2. insert is independently printable and publishes an STL;
3. subassembly depends explicitly on rail + bracket + insert;
4. generated views show the insert filling the exposed outer rail corner;
5. both C-openings remain accessible;
6. complete native source files live only with the subassembly owner.


### #92 — fix stale Pages repository identity after rename

Active on `fix/92-pages-repo-rename`.

The live site still renders build/image URLs through the pre-rename
`2026-011-02.cad.solidcraft.NEW` repository name.

Fix:

- canonicalize the Hugo default repository/base URL;
- derive Pages base URLs from the current GitHub repository owner/name;
- pass `github.repository` explicitly into the Pages builder;
- verify rendered artifact URLs against that explicit repository identity;
- lazy-load catalog card images and async-decode image content.

Acceptance:

1. stable and dev Pages output contain no `.solidcraft.NEW` URLs;
2. raw/blob artifact links use `brainboxemb/2026-011-02.cad.solidcraft`;
3. Pages PR verification and publish are green;
4. the live homepage no longer redirects every model image through the old
   repository name.


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
- Forge v0.18.0 / SolidCraft 0.49.0 / runtime v0.3.6 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- Basic / Components / Sub Assemblies / Assemblies taxonomy;
- metadata-driven Display / MFT grouping.
