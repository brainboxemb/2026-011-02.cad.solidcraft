# 0041 — HUB75 tube-clamp Installed state as one suppressable history step

Status: Proposed  
Issue: #281

## Problem

The HUB75 tube clamp is a preloaded elastic part.

For the default Ø10 mm tube with 0.4 mm interference, the printable Free clamp
has a 9.6 mm bore. When that same printed clamp is pushed over the Ø10 mm tube,
the ring opens elastically.

The current catalog does not model that history. It switches `clamp_bore`
between 9.6 mm and 10 mm and therefore rebuilds the ring as two different
nominal geometries.

The earlier #270 attempt moved in the right history direction by introducing one
named `installed` feature, but its geometry was wrong: widening the bore with a
cylindrical cut removes material and thins the clamp. That is machining, not
preload.

This change keeps the **one-step history model** and defines what that step must
actually mean.

## Goal

Free and Installed must be two states of **one physical clamp**.

The intended history is:

1. build the normal Free/print clamp;
2. define exactly one named history feature: `installed`;
3. keep that feature suppressed in the Free state;
4. unsuppress that same feature in the Installed state;
5. the `installed` feature opens/deforms the existing clamp around the target
   tube without removing clamp material.

Conceptually:

```python
body = build_free_clamp(...)

with feature("installed", suppressed=True):
    body = open_clamp_around_tube(
        body,
        tube_d=self.tube_d,
    )
```

The exact deformation operator is implementation detail. The important contract
is that `installed` is **one semantic history step** and that suppression alone
selects Free versus Installed.

## Required Free / Installed behavior

### Free

Free is the manufacturing state.

- `installed` is suppressed;
- no tube is present;
- the clamp is unloaded;
- `clamp_bore = tube_d - clamp_interference`;
- with the defaults this is 9.6 mm;
- the standalone STL is generated from this state.

### Installed

Installed is the same manufactured clamp fitted around the target tube.

- `installed` is not suppressed;
- the original Free clamp body is not replaced;
- the ring opens enough to accommodate `tube_d`;
- with the defaults the contact diameter becomes Ø10 mm;
- the open lips move farther apart;
- wall thickness is retained;
- the ring remains continuous;
- the female-slot or male-dovetail interface remains attached to the same ring.

Installed is a geometric representation of elastic preload. It is not intended
to calculate stress, strain or contact pressure.

## What the `installed` step must do

The `installed` history step represents the mechanical act of opening the
preloaded ring around the tube.

Its geometric intent is:

- keep the rear/interface side of the clamp as the stable attachment datum;
- open the ring symmetrically toward the existing gap;
- increase the tube-contact envelope from the Free bore to `tube_d`;
- preserve the clamp wall rather than offsetting only the inner face;
- preserve the amount of ring material as closely as the chosen CAD
  approximation allows;
- move connected ring geometry coherently with the opening.

For the current defaults, the expected visible result is a slightly wider ring
opening than the 90° Free opening. A conserved neutral-axis approximation gives
roughly 99° and is useful as a verification target, but the history contract is
more important than that exact number.

## Configuration behavior

The standalone document must configure only the suppression state of the named
`installed` feature.

Conceptually:

```python
clamp.configure(
    active="Free",
    columns=(clamp.feature("installed"),),
    rows={
        "Free": (True,),
        "Installed": (False,),
    },
)
```

So:

- **Free** = `installed` suppressed;
- **Installed** = `installed` active.

The configuration must no longer switch `clamp_bore` between two row
expressions to create the state change.

The same contract applies to both the female-slot and male-dovetail clamp
variants.

## Explicit non-solution

The `installed` step must **not** be:

```python
body = body - Cylinder(d=tube_d, ...)
```

That operation enlarges the bore by deleting material. It changes wall
thickness and does not represent deformation of the printed clamp.

Likewise, Installed must not be implemented as:

- a second independently rebuilt clamp body;
- a second nominal ring with a different radius;
- a Python `if installed:` geometry branch;
- a fake boolean parameter standing in for feature suppression.

## Forge / SolidCraft capability boundary

The desired consumer contract is clear even if the exact deformation operation
is not yet known:

- one named `installed` history feature;
- suppressed by default;
- Free/Installed selected only through feature suppression;
- the feature deforms/opens the existing ring without material removal.

Implementation must first determine whether the released Forge/SolidCraft
surface can express that deformation as one semantic history step.

If it can, implement it locally in this CAD model.

If it cannot, stop at the concrete missing operation and describe that missing
generic capability separately. Do not substitute another bore cut merely to
make the suppression mechanism work.

## Scope after approval

After approval, the CAD change may:

- replace the current parameter-row Free/Installed switching;
- author one `installed` history feature in the reusable clamp;
- use that feature in both female and male variants;
- configure only its suppression state;
- keep Free active by default;
- update model text and visual evidence to show the larger Installed opening.

No unrelated Forge API redesign or HUB75 geometry cleanup is part of this
change.

## Verification

The implementation is acceptable when all of the following are true:

1. Free is the existing printable preloaded clamp.
2. Free has `installed` suppressed.
3. Installed differs only by unsuppressing that one named history step.
4. Installed visibly opens the clamp around Ø10 mm.
5. The Installed step does not remove material to enlarge the bore.
6. Wall thickness remains materially unchanged.
7. The clamp remains one continuous body with the same physical identity.
8. Female and male variants use the same Installed-state mechanism.
9. The standalone STL remains Free.
10. Saved SolidCraft configuration can switch Free/Installed without rerunning
    Forge Python.

## Approval gate

This record defines the intended history and physical behavior only.

No geometry implementation is approved until the one-step suppression contract
and its deformation behavior are accepted.
