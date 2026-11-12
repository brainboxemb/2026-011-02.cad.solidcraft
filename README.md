# 2026-011-02.cad.solidcraft

CAD projects and native SolidCraft verification. The Python libraries live separately: [SCPF Python Forge](https://github.com/brainboxemb/lib.py.solidcraft.forge) for parametrized models and [SCPC Python Commands](https://github.com/brainboxemb/lib.py.solidcraft.cmd) for explicit native commands.

## Two Python scripts for one CAD design

The same design can be expressed in two deliberately different ways:

```text
models/basic/plate/
├── scpf/model.py   # Forge: parametric geometry objects
├── scpc/model.py   # Commands: native SolidCraft API calls
└── README.md
```

The native-command version is **not** compiled from the Forge script.
Both are independently written; SolidCraft executes both, and CI compares
their native geometry and feature history. We start with **Plate** and
**CornerBracket** before converting other models.

```powershell
.\bootstrap.ps1  # installs BOTH pinned Python packages
python -m scpf models/basic/plate/scpf/model.py --out output/plate-forge.json
python -m scpc models/basic/plate/scpc/model.py --out output/plate-commands.json
python -m scpc models/basic/plate/scpc/model.py --connect
```

The last command modifies an *already open* SolidCraft GUI design; open
an empty document first. Only SolidCraft performs CAD operations. SCPC
does not contain any replacement geometry calculations.

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

Then choose **one** model to send to the active SolidCraft design:

```powershell
# Wooden frame + five basic HUB75 modules + shared printed corner brackets
python -m scpf models/advanced/hub75-wood-frame/scpf/model.py --connect

# Detailed HUB75 panel, original two-occurrence regression
python -m scpf models/components/hub75-panel/scpf/model.py --connect

# Five detailed HUB75 panel occurrences
python -m scpf models/advanced/hub75-screen/scpf/model.py --connect
```

`--connect` compiles the Python script and sends its native commands through
SolidCraft's authenticated local control channel. It changes the **active
design**, but it **does not** launch SolidCraft, create a new document or
automatically save the design. Save it yourself in SolidCraft. Before running
another model, create a new empty design to avoid mixing geometries.

### Update the CAD models and both Python libraries

When the CAD repository has new changes (for example a new `HUB75Panels`
component), **update the CAD project first**, then rerun its bootstrap to
install the exact matching Forge and SCPC library revisions:

```powershell
cd C:\Workspace\brainboxemb-github\2026-011-02.cad.solidcraft
conda activate brainboxemb-dev-tools
git pull
.\bootstrap.ps1
```

`git pull` updates the models, the README and
[`dependencies.repos`](dependencies.repos). The bootstrap script compares
the pinned **SCPF commit** with your checkout in `ext/scpf`; it downloads
that revision if necessary and reinstalls the Python package in the
activated Conda environment. You do **not** need to clone the library
separately or run `git pull` inside `ext/scpf`.

Check the pinned Git commits with:

```powershell
git -C ext/scpf rev-parse --short HEAD
git -C ext/scpc rev-parse --short HEAD
```

The result should match the **start** of the full `version:` SHA shown
in `dependencies.repos`. The exact value changes whenever the CAD project
updates its library pin. `bootstrap.ps1` fails safely if you have changed
tracked files in the external SCPF checkout; preserve those changes first.

After updating, open a **new empty SolidCraft document** and run, from the
repository root:

```powershell
python -m scpf models/advanced/hub75-wood-frame/scpf/model.py --connect
```

Alternatively, if you are already in the model's own directory:

```powershell
cd models\hub75-wood-frame\scpf
python -m scpf model.py --connect
```

`--connect` applies the model to the active SolidCraft GUI document; it
does **not** need an intermediate JSON file.

`bootstrap.ps1` normally needs to run only once per environment or when
the pinned dependency is updated. It uses [vcs2l](https://github.com/ros-infrastructure/vcs2l)
to install the exact SCPF and SCPC versions from [dependencies.repos](dependencies.repos)
into ignored `ext/scpf/`. No Git submodules, manual `PYTHONPATH`, or
manually created `ext/` folder are needed.

### Optional: generate JSON or run headless

`--out` **only generates JSON**; it does not connect to the GUI:

```powershell
python -m scpf models/advanced/hub75-wood-frame/scpf/model.py --out output/wood-box.json
```

For a separate native CLI run and generated `.sc` / STEP / measurements
(and optionally a PNG), use:

```powershell
.\scripts\qualify-solidcraft.ps1 -Model models/advanced/hub75-wood-frame/scpf/model.py -Snapshot
```

The CLI workflow requires `solidcraft-cli` in PATH or `-CliPath`. It
does **not** connect to the active SolidCraft GUI. If live `--connect`
reports a missing port/token, confirm the GUI is open and the Assistant
connection preference is enabled.

## Organization

The Models website shows **Basic Models → Components → Advanced Models**.

- `components/`: genuinely reusable geometry, such as
  `CornerBracket`, `Hub75Panel` and `Hub75PanelBasic`.
- `models/basic/`: compact design/test examples for developing SCPF.
- `models/components/`: standalone example wrappers importing
  the shared component definitions; **no duplicate geometry**.
- `models/advanced/`: complete projects with private `parts/` and
  `assemblies/` next to their model script.
- `scripts/ci/model_catalog.py`: canonical source paths and website
  categories for every qualified model.

The API cheatsheet lives only on the
[SCPF library site](https://brainboxemb.github.io/lib.py.solidcraft/cheatsheet/);
the old CAD cheatsheet URL redirects there.

## Project structure

- `models/<category>/<name>/scpf/model.py` — parametric Forge design.\n- `models/<category>/<name>/scpc/model.py` — explicit native command design (where implemented).
- `models/<category>/<name>/README.md` — model design notes and geometry references.
- `models/<category>/<name>/source/` — original SolidCraft command/document references where available.
- `examples/` — small retained API qualification fixtures; reusable API tests live in the library.
- `scripts/ci/` and `site/` — source-matched result pages and checks.
- `.github/workflows/cad-models.yml` — Python package install, command-plan qualification and site smoke tests.
- `.github/workflows/native-cad.yml` — native CLI model qualification, STEP/native documents, screenshots and Pages branch publication.

## Main models

- [Corner Bracket](models/components/corner-bracket/README.md)
- [HUB75 Panel / two occurrences and four rear bays](models/components/hub75-panel/README.md)
- [Basic HUB75 Screen / five occurrences](models/advanced/hub75-screen/README.md)
- [Wooden Basic Box / nested HUB75Panels and prototype corner rails](models/advanced/hub75-wood-frame/README.md)
- [Plastic Enclosure Pi](models/basic/plastic-enclosure-pi/README.md)
- [Plate](models/basic/plate/README.md) and [CSG comparison](models/basic/csg-cube/README.md)

## Publication and migration

All ten existing Forge models use a pinned SCPF revision. The first two parallel native-command models also use a separately pinned SCPC revision. Nine primary examples have required native geometry and screenshots; the CSG preview is optional if CPU rendering fails. Native-qualified results and a machine-readable `provenance.json` are published from `main` into the `gh-pages` branch. The public website additionally requires GitHub Pages to be configured to serve this branch; a successful branch push alone does not prove that setting.

Legacy library Pages and files must **remain** until the new URL is verified. Migration and cutover tracking: [library issue #25](https://github.com/brainboxemb/lib.py.solidcraft/issues/25). The SCPF version used for qualification is controlled by the exact `dependencies.repos` commit, not the library's moving `main`.

## Build selection and cache planning

Current CI **still recompiles and native-verifies every model** for every PR
and merge to `main`. We will not skip independent model verification or
publish old snapshots without a validated fingerprint. Impact-aware builds,
shared component dependencies, native runtime versions, and a cache-invalidating
SCPF revision pin are specified in [issue #14](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/14).
Moonrepo is an option once individual model rebuild time justifies its setup.
