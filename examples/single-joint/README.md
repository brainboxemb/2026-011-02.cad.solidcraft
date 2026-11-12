# Single joint

Minimal SCPF experiment for inspecting one native SolidCraft rigid joint.

The model contains only:

- one `Base` box;
- one `Child` box;
- one face-to-face rigid joint;
- standard `Anchor.RIGHT` and `Anchor.LEFT` references.

There are deliberately **no** custom `AnchorFrame` objects, corner/edge
anchors, copies, groups or extra occurrence placement.

## Run

From the repository root, after `./bootstrap.ps1`:

```powershell
python -m scpf examples\single-joint\scpf\model.py --connect --new
```

Forge hides the Joints folder after compiling an assembly. Turn the **Joints**
folder eye back on in the SolidCraft Browser when you want to inspect the one
joint glyph.

Expected generated assembly commands:

- exactly one `joint.create`;
- zero `joint.origin`;
- the joint references the right face of `Base:1` and left face of
  `Child:1` directly.

This is the baseline for comparing the visualization with the HUB75
corner-bracket joints.
