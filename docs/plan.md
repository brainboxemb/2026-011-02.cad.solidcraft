# Repository plan

This file contains unfinished work only.

## Now

### #109 — Benchdog Clamp WIP subassembly

Active on `feature/109-benchdog-clamp-wip`.

Establish a source-faithful WIP baseline from the supplied
`doghole_clamp2.sc/json` before making new design changes.

Current scope:

- final visible T-slide with fixed centre hinge eye;
- mirrored left/right hinge arms;
- low Ø3 hinge pin;
- source-derived 40 mm dummy rail profile;
- straight Ø20 bench-dog reference;
- native feature-83 final Z datum.

Earlier hidden/replaced dog-expansion and compact-fork concepts remain reference
history only.

Acceptance for the first WIP baseline:

1. publish under Sub Assemblies / MFT as `benchdog-clamp`;
2. retain the source JSON and native-source hashes;
3. reconstruct only the source's final visible bodies;
4. qualify this model alone on the feature branch;
5. keep the PR draft/open until visual parity is reviewed.

### #103 — SamplePlate native A4 drawing PDF

Active on `issue/103-sample-plate-drawing-pdf-v2`.

Adopt released Forge v0.17.0 and make SamplePlate the first catalog model with
a durable native technical drawing:

- keep `SamplePlate` as a reusable `@component`;
- add drawing intent only in the final root design;
- use Forge's default ISO A4 part template;
- project Forge drawing declarations into the CAD build plan;
- export the native vector PDF through SolidCraft 0.49.0;
- publish `models/sample-plate/drawings/SamplePlate.pdf` in the durable scope;
- show the drawing generically on the model page without copying it to
  `gh-pages`;
- retain explicit A3 support through
  `template="iso-a3-part"` for future complex models.

### #102 — correct Wall Hook mounting-hole axis

Active on `fix/102-wall-hook-rear-holes`.

Move the two confirmed Ø4.2 screw holes from the 15 mm side/profile faces to
the 6 mm rear mounting spine. Preserve the existing vertical centres and 1 mm
hole-edge chamfers.

Acceptance:

1. both hole axes are perpendicular to the rear mounting wall;
2. holes are centred across the 15 mm hook width;
3. the cut depth is limited to the 6 mm rear spine and does not reach the diagonal web;
4. Wall Hook qualifies and republishes on dev Pages.

### #18 / #19 / #20 — improved native HUB75 panel

Active on `feature/18-hub75-improved-source`.

Use the supplied `hub75_improved.sc` / `hub75_improved.json` for the
remaining detailed panel work: connected rounded/stepped rear bays, tapered
side-wall trimming, two HUB75 data connector envelopes, the approximate power
connector and four white orientation markings. Preserve the existing local
XY/Z reusable-component frame; the native `Paneel rechtop` move is
presentation-only.

Acceptance:

1. `hub75-panel` and `hub75-screen` qualify on the accepted baseline;
2. accepted outer envelope and mounting centres stay unchanged;
3. connector envelopes are separate occurrences in the standalone detailed model;
4. the native JSON reference is retained under the component owner.

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
- Forge v0.16.0 / SolidCraft 0.49.0 / runtime v0.3.6 baseline;
- generated `build` branch with `dev/` and `main/` scopes;
- Basic / Components / Sub Assemblies / Assemblies taxonomy;
- metadata-driven Display / MFT grouping.
