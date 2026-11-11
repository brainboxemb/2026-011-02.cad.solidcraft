# Corner Bracket — SCPF

The standalone model imports the **single shared `CornerBracket` shape**
from `components/corner_bracket.py`. The default component is deliberately
**without screw holes**. The earlier countersink operations caused warnings
in native SolidCraft, especially when the same component was used four times
inside the wooden HUB75 frame.

Only the screw-hole features have been removed. The L outline, inside R4
fillet, outer chamfers and elephant-foot reliefs are all still separate,
editable native features.

The original **42-command, hole-containing** exploration is preserved as
`scpf/model_reference.py` for study, but is **not the default model** and is
**not used by the wooden enclosure**. Hole geometry and fixing methods can be
reintroduced later, after they can be built without native warnings.

## Named profile and explicit reliefs

The L outline is defined **once**, in a single `Polygon2D` table of `("name", (x, z))` rows:

```python
profile = Polygon2D([
    ("i_corner", (0, 0)),  # start at the sketch origin
    ("o_hor_tip", (h, 0)),
    ("o_hor_bevel", (h, w - end)),
    # ... the rest of the contour ...
    ("v_tip", (0, -v)),
], plane="XZ", world=True)
```

The name belongs to the **vertex** and becomes the sketch-line ID for the **segment beginning at that vertex**. `world=True` means the XZ coordinates are ordinary world (x, z); SCPF performs SolidCraft's local-sketch axis conversion.

`Edges.from_profile("o_*")` selects named profile segments on the two broad faces. `Edges.from_vertices("o_hor_tip", "v_tip")` instead selects the extrusion-direction edges starting at those vertices. SCPF translates both selectors to edge-pick points because SolidCraft 0.30.1's fillet/chamfer commands do not directly accept sketch-line IDs.

The original 0.6 mm **tip elephant-foot cuts are not in the polygon**: a separate native chamfer removes them at the two tip edges. Another chamfer produces the relief along the inside horizontal edge. The inside fillet, both reliefs and side chamfers remain separate editable features. No mounting holes are created in the default model.

Named-edge selection is currently implemented for **symmetric XZ polygon extrusions only**. The remaining irregularities at the arm tips are a separate follow-up in issue #20.

For local GUI testing from the repository root after `./bootstrap.ps1`:

```powershell
python -m scpf models/component-examples/corner-bracket/scpf/model.py --connect
```

Open an empty SolidCraft document and enable external Assistant control before running. To generate commands without touching the GUI:

```powershell
python -m scpf models/component-examples/corner-bracket/scpf/model.py --out output/corner-bracket.json
```

The uncorrected small pointed corners at the arm ends are tracked separately in [issue #20](https://github.com/brainboxemb/lib.py.solidcraft/issues/20). This issue is intentionally deferred, not a blocker for this initial SCPF model.

Original geometry reference: `brainboxemb/2026-011-01.cad.model-archive`, `models/corner_bracket/v0.1/scad/corner_bracket.scad`.
