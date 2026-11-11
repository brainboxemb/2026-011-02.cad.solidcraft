# HUB75 Panel — one upright native SolidCraft component

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

This model creates **one Hub75Panel component and one occurrence**, rather than
two copies. Its geometry is authored in local XY with rear depth in local +Z.
The occurrence is rotated **+90° around X** into the upright world **XZ** plane
and placed at **world Z=160 mm**. The front face points toward **world +Y**;
the rear with electronics pockets faces **world −Y**.

SolidCraft 0.30.1 handles the occurrence placement directly using native
`translate`, `axis` and `angle` parameters. SCPF does not calculate its own
rotation matrices. This is important: the later absolute `to` syntax was
silently ignored by SolidCraft 0.30.1, so a syntactically valid JSON did
not previously prove that the panel stood upright.

The [five-panel screen](../../advanced/hub75-screen/README.md) imports the
same [Hub75Panel class](../../../components/hub75.py) but creates four
additional occurrences as a separate assembly model.

The [published model page](https://brainboxemb.github.io/2026-011-02.cad.solidcraft/models/hub75-panel/)
shows independent native **front** and **rear** snapshots when SolidCraft
verification succeeds, including a visible rear electronics-bay layout.

## Open in SolidCraft

With the GUI running, a **new empty design** active, and
**Preferences → Assistant → Let AI agents connect** enabled:

```powershell
python -m scpf models/component-examples/hub75-panel/scpf/model.py --connect
```

This is the default interactive workflow: it creates the editable native
model in the already open design; save it in SolidCraft.

For **optional** command-JSON generation and headless verification:

```powershell
python -m scpf models/component-examples/hub75-panel/scpf/model.py --out output/hub75.json
solidcraft-cli run output/hub75.json --param-check strict --results --save output/hub75.sc
```
