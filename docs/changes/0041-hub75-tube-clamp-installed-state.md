# 0041 — HUB75 tube-clamp Installed state as one suppressible deformation feature

Status: Proposed  
Issue: #281

## Decision to review

The intended model is:

- **Free** is the current printable preloaded clamp;
- **Installed** is the same clamp opened around the target tube;
- exactly one history feature is named installed;
- installed is suppressed in Free and active in Installed;
- that feature changes the ring by deformation, not by cutting material away;
- the 2.0 mm ring wall and the neutral-axis material length are retained;
- the rear/interface datum stays fixed while the two lips open symmetrically.

The released Forge v0.27.0 configuration API already supports the required
suppression/configuration part.

It does **not** currently expose a solid-history operation that can perform the
required continuous ring deformation as one feature. SolidCraft 0.50.0 also has
no native solid flex/deformation command with those semantics.

Therefore this change cannot be implemented correctly as only a CAD-model edit
against the current released API. If this design is approved, a small,
consumer-driven deformation capability is required below the model. The
configuration API itself does not need redesign.

## Problem

The HUB75 tube clamp is a preloaded elastic part.

For the default Ø10 mm tube with 0.4 mm diametral interference, the printable
Free clamp has a 9.6 mm bore. When that same printed clamp is pushed over the
Ø10 mm tube, the ring opens elastically.

The current catalog models the two states by changing clamp_bore:

~~~python
clamp.configure(
    active="Free",
    columns=(self.clamp_bore,),
    rows={
        "Free": ("tube_d-clamp_interference",),
        "Installed": ("tube_d",),
    },
)
~~~

That produces two nominal ring geometries. It does not represent one
manufactured clamp being opened after it has been printed.

The withdrawn #270 direction correctly tried to make Installed one named
history feature, but the proposed operation was wrong:

~~~python
with feature("installed", suppressed=True):
    body = body - Cylinder(d=self.tube_d, ...)
~~~

That enlarges the bore by deleting material and reduces the wall thickness. It
represents machining, not elastic preload.

The history idea from #270 is retained; the bore-widening cut is not.

## Required history

The clamp history must read conceptually as:

~~~text
Free ring
    |
    +-- Installed deformation     [suppressed in Free]
    |
    +-- female or male interface features
~~~

The deformation is intentionally placed immediately after the shared ring is
created and before the female-slot or male-dovetail interface is added.

That ordering matters:

- the deformation operates only on the elastic ring;
- the rear side of the ring is the fixed datum;
- the later slide-interface geometry is authored from that fixed rear datum;
- the female/male interface itself is therefore not stretched or scaled.

The final document configuration is only:

~~~python
clamp.configure(
    active="Free",
    columns=(clamp.feature("installed"),),
    rows={
        "Free": (True,),
        "Installed": (False,),
    },
)
~~~

where True means the feature is suppressed.

No clamp_bore configuration column is required for the Free/Installed state
after this change.

## Free geometry

Free remains the manufacturing state and the authoritative STL geometry.

For the current defaults:

~~~text
tube_d             = 10.0 mm
clamp_interference = 0.4 mm
clamp_wall         = 2.0 mm
clamp_open         = 90 deg

inner radius       = 4.8 mm
outer radius       = 6.8 mm
neutral radius     = 5.8 mm
occupied sweep     = 270 deg
~~~

The standalone document starts in Free and installed is suppressed.

## Proposed Installed geometry

Installed is a kinematic deformation approximation of the same elastic ring.
It is not an FEA model.

The geometric invariant is the neutral-axis arc length of the ring.

For Free:

~~~text
r_free_neutral = 4.8 + 2.0 / 2
               = 5.8 mm

sweep_free     = 360 - 90
               = 270 deg
~~~

The neutral-axis material length is therefore:

~~~text
L = r_free_neutral * radians(sweep_free)
~~~

Installed must accommodate the Ø10 mm tube while retaining the 2.0 mm wall:

~~~text
installed inner radius   = 5.0 mm
installed neutral radius = 6.0 mm
installed outer radius   = 7.0 mm
~~~

With the same neutral-axis material length:

~~~text
sweep_installed
    = sweep_free * r_free_neutral / r_installed_neutral
    = 270 * 5.8 / 6.0
    = 261 deg

open_installed
    = 360 - 261
    = 99 deg
~~~

So the intended visual/mechanical change is:

~~~text
Free                         Installed
inner Ø9.6                   inner Ø10.0
wall 2.0                     wall 2.0
opening 90 deg               opening 99 deg
rear datum fixed             rear datum fixed
neutral arc length L         same neutral arc length L
~~~

The extra 9 degrees of opening is distributed symmetrically, approximately
4.5 degrees per lip, around the fixed rear datum.

This is the geometry the installed feature must produce for the current
defaults.

## Proposed clamp code

The model should keep the current shared Free ring construction and insert the
one Installed operation directly after its extrusion.

Conceptually:

~~~python
free_r = (self.tube_d - self.clamp_interference) / 2.0
free_r_neutral = free_r + CLAMP_WALL / 2.0
installed_r_neutral = self.tube_d / 2.0 + CLAMP_WALL / 2.0

ring_sketch = _open_clamp_ring(
    clamp_r=free_r,
    clamp_r_out=free_r + CLAMP_WALL,
    clamp_open=CLAMP_OPEN,
)
ring = ring_sketch.extrude(CLAMP_WIDTH)

with feature("installed", suppressed=True):
    ring = ring.radial_flex(
        axis=Axis.Z,
        fixed_angle=180.0,
        neutral_radius=free_r_neutral,
        target_neutral_radius=installed_r_neutral,
        preserve_neutral_length=True,
    )

body = ring

# Existing female or male interface history follows here.
~~~

