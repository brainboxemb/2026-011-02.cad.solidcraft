# Bolted Flange

This basic model uses the original SolidCraft flange sample as its dimension
source while expressing the bolt circle as a native CAD relationship.

The dimensions are:

- flange: Ø100 × 10 mm;
- hub: Ø44 × 16 mm above the flange;
- bore: Ø24 mm through the complete 26 mm height;
- bolt circle: six Ø9 mm holes on a 70 mm PCD.

## SCPF

The SCPF model uses:

- one `Cylinder` for the Ø100 flange;
- one face-attached sketch containing a single Ø9 seed circle at `pcd / 2`;
- one through-cut for that seed hole;
- one native `solid.pattern.circular` around the Z axis;
- one joined `Cylinder` for the hub;
- one native `Hole` for the central bore.

`bolts` and `pcd` are lowercase class attributes because they are editable
native CAD parameters. Changing `pcd` moves the seed feature radially; changing
`bolts` changes the native pattern count.

No Python loop calculates repeated bolt coordinates.

## SCPC

The SCPC implementation remains an independent direct-command geometry
reference. It currently expands the six bolt holes explicitly; native
qualification compares the resulting geometry with the SCPF model, not its
history shape.

## Source

The original SolidCraft sample command document is retained unchanged in
`source/flange.json` as a reference for the dimensions and original example.
