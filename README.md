# 2026-011-02.cad.solidcraft

CAD projects and native SolidCraft verification. The Python interface/compiler lives in [lib.py.solidcraft](https://github.com/brainboxemb/lib.py.solidcraft), not here.

## Run a model directly in SolidCraft (Windows)

The normal workflow is to send your Python model to the **open SolidCraft
GUI**. You do **not** need to save an intermediate JSON command file.

1. Open SolidCraft and create a **new empty design**.
2. Enable **Preferences → Assistant → Let AI agents connect** in SolidCraft.
3. Open PowerShell in this repository's root (the folder containing
   `bootstrap.ps1` and `models/`).
4. Activate your normal environment and, on first use, initialize the pinned
   SCPF dependency:

```powershell
conda activate brainboxemb-dev-tools
.\bootstrap.ps1
```

You can run the command **from the project root** as below, or directly
from a model's own directory. The pinned SCPF package now resolves shared
`models.components` imports either way. For example, when your PowerShell
prompt is already in `models/hub75-wood-frame/scpf/`:

```powershell
python -m scpf model.py --connect
```

Then choose **one** model to send to the active SolidCraft design:

```powershell
# Wooden frame + five basic HUB75 modules + provisional corner rails
python -m scpf models/hub75-wood-frame/scpf/model.py --connect

# Detailed HUB75 panel, original two-occurrence regression
python -m scpf models/hub75-panel/scpf/model.py --connect

# Five detailed HUB75 panel occurrences
python -m scpf models/hub75-screen/scpf/model.py --connect
```

`--connect` compiles the Python script and sends its native commands through
SolidCraft's authenticated local control channel. It changes the **active
design**, but it **does not** launch SolidCraft, create a new document or
automatically save the design. Save it yourself in SolidCraft. Before running
another model, create a new empty design to avoid mixing geometries.

`bootstrap.ps1` normally needs to run only once per environment or when
the pinned dependency is updated. It uses [vcs2l](https://github.com/ros-infrastructure/vcs2l)
to install the exact SCPF version from [dependencies.repos](dependencies.repos)
into ignored `ext/scpf/`. No Git submodules, manual `PYTHONPATH`, or
manually created `ext/` folder are needed.

### Optional: generate JSON or run headless

`--out` **only generates JSON**; it does not connect to the GUI:

```powershell
python -m scpf models/hub75-wood-frame/scpf/model.py --out output/wood-box.json
```

For a separate native CLI run and generated `.sc` / STEP / measurements
(and optionally a PNG), use:

```powershell
.\scripts\qualify-solidcraft.ps1 -Model models/hub75-wood-frame/scpf/model.py -Snapshot
```

The CLI workflow requires `solidcraft-cli` in PATH or `-CliPath`. It
does **not** connect to the active SolidCraft GUI. If live `--connect`
reports a missing port/token, confirm the GUI is open and the Assistant
connection preference is enabled.

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
