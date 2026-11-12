# Single corner joint

Diagnostic companion to [single-joint](../single-joint/README.md).

It still contains exactly one rigid joint and no custom `AnchorFrame` objects.
The only important difference is the parent anchor:

```python
parent=Anchor.FRONT_TOP_RIGHT
```

That makes Forge emit SolidCraft's native `edge` + `on` + `corner`
reference for the parent side. The child remains a normal `Anchor.LEFT`
face reference.

Run:

```powershell
python -m scpf examples\single-corner-joint\scpf\model.py --connect --new
```

Turn the **Joints** folder eye back on and select the single joint.

Compare its selected visualization with `examples/single-joint`. If the long
edge/highlight appears only here, it comes from the corner selector rather
than from rigid joints generally.
