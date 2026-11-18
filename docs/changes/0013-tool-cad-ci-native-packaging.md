# 0013 — Package native results in tool.cad.ci items

Status: implementation

## Goal

Make each model-root tool.cad.ci item a complete technical result before the
CAD build branch and Pages publication are switched to tool.cad.ci.

## Changes

- pin tool.cad.ci v0.2.1;
- keep the existing cheap and native CAD checks authoritative;
- run model-root tool.cad.ci items after native verification;
- add one shared `package` action to `scripts/ci/model_item.py`;
- package verified native files and verification metadata under
  `results/<catalog-slug>/`;
- use current-run native output when available;
- use accepted stable output for an unchanged sibling variant in a shared
  physical model root;
- declare `results` as a directory step output so nested output changes are
  part of tool.cad.ci reuse validation.

Generated command JSON remains under the same item root in
`generated/<catalog-slug>/<language>/solidcraft.json`.

## Boundary

This change does not publish the generic item output to `build` or Pages.
The existing CAD publisher remains authoritative until the next cutover phase.