radial_flex(...) above is the **proposed missing operation**, not an API that
exists in Forge v0.27.0.

Its required semantics are deliberately narrow:

- act on one continuous solid body;
- bend/unbend the body around one axis;
- keep one angular datum fixed;
- change the neutral radius;
- preserve neutral-axis length;
- keep the cross-section, including the 2.0 mm wall and 12 mm width;
- return one continuous solid;
- author exactly one native history feature so the existing
  feature("installed", suppressed=True) contract can name and suppress it.

The final API name and exact argument spelling belong to the Forge/SolidCraft
capability design. The clamp-side semantics above are the consumer requirement.

## Current API audit

### What Forge v0.27.0 already provides

The following parts are already sufficient:

~~~python
with feature("installed", suppressed=True):
    ...

clamp.feature("installed")

clamp.configure(
    active="Free",
    columns=(clamp.feature("installed"),),
    rows={
        "Free": (True,),
        "Installed": (False,),
    },
)
~~~

So feature identity, initial suppression, reusable-component feature exposure
and saved Free/Installed configuration do not need another redesign.

### Shape.move(...) is not the missing deformation

Forge v0.27.0 Shape.move(x, y, z) is a CSG translation helper.

It:

- translates an entire primitive/CSG shape;
- is feature-transparent in the current Forge history model;
- does not rotate or deform part of one continuous solid;
- does not create the required native suppressible body-history operation.

It therefore cannot open this ring.

### Native SolidCraft solid.move is also insufficient

SolidCraft 0.50.0 has a richer solid.move command with rigid translation and
rotation of bodies.

Forge v0.27.0 does not expose that command as the required public Shape-history
operation, but exposing it alone would still not solve this clamp.

A rigid move can move whole bodies. Opening this one continuous C-shaped ring
requires different displacement around the arc. Splitting the ring into rigid
halves would change the modeling contract, and a symmetric opening would require
opposite transforms rather than one history transform.

So the missing capability is not merely "expose solid.move".

### Native SolidCraft solid.scale is not acceptable

SolidCraft has solid.scale, but Forge v0.27.0 does not expose it as this
history operation.

More importantly, scaling the ring from Ø9.6 to Ø10 would also scale the wall
and the ring material. It would not preserve the 2.0 mm wall or neutral-axis
material length.

It is therefore not the Installed model.

### Native SolidCraft solid.offset_face is not acceptable

SolidCraft has solid.offset_face, also not exposed by the current Forge
surface.

One offset distance cannot move both the inner and outer cylindrical faces in
the required radial direction while preserving a 2.0 mm wall. Doing that with
separate offsets would require multiple history operations and would no longer
be the one suppressible Installed step.

### Parameter configuration is geometrically usable but has the wrong history

Forge can already parameterize both bore and opening angle. A two-parameter
Free/Installed table could therefore reproduce the 9.6/90 and 10.0/99 geometry
without a backend change.

That alternative is rejected for this change because it recreates the ring from
configuration values instead of representing Installed as one later
suppressible deformation of the Free clamp.

If the one-step history requirement is intentionally dropped later, this is the
available no-API-change fallback.

## Capability conclusion

The proposed clamp geometry is now concrete, and the capability result is also
concrete:

**Forge v0.27.0 + SolidCraft 0.50.0 cannot currently express the approved
physical intent as one suppressible Installed history feature.**

The missing capability is one continuous-solid bend/flex operation that can
change the radius of a curved constant-section body while preserving its
neutral-axis length and a fixed datum.

This is not a configuration problem.

A follow-up capability design must therefore answer one focused question:

> How does Forge author one native SolidCraft history feature that performs the
> radial bend/flex described above on a continuous body?

If SolidCraft first needs such a native history command, that backend dependency
must be implemented there rather than hidden in CAD consumer code.

Do not replace this gap with:

- the old bore-widening cut;
- a scaled ring;
- two or more hidden offset operations;
- split rigid clamp bodies;
- a Python if installed: branch;
- a second independent Installed body.

## Scope after approval

After this record is approved:

1. record the missing deformation capability in its owning Forge/SolidCraft
   issue/design;
2. implement and qualify that capability independently;
3. adopt the released capability in this CAD catalog;
4. insert installed immediately after the shared ring extrusion in both
   female and male variants;
5. replace the current clamp_bore Free/Installed configuration column with
   one suppression column targeting clamp.feature("installed");
6. keep Free active for the standalone catalog model and STL;
7. update visual evidence so Free and Installed can be compared directly.

No bore-cut substitute is permitted while the capability is missing.

## Verification

The eventual implementation is acceptable only when all of the following are
true:

1. Free is the existing printable preloaded clamp.
2. Free has installed suppressed.
3. Installed differs by activating exactly that one named history feature.
4. Default Free geometry is Ø9.6 inner diameter, 2.0 mm wall and 90° opening.
5. Default Installed geometry accommodates Ø10.0, retains the 2.0 mm wall and
   opens to approximately 99° under the neutral-axis model.
6. The rear/interface datum does not move.
7. The clamp remains one continuous body.
8. No clamp material is removed merely to create Installed.
9. Female and male variants use the same ring deformation mechanism.
10. Their later interface features remain mechanically coherent and are not
    themselves scaled/deformed.
11. The standalone STL remains Free.
12. Saved SolidCraft configuration switches Free/Installed without rerunning
    Forge Python.

## Approval gate

Approval of this record means approval of:

- the one-feature suppression history;
- the constant-wall, conserved-neutral-axis Installed approximation;
- the fixed rear datum and symmetric lip opening;
- the conclusion that the current released API is missing the required
  deformation operation.

It does **not** approve an arbitrary new Forge API name or implementation. That
capability must be designed and qualified in its owning repository before this
CAD model adopts it.
