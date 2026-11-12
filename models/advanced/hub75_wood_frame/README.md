# Wooden HUB75 Basic Box — one parametrized assembly

This model is a wooden enclosure for five upright P5 HUB75 LED modules.
[`scpf/model.py`](scpf/model.py) now contains only the top-level design
parameters and composition. Case-specific geometry is split into
`scpf/parts/`, while each logical subassembly has its own file under
`scpf/assemblies/`.

Only the cross-model parts — `Hub75PanelBasic` and `CornerBracket` —
come from the top-level `components/` directory.

**Reference:** [55th-edition Basic Box v29](https://drive.google.com/file/d/1f8JHa2DvL3FM0qgE_fydy4XPOtCT3QLH/view).
These figures reflect the **corrected design choices** below, not necessarily
every older dimension written in the v29 reference.

## Change dimensions in one place

At the bottom of the source, `WoodenHub75Box` has the design parameters:

```python
class WoodenHub75Box:
    opening_width = 844.0
    opening_height = 362.0
    panel_recess_depth = 25.0

    frame_wood_thickness = 12.0
    panel_wood_thickness = 9.0
    cabinet_depth = 100.0

    roof_front_overhang = 10.0
    roof_rear_overhang = 1.0
    corner_radius = 4.0
    bracket_width = 24.0

    glazing_wood_width = 12.0
    glazing_wood_depth = 12.0
```

Change these values at their owning level, **not** the placement coordinates
of every separate board. This model follows Forge's parameter-intent naming:

- `lower_case` is a native editable SolidCraft model parameter.
- `_lower_case` is a Forge/build-time input. It can be changed when the
  Python model is generated, but is deliberately not shown as a SolidCraft
  parameter.
- `UPPER_CASE` is a fixed design/product constant.

The five-panel layout is fixed here: `HUB75Panels` owns
`PANEL_COUNT = 5` and `PANEL_PITCH = 160.0`. Those values determine the
assembly topology and fixed product grid, so they are constants. In contrast,
`panel_recess_depth` is a genuine native model parameter: the lightweight
panel definition places its XZ sketch on
`y_center = panel_recess_depth + HUB75_PANEL_DEPTH / 2` and extrudes
symmetrically. Changing the recess in SolidCraft therefore moves all five
panel envelopes in depth without rebuilding the Python assembly.

`glazing_wood_depth` remains a native model parameter. The retainers now
extrude directly from the Y=0 front datum instead of being centred and moved
afterwards. The plexiglass receives the semantic front datum
`front_y=glazing_wood_depth` and is built directly from that native sketch
plane. Therefore changing `glazing_wood_depth` in SolidCraft updates both the
retainer depth and the plexiglass Y position without a frozen occurrence
translation.

Fixed product or part dimensions use `UPPER_CASE` constants instead. The
plexiglass sheet is fixed in this design, so `parts/window.py` contains
`GLASS_WIDTH`, `GLASS_HEIGHT` and `GLASS_THICKNESS`; they are deliberately
not editable CAD parameters. Changing `opening_height` does not resize the plexiglass, but
the fixed 360 mm-high sheet stays vertically centred in the opening. The
`Window` itself only receives `opening_bottom_z` and `opening_height`; it does
not know how the wooden frame derives that datum. At the default dimensions it
spans Z=13..373 mm.

Geometry stays symbolic inside the part definitions. In particular
`parts/board.py` uses the internal `_build_board()` function for shared board
geometry. The actual wooden CAD parts remain the semantic component classes
such as `LeftBoard`, `BottomBoard` and `RoofBoard`; there is no generic
`Board` component/class in the model. Reusable component defaults stay internal unless explicitly
published or linked to a parent parameter.

The design therefore has one `corner_radius`: BottomBoard, RoofBoard and
all eight CornerBracket inside fillets reference that same native parameter.
Likewise, one top-level `bracket_width` controls the Y width of all eight
brackets and their front/rear attachment bands. Internal
CornerBracket defaults do not appear as separate `CornerBracket_*`
parameters in the wooden-display design.

The short `pv(...)` helper is only used where Python itself needs a concrete
number for control flow or assembly placement. It is not used to flatten the
board dimensions inside the CAD geometry.

World axes: **X** left/right, **Y** front-to-back, **Z** upward. **Y=0 is the front face of the wooden cabinet** and **Z=0 is its outside bottom face**. `cabinet_depth` grows only towards +Y: the sidewalls and bottom start at Y=0, the rear face is Y=`cabinet_depth`, the back board starts on that same plane, and the rear brackets remain flush with it. The roof is the deliberate exception at the front and starts at Y=`-roof_front_overhang`. The wood opening starts at Z=`frame_wood_thickness` and keeps its own fixed `opening_height`. At the default 12 mm wood thickness the opening spans X=−422..422 and Z=12..374 mm.

The HUB75 modules are recessed **25 mm** from the sidewall front, so their
front faces start at Y=25. `panel_recess_depth` is native and associative:
the panel sketch plane carries the depth datum, so no panel Y occurrence move
is needed.

## Wood dimensions and the roof overhang

| Part | Size and placement | Notes |
| --- | --- | --- |
| `LeftBoard` + `RightBoard` | **12 × 100 × 362 mm** each | Front Y=0; rear Y=100 |
| Bottom board | **868 × 100 × 12 mm** | Z=0..12; R4 at outer bottom edges |
| Roof board | **868 × 120 × 12 mm** | Z=374..386; R4 at outer top edges |
| Rear board | **868 × 374 × 9 mm** | Y=100..109, fixed to the rear |
| Plexiglass | **840 × 360 × 4 mm** | Y=12..16; Z=13..373 |
| Five basic panels | 159.70 × 319.71 × 14.50 mm | X pitch 160 |
| Four glass retainers | Two lengths: **844** and **362 mm** | **12 × 12 mm pine (grenen)**, straight mitres |
| Eight corner brackets | **24 mm Y width** (editable `bracket_width`), 12 mm wall | Two per corner, no screw holes |

**Roof front:** the sidewall front is the Y=0 reference plane, while the roof starts at Y=−10. That is a **10 mm front overhang**.

**Roof rear:** the rear sheet ends at Y=109; the roof finishes at Y=110.
That is **1 mm behind the mounted backboard**, *not* 1 mm behind the
sidewalls. The roof depth is therefore 120 mm, centred at Y=50.

The roof and bottom board are rounded at their **outside X/Z corners**
with a native SolidCraft **R4 fillet**. This creates the clearance for
the rounded inside corners of the printed brackets.

## One GlassStrip class, four pieces

The wooden retaining frame has only **one Python type**:

```python
class GlassStrip:
    length = 844.0
    width = 12.0
    depth = 12.0
    finish = 0
```

It defines a long strip with **straight 45° cuts at both ends**.
The assembly creates two length variants from the same class:

- **Horizontal:** length 844 mm, lighter wood finish; two occurrences
  at the bottom and top of the opening (Z=12 and Z=374 by default). The top
  copy turns 180° about X.
- **Vertical:** length 362 mm, darker wood finish; two occurrences
  at X=−422 and X=422, starting from the same opening-bottom datum. The left
  and right copies turn +90° and −90°
  about Y to stand upright.

The assembly uses Forge's named-axis occurrence syntax, so these placements
read directly as `rotate(X, 180)`, `rotate(Y, 90)` and
`rotate(Y, -90)` instead of raw XYZ axis tuples.

They are four individual manufactured parts in SolidCraft, not
four different Python classes. The two lengths require two native
component definitions, each shared by its pair of occurrences.

**Do not round the glass retaining strips.** Their ends are mitred,
not filleted. The R4 rounding belongs to the **roof and bottom boards**.

The retaining strips are authored directly from **Y=0**, aligned flush with
the sidewalls; no Y occurrence translation is required. They are 12 mm deep
and end at Y=12. The glass touches their
rear faces and occupies Y=12..16. The glass and its retainers therefore
stay within the box's front plane, rather than sticking out.

## Eight printed corner brackets

Every outside X/Z corner has **two CornerBracket occurrences**:

- Four at the front, in the Y=0..24 band.
- Four at the rear, in the **Y=76..100** band, entirely on the sidewalls.

The four X/Z corner positions are **X=±434** and **Z=0 or 386 mm**.
All eight use the same shared `CornerBracket` geometry class. Their X/Z/Y
placement is kept in the native symbolic geometry, so front and rear
placements compile as separate native definitions instead of fixed
occurrence translations. At the rear, the bracket's back edge is
flush with the **rear face of the sidewall (Y=100)**. The 9 mm backboard
starts there and occupies Y=100..109, so no corner bracket overlaps it.
This is independent of the roof's 1 mm overhang *past* the backboard.

The old screw-hole operations are deliberately absent. They had caused
native SolidCraft warnings and should not be silently reintroduced.
Mounting and fastener design remains to be resolved later.

## Model browser and source layout

```text
WoodenHub75Box
├── HUB75Panels
│   └── Hub75PanelBasic × 5
├── WoodBoxFrame
│   ├── LeftBoard\n│   ├── RightBoard
│   ├── BottomBoard
│   ├── RoofBoard
│   └── BackBoard
├── WoodGlassFrame
│   ├── GlassStrip (horizontal, 844 mm) × 2
│   └── GlassStrip 2 (vertical, 362 mm) × 2
├── CornerBrackets
│   └── CornerBracket × 8
└── Window (plexiglass)
```

The source is split by responsibility:

```text
scpf/
├── model.py
├── parts/
│   ├── board.py
│   ├── glass_strip.py
│   └── window.py
└── assemblies/
    ├── hub75_panels.py
    ├── wood_frame.py
    ├── glass_frame.py
    └── corner_brackets.py
```

`parts/board.py` contains the internal `_build_board()` geometry function
plus the semantic wooden part classes. Parts use `@component`; subassemblies use
`@assembly`. That lets the top-level model compose them directly as
`Window()`, `WoodFrame()`, `GlassFrame()`, `HUB75Panels()` and
`CornerBrackets()`, without procedural `build_*` wrappers. The generic
imported panel and bracket remain in `components/hub75_basic.py` and
`components/corner_bracket.py`.

## Test locally

After `./bootstrap.ps1` and `git pull`, open SolidCraft 0.30.1 and
enable **Preferences → Assistant → Let AI agents connect**:

```powershell
python -m scpf models/advanced/hub75-wood-frame/scpf/model.py --connect --new
```

`--new` replaces the active design with a clean empty design before the
model batch is sent. Leave it off only when you intentionally want to build
into the current design.

To inspect only the generated command JSON:

```powershell
python -m scpf models/advanced/hub75-wood-frame/scpf/model.py --out output/wood-frame.json
```

The native CI separately checks that SolidCraft can evaluate the assembly.
Passing Python tests alone is insufficient evidence of correct physical fit.
