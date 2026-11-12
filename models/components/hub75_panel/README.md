# HUB75 Panel — one shared native SolidCraft component

## Source shown on the model website

The website shows the **real shared component source first**, not just the
short model entry script. The complete editable profile, extrusions and
features are in `models/components/hub75.py`.

`models/components/hub75.py` is both the reusable definition and the standalone
SCPF model. Forge runs it directly because it contains exactly one public
model class with `build()`. There is no `scpf/model.py` launcher, no
standalone wrapper class and no alternate geometry path. The five-panel screen
imports that exact class and is solely responsible for rotating/placing
occurrences.

Source of measured geometry: `brainboxemb/2026-006-01.cad.HUB75-display-frame`,
`v1.2/cad/components/hub75_panel.scad` (portrait 64×32 P5 panel).

This first SCPF model is **not** an exact reproduction of the panel.
It contains the measured front envelope **159.70 × 319.71 mm**,
a **14.50 mm** depth, and six **rear-side blind Ø3 mm** mounting-hole centres:
**X=±72 mm**, **Y=-152/0/+152 mm**. It uses one grey housing material.
The STEP-derived housing has a **continuous taper**: its outer perimeter
insets by **1.25 mm per side** from **Z=2.00 mm** (the start of the
rear housing) to **Z=14.50 mm**. SCPF describes this with a straight
front extrusion, two rectangle sketches and a **native SolidCraft loft**
joined to the front. These are editable features, not a short edge chamfer.
The holes start at the rear mounting plane (**Z=14.50 mm**) and stop at
the rear-housing start (**Z=2.00 mm**). The nominal **12.50 mm blind bore**
therefore does **not** pierce the front mask / PCB stack. The original
OpenSCAD reference builds its mounting tubes and front layers separately;
our simplified one-body envelope uses a blind cut as the closest supported
native feature until that rear structure is modelled. The six coordinates
remain available for locating brackets and other mounting parts.
## Four rear electronics bays (first rear-frame milestone)

The tapered rear housing now contains **four editable pockets** cut in one
named sketch (`Rear electronics bays`). From the actual rear mounting face
Z=14.50 mm, a negative 12.50 mm cut stops at Z=2.00 mm, so it **never
pierces the LED/front PCB stack**. The original six mounting bores remain
on the two side rails and the three crossbar positions.

The rear web layout is derived from
[the v1.2 OpenSCAD reference](https://github.com/brainboxemb/2026-006-01.cad.HUB75-display-frame/blob/main/v1.2/cad/components/hub75_panel.scad):

- Side rails **12.50 mm** in 160 mm reference-space width.
- Top/bottom end rails **10.75 mm** in 320 mm reference-space height.
- Three dividing ribs **20.00 mm** wide at height 80/160/240 mm.
- Physical scaling uses measured 159.70 × 319.71 mm, without stretching
  the placement grid (which stays at nominal 160 × 320 mm).

**Current approximation:** the four pockets have square corners, whereas
the measured STEP/OpenSCAD model has **R5 rounded opening corners**, local
45°/3 mm rail steps, a shallow 0.8 mm rear recess, circular mounting tubes,
additional reinforcement bushings and two locator pins. This milestone
deliberately avoids misrepresenting those as finished geometry. The PCB,
power/IDC connector volumes, front mask and distinct colors still need
their own editable SolidCraft bodies/features; they are not present yet.

SCPF uses X for width, Y for height and Z for depth (front at Z=0).
The source OpenSCAD model used X/Z for the front and Y for depth.

## One physical panel, one reusable component

The standalone model now executes the shared `Hub75Panel` class **directly**.
Its local component axes are therefore visible without any presentation
transform:

- X = physical panel width (159.70 mm)
- Y = physical panel height (319.71 mm)
- Z = rear depth (14.50 mm), with the front at Z=0

This is intentional CAD behavior: a reusable part owns geometry in its local
coordinate system; an assembly owns placement. The standalone entry point does
not rotate the part merely to make it look like the assembled screen.

The [five-panel screen](../../advanced/hub75-screen/README.md) imports the
same [Hub75Panel class](../hub75.py), creates its occurrences,
and rotates them into world XZ. There is no separate "standalone panel"
geometry definition.

The [published model page](https://brainboxemb.github.io/2026-011-02.cad.solidcraft/models/hub75-panel/)
shows independent native **front** and **rear** snapshots of the same local
component when SolidCraft verification succeeds, including the rear electronics-bay layout.

## Open in SolidCraft

With the GUI running, a **new empty design** active, and
**Preferences → Assistant → Let AI agents connect** enabled:

```powershell
python -m scpf models/components/hub75.py --connect
```

This is the default interactive workflow: it creates the editable native
model in the already open design; save it in SolidCraft.

For **optional** command-JSON generation and headless verification:

```powershell
python -m scpf models/components/hub75.py --out output/hub75.json
solidcraft-cli run output/hub75.json --param-check strict --results --save output/hub75.sc
```
