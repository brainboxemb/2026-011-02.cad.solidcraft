# Single custom-anchor joint

Third diagnostic in the single-joint series.

This example contains exactly one rigid joint. It combines:

- parent: `Anchor.FRONT_TOP_RIGHT` on `Base`;
- child: one named custom `AnchorFrame("mount")`;
- exactly one native `joint.origin`;
- exactly one native `joint.create`.

Run:

```powershell
python -m scpf examples\single-custom-anchor-joint\scpf\model.py --connect --new
```

Turn the **Joints** folder eye back on and select the single joint.

If this produces the long/multiple selection lines that do not appear in
`single-joint` or `single-corner-joint`, the custom child joint origin is
the isolated cause.
