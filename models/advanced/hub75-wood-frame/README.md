# Wooden HUB75 Basic Box — one parametrized assembly

This model is a wooden enclosure for five upright P5 HUB75 LED modules.
Everything specific to this wooden enclosure is defined in
[`scpf/model.py`](scpf/model.py): the boards, glazing retainers, glass,
assembly and their placements.

Only the general reusable parts — `Hub75PanelBasic` and `CornerBracket` —
come from the top-level `components/` directory. There is no separate
`wood.py` or `wood_frames.py` abstraction to chase through.

**Reference:** [55th-edition Basic Box v29](https://drive.google.com/file/d/1f8JHa2DvL3FM0qgE_fydy4XPOtCT3QLH/view).
These figures reflect the **corrected design choices** below, not necessarily
every older dimension written in the v29 reference.

## Change dimensions in one place

At the bottom of the source, `WoodenHub75Box` has the design parameters:

```python
class WoodenHub75Box:
    opening_width = 844.0
    opening_height = 362.0
    panel_count = 5
    panel_pitch = 160.0

    wood_thickness = 12.0
    back_thickness = 9.0
    cabinet_depth = 100.0
    frame_front_y = -25.0

    roof_front_overhang = 10.0
    roof_rear_overhang = 1.0
    corner_radius = 4.0

    glass_width = 840.0
    glass_height = 360.0
    glass_thickness = 4.0
    glass_bottom_clearance = 1.0
    glazing_width = 15.0
    glazing_depth = 15.0
```

Change these parameters, **not** the placement coordinates of every
separate board. In `build()` the dimensions are derived and passed to the
individual components.

These are **Python model parameters**: change them and regenerate the
SolidCraft model. Do not assume a change to one parameter in an already-open
SolidCraft assembly will automatically reposition every separate occurrence.
Within each individual `GlassStrip`, however, the native sketch uses
**symbolic length and width parameters**, so those are real editable CAD
dimensions, not hardcoded polygon points.

World axes: **X** left/right, **Y** front-to-back (front is negative Y),
**Z** upward. The wood opening spans X=−422..422 and Z=0..362 mm.

## Wood dimensions and the roof overhang

| Part | Size and placement | Notes |
| --- | --- | --- |
| Two sidewalls | **12 × 100 × 362 mm** | Front Y=−25; rear Y=75 |
| Bottom board | **868 × 100 × 12 mm** | Z=−12..0; R4 at outer bottom edges |
| Roof board | **868 × 120 × 12 mm** | Z=362..374; R4 at outer top edges |
| Rear board | **868 × 374 × 9 mm** | Y=75..84, fixed to the rear |
| Plexiglass | **840 × 360 × 4 mm** | Y=−10..−6; Z=1..361 |
| Five basic panels | 159.70 × 319.71 × 14.50 mm | X pitch 160 |
| Four glass retainers | Two lengths: **844** and **362 mm** | 15 mm wide/deep, straight mitres |
| Eight corner brackets | 24 mm Y width, 12 mm wall | Two per corner, no screw holes |

**Roof front:** the sidewall front is at Y=−25, while the roof starts at
Y=−35. That is a **10 mm front overhang**.

**Roof rear:** the rear sheet ends at Y=84; the roof finishes at Y=85.
That is **1 mm behind the mounted backboard**, *not* 1 mm behind the
sidewalls. The roof depth is therefore 120 mm, centred at Y=25.

The roof and bottom board are rounded at their **outside X/Z corners**
with a native SolidCraft **R4 fillet**. This creates the clearance for
the rounded inside corners of the printed brackets.

## One GlassStrip class, four pieces

The wooden retaining frame has only **one Python type**:

```python
class GlassStrip:
    length = 844.0
    width = 15.0
    depth = 15.0
    finish = 0
```

It defines a long strip with **straight 45° cuts at both ends**.
The assembly creates two length variants from the same class:

- **Horizontal:** length 844 mm, lighter wood finish; two occurrences
  at Z=0 and Z=362. The top copy turns 180° about X.
- **Vertical:** length 362 mm, darker wood finish; two occurrences
  at X=−422 and X=422. The left and right copies turn +90° and −90°
  about Y to stand upright.

They are four individual manufactured parts in SolidCraft, not
four different Python classes. The two lengths require two native
component definitions, each shared by its pair of occurrences.

**Do not round the glass retaining strips.** Their ends are mitred,
not filleted. The R4 rounding belongs to the **roof and bottom boards**.

The retaining strips begin at **Y=−25**, aligned flush with the
sidewalls. They are 15 mm deep and end at Y=−10. The glass touches their
rear faces and occupies Y=−10..−6. The glass and its retainers therefore
stay within the box's front plane, rather than sticking out.

## Eight printed corner brackets

Every outside X/Z corner has **two CornerBracket occurrences**:

- Four at the front, in the Y=−25..−1 band.
- Four at the rear, in the **Y=51..75** band, entirely on the sidewalls.

The four X/Z corner positions are **X=±434** and **Z=−12 or 374 mm**.
All eight reuse the **same shared CornerBracket component** with
its existing R4 inside fillet. At the rear, the bracket's back edge is
flush with the **rear face of the sidewall (Y=75)**. The 9 mm backboard
starts there and occupies Y=75..84, so no corner bracket overlaps it.
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
│   ├── SideWall × 2
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

All seven wooden-case Python classes are located in the model's own
`scpf/model.py`. The generic imported panel and bracket are located in
`components/hub75_basic.py` and `components/corner_bracket.py`.
This structure keeps the full model readable in one place.

## Test locally

After `./bootstrap.ps1` and `git pull`, open a blank design in
SolidCraft 0.30.1 and enable **Preferences → Assistant →
Let AI agents connect**:

```powershell
python -m scpf models/advanced/hub75-wood-frame/scpf/model.py --connect
```

To inspect only the generated command JSON:

```powershell
python -m scpf models/advanced/hub75-wood-frame/scpf/model.py --out output/wood-frame.json
```

The native CI separately checks that SolidCraft can evaluate the assembly.
Passing Python tests alone is insufficient evidence of correct physical fit.
