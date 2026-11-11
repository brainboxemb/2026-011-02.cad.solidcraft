# 2026-011-02.cad.solidcraft

SolidCraft CAD models, assemblies and native verification. The reusable Python interface and compiler live in [lib.py.solidcraft](https://github.com/brainboxemb/lib.py.solidcraft).

## Getting started (Windows)

Activate the shared `brainboxemb-dev-tools` Conda environment, then:

```powershell
.\bootstrap.ps1
python -m scpf examples/hub75-panel/scpf/model.py --out output/hub75-panel.json
```

The project uses [vcs2l](https://github.com/ros-infrastructure/vcs2l) with an exact commit in `dependencies.repos` to fetch `ext/scpf/`. The `ext/` directory is ignored by Git; **no Git submodule** and no `PYTHONPATH` setup are required. `bootstrap.ps1` installs `ext/scpf/scpf` editable in the active Python environment.

## Structure and migration

- `examples/` — original CAD models and model references, retained at their current paths so website/build scripts continue working during migration.
- `models/` — new project model structure, to be introduced after CI establishes parity.
- `scripts/ci/` — static results site generator and smoke tests.
- `site/` — results website styling.
- `dependencies.repos` — immutable SCPF dependency pin.

First milestone: compile all migrated model command documents and validate the static website **without replacing the old live GitHub Pages site**. Native rendering and publishing are separate acceptance gates. The old site stays available until the new site passes native checks. See [library issue #25](https://github.com/brainboxemb/lib.py.solidcraft/issues/25).

## Project models

- [Corner Bracket](examples/corner-bracket/README.md)
- [HUB75 Panel](examples/hub75-panel/README.md)
- [Plastic Enclosure Pi](examples/plastic-enclosure-pi/README.md)
