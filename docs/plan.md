# Repository plan

This file contains unfinished work only.

## Now

### #62 — design MFT mounting-rail corner bracket

Active on `feature/mft-rail-corner-bracket`.

Create a reusable printable 90° bracket for the current
`MountingRailM8` profile and qualify it first in a standalone two-rail
assembly before adding it to the full Simple MFT.

Current prototype contract:

- two perpendicular 75 mm vertical fixing arms;
- each arm follows the existing rail round-hole datums at 12.5 and 62.5 mm;
- Ø8.5 mm M8 clearance through the bracket arms;
- upper and lower triangular gussets stiffen the corner;
- one provisional countersunk screw seat fixes upward into the MFT underside;
- C-openings and rail ends remain unobstructed for slide-in hardware;
- non-rail dimensions remain provisional until physical measurement.

Acceptance:

1. component and two-rail assembly compile on Forge v0.15.0;
2. native SolidCraft 0.48.1 replay succeeds;
3. bracket holes visibly/structurally align with both rails' first two round
   perforations;
4. bracket remains entirely on the inside of the corner;
5. top face is flush with the future worktop underside plane;
6. document the supplied reference images / Etsy listing as inspiration only,
   not dimensional authority.

### #12 — migrate remaining historical CAD issues and open pull requests

The full CAD catalog is accepted on stable `main`.

Current stable baseline:

- main promotion: `6ef14a509b006a3c3657598f2b56824b6aa6d135`;
- Forge v0.15.0;
- SolidCraft 0.48.1 / runtime v0.3.5;
- generated CAD artifacts owned only by the `build` branch.

Continue transferring only relevant model-owned source/data from the historical
repository. Generic CI/build/Pages behavior remains inherited from the template.

Next:

1. close or update historical issue copies with explicit pointers;
2. assess remaining historical open PRs tracked by #12;
3. port only relevant model-owned source/data;
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
