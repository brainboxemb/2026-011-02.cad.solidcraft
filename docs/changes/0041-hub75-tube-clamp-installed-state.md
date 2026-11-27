# 0041 — Physically correct HUB75 tube-clamp Installed state

Status: Proposed  
Issue: #281

## Problem

The reusable HUB75 tube clamp is a preloaded elastic part.

For the default Ø10 mm tube:

- the manufactured Free state uses `clamp_interference = 0.4 mm`;
- therefore the unloaded bore is 9.6 mm;
- installation on the Ø10 mm tube must open/deform that same printed clamp.

The current catalog representation does not express that physical distinction.
It changes `clamp_bore` from 9.6 mm to 10 mm and rebuilds the parametric ring
at the new diameter. That is a useful configuration consumer, but by itself it
does not show that one manufactured part is being elastically opened by the
tube.

The withdrawn #270 proposal is also not physically acceptable. Cutting the
9.6 mm bore out to 10 mm removes material and thins the clamp. It represents
machining, not preload or elastic deformation.

This change defines the physical/modeling contract before another geometry
implementation is attempted.

## Existing evidence

The retained standalone SolidCraft source records two parameter rows:

```text
Free       clamp_bore = tube_d - clamp_interference
Installed  clamp_bore = tube_d
```

That source is valid historical authoring evidence. It does not require the
Forge configuration API that was developed from this consumer example to be
redesigned.

Historical CAD issue #199 also records a parent-frame feature called
`Installed` that applied tube-fit behavior after linked clamp insertion.
That record explains why later work explored a named Installed history feature,
but it is not sufficient evidence that a bore-widening cut is the correct
mechanical model.

Current Forge configuration capability is therefore treated as available
infrastructure, not as the problem being solved here.

## Physical contract

### Free

`Free` is the authoritative manufacturing state:

- no tube is present;
- the clamp is unloaded;
- `tube_d` is the target tube diameter;
- `clamp_interference` is the diametral preload;
- default inner diameter is
  `tube_d - clamp_interference = 9.6 mm`;
- the printable STL remains Free.

### Installed

`Installed` represents the same manufactured clamp fitted around the target
tube.

It must therefore satisfy all of the following:

1. the contact envelope accommodates `tube_d`;
2. material is not removed or added merely to create Installed;
3. wall thickness is not intentionally reduced to create Installed;
4. the ring remains one continuous elastic part with the same topology;
5. the open lips move apart rather than being replaced by a larger manufactured
   ring;
6. geometry attached to the ring remains mechanically coherent with that
   deformation;
7. the state is a geometric/kinematic representation of preload, not a claim of
   stress or FEA accuracy.

The female-slot and male-dovetail variants share this ring-state contract. Their
different slide interfaces do not change the Free/Installed mechanics.

## Why the current parameter row is incomplete

The current SCPF ring derives:

```text
clamp_r     = clamp_bore / 2
clamp_r_out = clamp_r + clamp_wall
```

Changing only `clamp_bore` therefore changes the nominal inner and outer
radii. It describes another exact concentric ring geometry. It does not encode
how the original 9.6 mm clamp opens around the 10 mm tube.

The ring opening is currently fixed at 90 degrees, so the state change also
fails to communicate the visible opening that preload should cause.

## Proposed geometric model

The leading model for review is a simple kinematic deformation approximation,
not material removal.

Preserve:

- constant wall thickness;
- the free-state neutral-axis arc length of the elastic ring;
- symmetry about the existing opening;
- the rear/interface datum opposite the opening as the stable attachment side.

Let:

```text
r_free       = (tube_d - clamp_interference) / 2
r_neutral    = r_free + clamp_wall / 2
theta_free   = 360 deg - clamp_open
arc_length   = r_neutral * theta_free
```

For Installed:

```text
r_installed_neutral = tube_d / 2 + clamp_wall / 2
theta_installed     = arc_length / r_installed_neutral
open_installed      = 360 deg - theta_installed
```

For the current defaults:

```text
tube_d             = 10.0 mm
clamp_interference = 0.4 mm
clamp_wall         = 2.0 mm
clamp_open Free    = 90 deg

neutral radius Free      = 5.8 mm
neutral radius Installed = 6.0 mm
occupied arc Free        = 270 deg
occupied arc Installed   = 261 deg
opening Installed        = 99 deg
```

This gives the desired visible behavior: the same nominal material arc opens
approximately 9 degrees while accommodating the Ø10 tube, instead of losing
0.2 mm of material radially.

This is the proposed modeling contract for approval. It is intentionally a
kinematic approximation; no elastic modulus, stress distribution or nonlinear
contact solver is implied.

## Configuration representation

No new Forge API is assumed.

If this proposed model is approved, the expected CAD representation is to make
the deformation-driving geometry explicit parameters of the reusable clamp and
let the existing final-model configuration select the Free and Installed
values.

Conceptually the state needs at least:

- the bore/contact diameter;
- the corresponding opening angle derived from the conserved neutral-axis arc
  length.

The exact public/internal parameter split is implementation work and must not be
committed until this record is approved.

A named history feature is not required merely because the state is called
Installed. Feature suppression should only be used if the approved CAD
implementation genuinely contains one history operation whose suppression
represents the entire deformation.

## Forge capability check

Current Forge/SolidCraft evidence shows ordinary parameter configuration,
feature suppression, shape translation and SolidCraft `Offset Face` support.
No public Forge flex/deformation operation was identified.

That absence does **not** currently block this proposed model: the kinematic
ring state can be described parametrically with existing sketch dimensions.

Therefore this change does not create a Forge issue yet.

Create a separate Forge issue only if implementation of the approved model
demonstrates a specific missing generic capability that cannot be represented
through the existing parameter/configuration contract.

## Scope after approval

Expected CAD scope:

- reusable ring geometry shared by female and male variants;
- standalone Free/Installed configuration evidence;
- higher-level HUB75 tube-frame consumers that drive the same shared installed
  state;
- model/reference text that describes the physical state accurately;
- visual evidence that makes the larger Installed opening visible.

## Non-goals

This change does not:

- redesign Forge configuration;
- add a Forge deformation API speculatively;
- model stress, strain or contact pressure;
- change the tube diameter default;
- change the female-slot or male-dovetail interface geometry for unrelated
  reasons;
- make Installed the manufacturing/STL state;
- use a bore-widening cut as a deformation substitute;
- introduce a second independent Installed body.

## Verification after implementation

Implementation is acceptable only when all of the following can be shown:

1. Free remains the current printable unloaded geometry.
2. Installed accommodates the target tube diameter.
3. Installed visibly opens the clamp lips relative to Free.
4. The Installed state does not thin the wall by subtracting the interference.
5. The ring remains continuous and mechanically attached to its interface.
6. Female and male variants use the same deformation rule.
7. Saved SolidCraft configuration can switch state without rerunning Forge
   Python.
8. The standalone STL remains Free.
9. Higher-level tube-frame occurrences use the same approved Installed contract.
10. Any newly discovered Forge limitation is isolated in a separate Forge issue
    with a concrete consumer case.

## Approval gate

No HUB75 geometry change is authorized by this Proposed record.

Approval must explicitly confirm the physical contract and the proposed
constant-wall / conserved-neutral-arc approximation, or replace it with an
alternative model before implementation starts.
