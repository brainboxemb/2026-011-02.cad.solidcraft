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
Four 15×15 mm wooden glass retainers now lie **in front of the
plexiglass** at Y=-33..-18, touching its front face. Each end is
**mitred at 45°** against its neighbour. The assembled rectangular frame
has a rounded external corner of **R4**, matching
`CornerBracket.inside_corner_radius`. The side and cross pieces split
the *same* circular contour along the 45° joining line, so the corners
meet without overlapping or leaving a triangular gap. This is expressed
as an editable XZ polygonal contour extruded along Y (not a decorative
post-render rounding). The curved cut uses short straight segments
and still requires a real cutting/fastening test.

The rear board starts at Z=-15 and ends at **Z=362**, so it now
fits **under** the roof instead of crossing it.

The four **shared CornerBracket** instances sit on the OUTSIDE wood
corners (X=±437, Z=-15/377), Y=-13. Unlike an internal-corner position
that would physically intersect the plywood, their 12 mm wings follow
the **outside faces** of the side, top and bottom boards. The 24 mm bracket
width occupies Y=-25..-1 of the wooden cabinet depth; the top wing sits
above the roof, and the vertical wing sits outside the side board. The
four-hole geometry is **defined once** in `components/corner_bracket.py`,
also used by the standalone demo. The native 90° countersinks remain an
approximation of the original flat-bottom recess; real bolt seating,
corner clearances and arm-tip refinements still need physical checking.

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
python -m scpf models/advanced/hub75_wood_frame/scpf/model.py --connect
```

From inside its `scpf/` directory, `python -m scpf model.py --connect`
also works. The `--out` option only generates JSON.

**Remaining design work:** exact bracket and mounting fit, glass
standoffs and seals, electronics installation, ventilation, optional
exploded view. Rear/top native image views are [issue #20](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/20),
and interactive CAD web loading is [issue #21](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/21).
