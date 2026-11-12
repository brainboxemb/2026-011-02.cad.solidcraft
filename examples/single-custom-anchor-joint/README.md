# Single custom-anchor joint

Third diagnostic in the single-joint series.

This example contains exactly one rigid joint. It combines:

- parent: `Anchor.FRONT_TOP_RIGHT` on `Base`;
- child: one named custom `AnchorFrame("mount")`;
- the named custom `AnchorFrame("mount")` is lowered inline into `joint.create`;
- zero persistent native `joint.origin` objects;
- exactly one native `joint.create`.

Run:

```powershell
python -m scpf examples\single-custom-anchor-joint\scpf\model.py --connect --new
```

Turn the **Joints** folder eye back on and select the single joint.

This example originally isolated the visible RGB axes to a persistent
`joint.origin`. Current Forge lowers this unrotated custom frame inline, so
the selected joint should now look like the simpler diagnostics without a
separate red/green/blue origin glyph.
