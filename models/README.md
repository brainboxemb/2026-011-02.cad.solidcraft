# SolidCraft model catalog

The source is organized by the **purpose of the code**, not by a
perceived level of geometric complexity.

## Basic Models — SCPF tooling and tests

- [Plate](basic/plate/README.md), [CsgCube](basic/csg-cube/README.md)
- [Bracket](basic/bracket/README.md), [SamplePlate](basic/sample-plate/scpf/model.py)
- [Plastic Enclosure](basic/plastic-enclosure/README.md),
  [Plastic Enclosure Pi](basic/plastic-enclosure-pi/README.md)

## Components — reusable physical geometry

- [CornerBracket](../components/corner_bracket.py) has **one** shape
  definition, reused by the
  [standalone example](components/corner-bracket/README.md)
  and the wooden display.
- [Hub75Panel](../components/hub75.py) is the detailed panel with
  rear electronics bays; [Hub75PanelBasic](../components/hub75_basic.py)
  is the faster envelope.

These live in top-level `components/`. The standalone demonstration
scripts in `models/components/` import the corresponding
component and never reimplement its sketch or features.

## Parallel Python interfaces — Forge and native Commands

The **same model** can have an independent script for each interface:

```text
models/basic/plate/
  scpf/model.py   — parametric Forge objects
  scpc/model.py   — direct SolidCraft command calls
```

The first parallel models are [Plate](basic/plate/README.md) and
[CornerBracket](components/corner-bracket/README.md).
They are compiled from distinct sources and compared using the native
SolidCraft engine. **SCPC does not reuse SCPF-generated JSON.**

The libraries are [SCPF Forge](https://github.com/brainboxemb/lib.py.solidcraft.forge)
and [SCPC Commands](https://github.com/brainboxemb/lib.py.solidcraft.cmd).
The model site publishes both source scripts and their command plans.
The second route is intentionally low-level and exposes SolidCraft's
native parameter/edge-selector semantics.

## Advanced Models — designs and assemblies

- [Five-panel screen](advanced/hub75-screen/README.md)
- [Wooden HUB75 Basic Box](advanced/hub75-wood-frame/README.md)

The wooden enclosure keeps its case-specific parts and assembly in **one**
[parameterized `model.py`](advanced/hub75-wood-frame/scpf/model.py).
It uses one `GlassStrip` type for the four differently oriented retainers.
Only the generically reusable HUB75 module and CornerBracket remain in
`components/`. There is no separate `parts/` or `assemblies/` layer.

## Open a verified model with the SolidCraft web application

For every verified design, the model page offers a downloadable native
`.sc` file and a **clearly labelled link to the external SolidCraft
website** (`docs.solidcraft.io`). Clicking that link opens a new tab.
The browser downloads the SolidCraft web application from its own
servers, so the external provider handles that network traffic.
Our GitHub Pages site supplies only the verified model file.

We deliberately do **not** embed SolidCraft on our page. The model
gallery itself never automatically loads the web application.

See [browser links and the option to host SolidCraft ourselves](../docs/browser-viewer.md).
The upstream web application can also be compiled from source and
served as a self-contained static site, but we would test that separately,
with an independent repository and fixed version.

## Running a model

Run `./bootstrap.ps1` after `git pull`. Open an empty design in
SolidCraft and enable **Preferences → Assistant → Let AI agents connect**.

```powershell
python -m scpf models/advanced/hub75-wood-frame/scpf/model.py --connect
```

`--connect` sends native commands to the GUI. `--out output/model.json`
only compiles JSON. See the [root README](../README.md).

## Source conventions

Use plain Python classes, numeric class attributes instead of
`@dataclass` and `: float`, and an explicit `return` from every
`build()`. Root files end in `ModelName()`, no `show()` or `main()`.

## Directory and Python naming convention

- CAD model directories and published URLs use **kebab-case**, e.g. `hub75-wood-frame`.
- When a separate Python module is actually needed, it uses **snake_case**. The current wooden HUB75 design keeps all its case-specific classes directly in one `scpf/model.py`, without a `hub75_wood_frame` package.
- Python classes use **PascalCase**, e.g. `WoodenHub75Box`, `GlassStrip`.
- A CAD directory is not necessarily a Python package. Reusable cross-model components live in root `components/`; model-specific wood parts and their assembly belong together in the wooden model's own `scpf/model.py`.
- Published slugs remain unchanged when internal directories move.
