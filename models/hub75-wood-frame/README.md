# Wooden HUB75 Basic Box — fast mechanical concept

**Scope:** physical **wooden prototype** with **five simple panel volumes**
and **four external full-depth corner connector concepts**. This is
intentionally separate from the advanced HUB75 model and its rear four-bay
electronics shell.

## Sources and dimensions

The [55th edition Basic Box concept](https://drive.google.com/file/d/1f8JHa2DvL3FM0qgE_fydy4XPOtCT3QLH/view)
records the selected v29 geometry and materials:

| Part | Size (mm) | Material |
| --- | --- | --- |
| Five panel envelopes | 159.70 × 319.71 × 14.50 each | dark, fast BRep box |
| Plexiglass window | 840 × 360 × 4 | plexiglass |
| Free opening | 844 × 362 | clearance around window |
| Two side walls | 15 × 362 × 100 | 15 mm LIGHTPLY |
| Bottom | 874 × 15 × 100 | 15 mm LIGHTPLY |
| Roof | 874 × 15 × 124 | 15 mm LIGHTPLY |
| Rear panel | 874 × 377 × 9 | 9 mm LIGHTPLY |
| Four corner rails | 100 mm long L arms, 6 mm profile thickness, 100 mm depth | **provisional** printed corner connection |

The overall front rectangular outer size is **874 × 392 mm**, while the
visible window opening is 844 × 362 mm. The nominal LED grid remains
**800 × 320 mm**. The 0.30 mm pitch seam is not removed by the simple model.

## Basic versus advanced HUB75

| Basic | Advanced |
| --- | --- |
| `models/components/hub75_basic.py` | `models/components/hub75.py` |
| Single native Box, measured envelope | Native loft, four rear pockets, six blind mounting holes |
| Very few features; assembly layout and enclosure checks | Detailed module interfaces, connector and mounting development |
| Used by this wooden Basic Box | Used by `hub75-panel` and `hub75-screen` regressions |

Both representations are **independent**, but share the same measured
external dimensions. The advanced design remains in use and is not replaced.

## Intentional limits

The wooden outer structure is based on the actual Basic Box concept, not
on the older **840 × 360 aluminium extrusion** prototype.

The four red `CornerRailConcept` occurrences are **visual / envelope
placeholders** showing full-depth external corner coupling. They are not the
final production Corner Bracket geometry, hole locations, structural strength
or fit. Their 100 mm arms follow the earlier 100 mm bracket design intent;
their 6 mm profile wall is a preliminary display dimension. The existing
`corner-bracket` SCPF model remains unchanged and will be reused in the
follow-up once its physical orientation and wood attachments are specified.

The model also deliberately omits the 15 × 15 mm inner support strips,
glass standoffs (5/10/15/20 mm trial spacing), sealing, ventilation,
frame screws, electronics and assembly exploded view. These are the next
mechanical milestones; don't interpret this source as a printable final
design.

## Open directly in SolidCraft

From the CAD repository root (after `./bootstrap.ps1`), start SolidCraft,
open a **new empty design**, and enable **Preferences → Assistant → Let AI
agents connect**. Then:

```powershell
python -m scpf models/hub75-wood-frame/scpf/model.py --connect
```

The model is sent directly to the active design; save the `.sc` file from
SolidCraft. This is the recommended way to inspect the wooden enclosure.

If you specifically need an **intermediate JSON file** or a separate
headless CLI run, use:

```powershell
python -m scpf models/hub75-wood-frame/scpf/model.py --out output/wood-basic-box.json
solidcraft-cli run output/wood-basic-box.json --param-check strict --results --save output/wood-basic-box.sc
```

The initial native build qualifies only the mechanical representation.
A simplified panel is **not** proof of the real PCB or connector fit.
