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

This is a nominal **800 × 320 mm** panel grid. The SCPF panel front plane is **XY**, depth is **Z**; OpenSCAD's `rotate([0,180,0])` about its Y depth axis becomes SolidCraft's native occurrence rotation about **Z**.

The first occurrence is the *middle* panel at X=0; `copy()` adds the other four placements. The two alternating rotations are native absolute `occurrence.move` placements. All five share one component definition/feature history.

**Scope:** this phase now verifies five real placements, rotation, the existing rear loft, **four rear electronics bays with dividing ribs**, six **blind rear-facing mounting bores** (front face stays intact), and one grey housing material. It does **not** yet include rounded/stepped bay corners, rear-tube reinforcement, connector/PCB bodies, brackets or native exploded views. The source's annotations and physical connector roles are documented, not claimed to be displayed in SolidCraft.

## Build

From the repository root, after `./bootstrap.ps1`:

```powershell
python -m scpf models/hub75-screen/scpf/model.py --out output/hub75-screen.json
solidcraft-cli run output/hub75-screen.json --param-check strict --results --save output/hub75-screen.sc --out output/hub75-screen.step
```
