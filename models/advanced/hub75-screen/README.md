# Basic HUB75 Screen — five panel occurrences

[Issue #7](https://github.com/brainboxemb/2026-011-02.cad.solidcraft/issues/7). The component class is maintained in [components/hub75.py](../components/hub75.py), **not duplicated** between the existing two-panel regression and this assembly.

## Layout from the OpenSCAD reference

[project_config.scad](https://github.com/brainboxemb/2026-006-01.cad.HUB75-display-frame/blob/main/v1.2/cad/config/project_config.scad) and [panels_assembly.scad](https://github.com/brainboxemb/2026-006-01.cad.HUB75-display-frame/blob/main/v1.2/cad/assemblies/panels_assembly.scad) define the exact nominal 160 × 320 mm grid, five columns, and rear data-chain input order. The panel component stays physically **159.70 × 319.71 × 14.50 mm**; the 0.30 mm horizontal seam gap is intentional.

| Left-to-right column | Centre X | Rear chain no. | Input | Rotation |
| --- | ---: | ---: | --- | ---: |
| 1 | −320 mm | 5 | Top | 0° |
| 2 | −160 mm | 4 | Bottom | 180° |
| 3 | 0 mm | 3 | Top | 0° |
| 4 | +160 mm | 2 | Bottom | 180° |
| 5 | +320 mm | 1 | Top | 0° |

This is a nominal **800 × 320 mm** panel grid. The detailed component's **native** front plane is XY, depth is Z. In the **assembly**, each occurrence is rotated +90° about world X so its front plane is **XZ** (standing upright), depth is along world Y and the 319.71 mm dimension points up along Z. Alternating panel orientations combine the upright X+90° with a world Y+180° turn as one absolute axis-angle pose (180° about the diagonal [0, 1, -1]), because SCPF does not compose consecutive rotate calls. The centre height is world Z=160 mm (nominal 320 mm panel grid). Column X translations happen last.

The first occurrence is the *middle* panel at X=0; `copy()` adds the other four placements. Every panel has a vertical Z axis; SCPF creates the four native copies at the origin first, then asks SolidCraft to apply each occurrence's position and rotation using its native `translate`, `axis` and `angle` parameters. All five share one component definition/feature history.

**Scope:** this phase now verifies five real placements, rotation, the existing rear loft, **four rear electronics bays with dividing ribs**, six **blind rear-facing mounting bores** (front face stays intact), and one grey housing material. It does **not** yet include rounded/stepped bay corners, rear-tube reinforcement, connector/PCB bodies, brackets or native exploded views. The source's annotations and physical connector roles are documented, not claimed to be displayed in SolidCraft.

## Open in SolidCraft

From the CAD repository root after `./bootstrap.ps1`, with a **new empty
SolidCraft design** and its Assistant connection enabled:

```powershell
python -m scpf models/advanced/hub75-screen/scpf/model.py --connect
```

`--connect` applies the model to the open GUI; save it there. For
**optional** JSON generation or headless native verification:

```powershell
python -m scpf models/advanced/hub75-screen/scpf/model.py --out output/hub75-screen.json
solidcraft-cli run output/hub75-screen.json --param-check strict --results --save output/hub75-screen.sc --out output/hub75-screen.step
```
