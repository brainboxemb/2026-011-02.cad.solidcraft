# Hinge source

Source supplied by the project owner on 2026-11-25.

- `Hinge Assembly.json`
  - SolidCraft JSON export
  - size: 3442 bytes
  - SHA-256: `7b1c9e5560893afad1f23a1f79c6a5e4a29971b14b5c92969bd6da0fc272caf0`
  - format: `solidcraft/68`
- `Hinge Assembly.sc`
  - native SolidCraft container supplied together with the JSON export
  - size: 73323 bytes
  - SHA-256: `49fe00844a8468065b0b9922bc8ce4c8f4be99ea37cf820fa54f0552a81006cd`

The native `.sc` container is retained here as the authoritative binary source.
Its committed file matches the supplied 73323-byte source and recorded SHA-256.

## Native geometry

The design contains two reusable components, `Leaf A` and `Leaf B`.

Each leaf contains:

1. one 40 × 30 × 3 mm box starting at component-local origin;
2. one Ø8 × 40 mm cylinder with axis +X and base/axis centre at
   `(0, 33, 4)`.

The two primitive bodies overlap physically near the plate edge. The Forge
consumer model may join them inside one reusable leaf definition, but it must
retain two independent leaf occurrences and the native moving relationship.

## Native assembly relationship

- `Leaf A:1` is grounded;
- `Leaf B:1` is floating;
- native joint name: `Hinge`;
- joint type: `revolute`;
- axis follows the knuckle cylinder (+X);
- source value: 60°;
- limits: 0° .. 180°;
- source clocking direction: `(0, 0, -1)`.

The generated SolidCraft design must keep this as a real native revolute joint,
not as a fixed 60° occurrence rotation.

## Source-pose check

The supplied `Leaf B:1` occurrence transform is:

```text
[-1,  0,        0,       0]
[ 0, -0.5,      0.866025,0]
[ 0,  0.866025, 0.5,     0]
[ 0, 46.035898,-26.578838,1]
```

Using the SolidCraft row-vector convention, that transform maps the child
hinge-axis origin `(0, 33, 4)` exactly back to the parent hinge-axis origin
`(0, 33, 4)`. The source snap clocking direction is `(0, 0, -1)`.

The SCPF `hinge_axis` AnchorFrame therefore uses:

- origin `(0, 33, 4)`;
- local joint Z / rotation axis `(+1, 0, 0)`;
- local joint X / clocking direction `(0, 0, -1)`.

The source transform also fixes the native mating orientation. Its 3 × 3
rotation block is exactly:

```text
R_source = R_x(+60°) · diag(-1, -1, +1)
```

With the joint frame above, `diag(-1, -1, +1)` is a 180° rotation around
the joint-frame X / clocking axis `(0, 0, -1)`. That is SolidCraft's normal
(non-flipped) mating orientation. The public Forge `flip=True` option removes
that 180° mating orientation; using it therefore produces a different Leaf B
pose even though the revolute value is still 60°.

The intended source-pose contract is therefore:

- the shared `hinge_axis` AnchorFrame above;
- native revolute `value=60`;
- native `limits=(0, 180)`;
- **no `flip=True` override**.

No extra fixed occurrence rotation should be added in CAD.
