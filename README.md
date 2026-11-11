# 2026-011-02.cad.solidcraft

CAD projects and native SolidCraft verification. The Python interface/compiler lives in [lib.py.solidcraft](https://github.com/brainboxemb/lib.py.solidcraft), not here.

## Start on Windows

Activate the shared `brainboxemb-dev-tools` Conda environment, then run from the repository root:

```powershell
.\bootstrap.ps1
python -m scpf models/hub75-panel/scpf/model.py --out output/hub75.json
.\scripts\qualify-solidcraft.ps1 -Model models/hub75-panel/scpf/model.py -Snapshot
```

`bootstrap.ps1` uses [vcs2l](https://github.com/ros-infrastructure/vcs2l) to import the **exact** commit declared in [dependencies.repos](dependencies.repos) into ignored `ext/scpf/`, checks the checkout SHA, and installs the external `scpf` Python package editable into the active environment. No submodule, source copying, manually created `ext/` or `PYTHONPATH` changes are needed.

## Project structure

- `models/<name>/scpf/model.py` — project-owned CAD models and assembly sources.
- `models/<name>/README.md` — model design notes and geometry references.
- `models/<name>/source/` — original SolidCraft command/document references where available.
- `examples/` — small retained API qualification fixtures; reusable API tests live in the library.
- `scripts/ci/` and `site/` — source-matched result pages and checks.
- `.github/workflows/cad-models.yml` — Python package install, command-plan qualification and site smoke tests.
- `.github/workflows/native-cad.yml` — native CLI model qualification, STEP/native documents, screenshots and Pages branch publication.

## Main models

- [Corner Bracket](models/corner-bracket/README.md)
- [HUB75 Panel / two occurrences and four rear bays](models/hub75-panel/README.md)
- [Basic HUB75 Screen / five occurrences](models/hub75-screen/README.md)
- [Wooden Basic Box / simple HUB75 envelopes and prototype corner rails](models/hub75-wood-frame/README.md)
- [Plastic Enclosure Pi](models/plastic-enclosure-pi/README.md)
- [Plate](models/plate/README.md) and [CSG comparison](models/csg-cube/README.md)

## Publication and migration

All ten models are compiled against one pinned SCPF library revision. Nine primary examples have required native geometry and screenshots; the CSG preview is optional if CPU rendering fails. Native-qualified results and a machine-readable `provenance.json` are published from `main` into the `gh-pages` branch. The public website additionally requires GitHub Pages to be configured to serve this branch; a successful branch push alone does not prove that setting.

Legacy library Pages and files must **remain** until the new URL is verified. Migration and cutover tracking: [library issue #25](https://github.com/brainboxemb/lib.py.solidcraft/issues/25). The SCPF version used for qualification is controlled by the exact `dependencies.repos` commit, not the library's moving `main`.

## Build selection and cache planning

Current CI **still recompiles and native-verifies every model** for every PR
and merge to `main`. We will not skip independent model verification or
publish old snapshots without a validated fingerprint. Impact-aware builds,
shared component dependencies, native runtime versions, and a cache-invalidating
SCPF revision pin are specified in [issue #14](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/14).
Moonrepo is an option once individual model rebuild time justifies its setup.
