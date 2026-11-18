# 0007 — Parallel HUB75Display2 model

Issue: #142

## Problem

The existing wooden HUB75 display is now a useful, verified design, but the next
iteration is expected to change substantially. Continuing that work directly in
`hub75_wood_frame` would make it difficult to preserve a stable first design
while experimenting with the second one.

## Decision

Add a separate advanced model:

`models/advanced/hub75-display2/`

with top-level class:

`HUB75Display2`.

The first revision intentionally starts from the current
`hub75_wood_frame` geometry and parameter set so v1 and v2 have a known
comparison baseline.

HUB75Display2 owns its own model-local parts and assemblies. It must not import
v1 model-local modules because that would couple later changes between the two
designs.

Reusable physical components remain shared from `models/components/`.
In particular, both designs may continue to use the same HUB75 panel and
CornerBracket components.

## Repository and CI contract

- `hub75_wood_frame` remains unchanged.
- `hub75-display2` gets a separate catalog entry and results page.
- v2 gets its own README, check.py and focused regression tests.
- Default v2 geometry is initially expected to match the verified v1 baseline.
- Later v2 changes are allowed to diverge without changing v1.
- Adding or changing v2 must select/build v2 through the normal central catalog
  and targeted CAD pipeline; no workflow-local model list is added.

## Verification

The initial v2 baseline is accepted when:

1. ordinary model regression/static-site checks pass;
2. native SolidCraft evaluation passes;
3. the saved body/assembly geometry matches the current v1 default dimensions
   and placements at the point this record is introduced;
4. the existing v1 source and stable output are unchanged.
