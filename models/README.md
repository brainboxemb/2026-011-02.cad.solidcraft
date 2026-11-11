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
  [standalone example](component-examples/corner-bracket/README.md)
  and the wooden display.
- [Hub75Panel](../components/hub75.py) is the detailed panel with
  rear electronics bays; [Hub75PanelBasic](../components/hub75_basic.py)
  is the faster envelope.

These live in top-level `components/`. The standalone demonstration
scripts in `models/component-examples/` import the corresponding
component and never reimplement its sketch or features.

## Advanced Models — designs and assemblies

- [Five-panel screen](advanced/hub75-screen/README.md)
- [Wooden HUB75 Basic Box](advanced/hub75-wood-frame/README.md)

Parts specific to the wooden case are in its own `parts/` directory,
and combinations (including `WoodBoxFrame`, `WoodGlassFrame` and
`HUB75Panels`) are in its `assemblies/` directory.

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
- Python packages, modules and files use **snake_case**, e.g. `hub75_wood_frame`, `hub75_panels.py`.
- Python classes use **PascalCase**, e.g. `WoodBoxFrame`.
- A CAD directory is not a Python package. Model-local import packages live below `scpf/` and the model script makes that directory importable; no external `PYTHONPATH` is needed.
- Published slugs remain unchanged when internal directories move.
