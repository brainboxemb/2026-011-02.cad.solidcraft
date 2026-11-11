# HUB75 Panel — first native SolidCraft assembly experiment

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

Both the two-occurrence regression and the [five-panel screen](../hub75-screen/README.md) import the [shared Hub75Panel model](../components/hub75.py). The assembly builds the model **once**, then creates a second occurrence with
`panel.copy().move(x=160)`. `TwoHub75Panels()` therefore produces one
`Hub75Panel` component definition and two native occurrences at X=0 and
X=160 mm. A native occurrence
has its own position without duplicating the panel's editable geometry.
The gap between physical panel envelopes is **0.30 mm**, as in the
original 160 mm nominal placement grid.

**Current limit:** `copy().move(x=self.pitch_x)` uses a placement value,
not an associative SolidCraft constraint or an editable native design
parameter. The five rotated occurrences are implemented in the [screen model](../hub75-screen/README.md). Detailed front/PCB/connector colors, couplers and exploded views remain open in [CAD issue #7](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/7).

Generate and inspect after running `./bootstrap.ps1`:

```powershell
python -m scpf models/hub75-panel/scpf/model.py --out output/hub75.json
solidcraft-cli run output/hub75.json --param-check strict --results --save output/hub75.sc
```
