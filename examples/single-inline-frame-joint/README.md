# Single inline-frame joint

This is the control experiment for the visible red/green/blue axes produced by
a named custom `joint.origin`.

Unlike the SCPF `single-custom-anchor-joint` example, this script sends the
child frame directly in `joint.create`:

```text
b = {
  occurrence: Child:1,
  point: [40, -20, 80],
  z: [0, 1, 0],
  x: [1, 0, 0]
}
```

There is **no** `joint.origin` command.

## Run

First open a new empty design in SolidCraft, then from the repository root:

```powershell
git pull
.\bootstrap.ps1
python -m scpc examples\single-inline-frame-joint\scpc\model.py --connect
```

Select the single joint in SolidCraft.

Expected diagnostic result: if the separate red/green/blue origin axes are
gone and the selected joint looks like the simple single-joint examples, the
correct Forge fix is to lower named `AnchorFrame` references inline into
`joint.create` instead of creating persistent native `joint.origin`
objects.
