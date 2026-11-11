# CAD model catalog

Every model below is owned by this CAD repository, not by `lib.py.solidcraft`. Run `./bootstrap.ps1` once to install the pinned SCPF package.

| Model | Purpose |
| --- | --- |
| [corner-bracket](corner-bracket/README.md) | L-shaped plywood bracket, native fillets/chamfers/countersinks |
| [hub75-panel](hub75-panel/README.md) | Measured P5 panel with native loft and two component occurrences |
| [hub75-screen](hub75-screen/README.md) | Five native panel occurrences, alternating rotations |
| [plastic-enclosure-pi](plastic-enclosure-pi/README.md) | Raspberry Pi enclosure with shell, ports and vents |
| [plastic-enclosure](plastic-enclosure/README.md) | Shell, lip, snap, bosses and rest |
| [sample-plate](sample-plate/scpf/model.py) | Four-sketch native history (Base/Holes/Boss/Bore) |
| [plate](plate/README.md) | Rounded plate and mounting holes |
| [bracket](bracket/README.md) | L extrusion and holes |
| [csg-cube](csg-cube/README.md) | CSG reference and cross-CAD comparison |

A model generates native command JSON using `python -m scpf models/<slug>/scpf/model.py --out output/<slug>.json`. See `scripts/qualify-solidcraft.ps1` for native SolidCraft CLI execution.
