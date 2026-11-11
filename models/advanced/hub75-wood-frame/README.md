# Wooden HUB75 Basic Box — advanced assembly

Upright five-module display inside the 874 × 392 mm plywood case. The
**basic** HUB75 boxes model only measured envelopes; the advanced HUB75
reference retains the real four-bay electronics back and six blind M3 bores.
All five simple panel fronts are coplanar, with no misleading rotations.

## Reference, dimensions and parts

Reference: [55th-edition Basic Box v29](https://drive.google.com/file/d/1f8JHa2DvL3FM0qgE_fydy4XPOtCT3QLH/view).

| Part | Dimensions (mm) | Ownership |
| --- | --- | --- |
| 5 HUB75 basic envelopes | 159.70 × 319.71 × 14.50 | `components/hub75_basic.py` |
| Internal opening | 844 × 362 | `scpf/model.py` |
| 2 side walls | 15 × 362 × 100 | `parts/wood.py` |
| Bottom | 874 × 100 × 15 | `parts/wood.py` |
| **Horizontal** roof | 874 × 124 × 15 | `parts/wood.py` |
| Rear board | 874 × 377 × 9 | `parts/wood.py` |
| Plexiglass | 840 × 360 × 4 | `parts/wood.py` |
| 4 mitred, R4 glazing strips | 2 × 15×15×362 and 2 × 844×15×15 (including mitre tips) | `parts/wood.py` |
| 4 corner brackets (no screw holes) | 24 mm extrusion, 12 mm wall, 60 mm arms | `components/corner_bracket.py` |

**Geometry axes:** X is screen width, Y depth (front at negative Y), Z
height/up. Outside plywood spans X=-437..437 and Z=-15..377.
The opening is X=-422..422, Z=0..362. Panels stand from Z=21.145 to
340.855 and have front plane Y=0. Their centre X coordinates are
-320, -160, 0, 160, 320 mm, pitch 160. The five basic rectangles have
identical Y and Z positions; no rotated copies stick out of the frame.

The roof extends in Y from -25 to +99 and in Z from 362 to 377, with
its **15 mm thickness vertical**. The back board is behind the main
100 mm-deep case, at Y=75..84. Plexiglass is at Y=-18..-14.
### The four glazing strips: where they sit and how they meet

The glass is 4 mm thick, from **Y=-18 to -14 mm**. All four
wooden retainers are 15 mm deep in Y, from **Y=-33 to -18 mm**.
Their rear faces therefore meet the front face of the glass,
without extending through it.

The retainers are separate manufactured parts:

| Piece | Position and orientation | Appearance |
| --- | --- | --- |
| Left side | Outer edge X=-422; vertical Z=0..362 | Darker wood `#A9793E` |
| Right side | Mirror of the left at X=+422 | Same darker wood |
| Bottom | Outer edge Z=0; horizontal | Lighter wood `#E3BF80` |
| Top | Mirror of the bottom at Z=362 | Same lighter wood |

The normal plywood frame remains `#CBA36B`. The different
finishes are **visual aids in the CAD model**, not prescribed
timber species or coatings.

**What makes the 45° corners?** Each strip's cross-section has
a diagonal end. The two neighbouring ends meet on the same diagonal.
Neither strip is simply laid over the other. The external corner is
rounded to the same **R4** used for the printed corner bracket's
inside radius. A small series of straight profile segments represents
that arc inside native SolidCraft.

**Why does the mirroring now work?** SCPF creates the second native
occurrence of a strip *before* moving or rotating either occurrence.
Then SolidCraft itself applies the correct 180° orientation and
position. No custom Python rotation matrices or corrective offsets
are used. The right-hand strip flips around Z; the top strip flips
around X. Both remain in the XZ plane.

The native model is verified for distinct parts, correct Y depth,
mirrored X/Z positions, mitred profiles and material assignments.
The final design still needs a physical fit and fastening test.

The rear board starts at Z=-15 and ends at **Z=362**, so it now
fits **under** the roof instead of crossing it.

The four **shared CornerBracket** instances sit on the OUTSIDE wood
corners (X=±437, Z=-15/377), Y=-13. Unlike an internal-corner position
that would physically intersect the plywood, their 12 mm wings follow
the **outside faces** of the side, top and bottom boards. The 24 mm bracket
width occupies Y=-25..-1 of the wooden cabinet depth; the top wing sits
above the roof, and the vertical wing sits outside the side board. The shared bracket geometry is **defined once** in
`components/corner_bracket.py` and used by the standalone demo.
**Screw holes are currently omitted** because an earlier native SolidCraft
attempt produced errors. No countersink geometry is claimed for this
version. Bolt seating, corner clearances and arm-tip fit still need
physical checking.

## Actual SolidCraft model browser groups

```text
WoodenHub75BasicBox
├── HUB75Panels
│   └── Hub75PanelBasic × 5
├── WoodBoxFrame
│   ├── SideWall × 2
│   ├── BottomBoard
│   ├── RoofBoard
│   └── BackBoard
├── WoodGlassFrame
│   ├── GlassSideStrip × 2
│   └── GlassCrossStrip × 2
├── CornerBrackets
│   └── CornerBracket × 4
└── Window (plexiglass)
```

These are **real nested SolidCraft components**: one shared editable
definition per manufactured part, not labels or joined mesh objects.
The case-specific code lives under this model's `parts/` and
`assemblies/`; only generically reusable parts belong to root
`components/`. This advanced design can eventually move to its own repo.

## Load into the native SolidCraft GUI

Open a new, empty SolidCraft design with **Preferences → Assistant →
Let AI agents connect** enabled. After `./bootstrap.ps1` from the repo
root, run:

```powershell
python -m scpf models/advanced/hub75-wood-frame/scpf/model.py --connect
```

From inside its `scpf/` directory, `python -m scpf model.py --connect`
also works. The `--out` option only generates JSON.

**Remaining design work:** exact bracket and mounting fit, glass
standoffs and seals, electronics installation, ventilation, optional
exploded view. Rear/top native image views are [issue #20](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/20),
and interactive CAD web loading is [issue #21](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/21).

## Naming

The CAD directory `hub75-wood-frame` uses kebab-case. Python-only modules live under `scpf/hub75_wood_frame/` and use snake_case; classes use PascalCase. No external PYTHONPATH is needed.
