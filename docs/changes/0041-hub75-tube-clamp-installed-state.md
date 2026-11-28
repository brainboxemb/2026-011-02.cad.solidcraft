# 0041 — HUB75 tube-clamp Installed state as one suppressible geometry edit

Status: Proposed  
Issue: #281

## Decision to review

The Installed state does **not** require a generic flex/deformation operation.

The clamp profile is already defined by explicit sketch points and circular arcs.
For Installed, the required geometry can be produced by moving the points that
define that profile to new calculated positions.

The intended history is:

1. author the normal Free clamp profile;
2. define one geometry-edit step named `installed`;
3. that step moves the relevant profile points/arc centres to their Installed coordinates;
4. Free suppresses that step;
5. Installed enables that step;
6. the existing extrusion and female/male interface history use the resulting profile.

~~~text
Free ring sketch
    |
    +-- Installed point move      [suppressed in Free]
    |
    +-- Extrude
    |
    +-- female or male interface features
~~~

The first question for Forge is deliberately smaller than a point-edit API:

> Can a normal Forge `Sketch` be used directly as a named suppressible
> configuration target?

SolidCraft already supports Sketch suppression. Forge v0.27 does not currently
expose Sketch as such a target. That gap must be resolved before inventing any
new geometry operation. A generic `radial_flex`, deformation solver or material
model is out of scope.

## Problem

The HUB75 tube clamp is a preloaded elastic part.

For the default Ø10 mm tube with 0.4 mm diametral interference, the printable
Free clamp has a 9.6 mm bore. When that same printed clamp is pushed over the
Ø10 mm tube, the opening becomes wider.

The current catalog models the states by changing `clamp_bore`:

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

That rebuilds the ring from different parameter values. It does not show
Installed as one later CAD step that may be suppressed.

The withdrawn #270 direction correctly tried to make Installed one named
history feature, but the operation was wrong:

~~~python
with feature("installed", suppressed=True):
    body = body - Cylinder(d=self.tube_d, ...)
~~~

That removes material and thins the clamp. It is not the geometry change we want.

## Existing ring geometry

The shared ring in `common.py` is already authored from a small number of
calculated points:

~~~python
half_open = radians(CLAMP_OPEN / 2.0)
radial_mid = (clamp_r + clamp_r_out) / 2.0

outer_x = clamp_r_out * cos(half_open)
outer_y = clamp_r_out * sin(half_open)
inner_x = clamp_r * cos(half_open)
inner_y = clamp_r * sin(half_open)
lip_center_x = radial_mid * cos(half_open)
lip_center_y = radial_mid * sin(half_open)
~~~

Those values define the outer and inner arc endpoints and the two lip-arc centres.
The two main ring arcs keep their centre at the sketch origin.

Installed therefore does not need a new geometric primitive. It needs new
coordinates for the same profile-defining references.

## Free geometry

With the current defaults:

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

Approximate Free coordinates:

~~~text
outer x = 4.808 mm    outer y = ±4.808 mm
inner x = 3.394 mm    inner y = ±3.394 mm
lip x   = 4.101 mm    lip y   = ±4.101 mm
~~~

Free remains the active standalone state and the STL state.

## Installed target geometry

Installed should accommodate the Ø10 mm tube without reducing the 2.0 mm wall.
The selected simple approximation keeps the Free neutral-axis arc length.

Therefore:

~~~text
installed inner radius   = 5.0 mm
installed outer radius   = 7.0 mm
installed neutral radius = 6.0 mm

sweep_installed = 270 deg * 5.8 / 6.0 = 261 deg
open_installed  = 360 deg - 261 deg   = 99 deg
~~~

So `half_open` changes from 45° to 49.5° and the Installed coordinates are
calculated with the same equations as Free:

~~~text
outer x = 4.546 mm    outer y = ±5.323 mm
inner x = 3.247 mm    inner y = ±3.802 mm
lip x   = 3.897 mm    lip y   = ±4.562 mm
~~~

The Installed step is therefore a deterministic move from the Free references
to these Installed references. No material is cut away and no generic body
deformation algorithm is needed.

## Proposed clamp authoring

The desired model is conceptually:

~~~python
ring = _open_clamp_ring(
    clamp_r=free_r,
    clamp_r_out=free_r + CLAMP_WALL,
    clamp_open=CLAMP_OPEN,
)

installed_points = _installed_ring_points(
    tube_d=self.tube_d,
    clamp_wall=CLAMP_WALL,
    free_r=free_r,
    free_open=CLAMP_OPEN,
)

with feature("installed", suppressed=True):
    ring = ring.move_points(installed_points)

body = ring.extrude(CLAMP_WIDTH)

# Existing female or male interface history follows.
~~~

The exact public spelling of `move_points(...)` is not fixed by this CAD change.
It only makes the required operation explicit.

The operation must:

- work on the existing ring sketch;
- move several related points atomically;
- keep the same profile topology;
- not cut or add material;
- result in one named history step;
- be suppressible by configuration.

## Configuration behavior

The final configuration should target only that one history step:

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

~~~text
Free       installed = suppressed
Installed  installed = active
~~~

The Free/Installed state no longer needs `clamp_bore` as a configuration column.

## Current API audit

### SolidCraft already supports Sketch suppression

SolidCraft 0.50.0 represents a Sketch as a normal timeline feature. Its
suppression/configuration commands accept feature names/ids, and existing
SolidCraft examples explicitly suppress Sketch features.

So the backend does **not** need a new deformation or point-edit feature merely
to make a Sketch suppressible.

### Forge v0.27.0 does not expose that capability

This is the actual Forge gap.

The released configuration design currently permits only:

- a `Parameter` as a value column; or
- an authored **Shape/feature handle** as a suppression column.

The released `feature(name, suppressed=...)` contract is also deliberately
restricted to one terminal Shape and says that helper Sketch/profile
construction belongs outside the feature scope.

Therefore this is currently valid Forge authoring:

~~~python
with feature("installed", suppressed=True):
    body = body - cutter

model.configure(
    columns=(installed_feature,),
    ...
)
~~~

but the equivalent direct Sketch target is not part of the public v0.27 API:

~~~python
with Sketch(name="installed", plane="XY") as installed:
    ...

model.configure(
    columns=(installed,),
    ...
)
~~~

That is narrower than SolidCraft's own feature model and is the first capability
gap this change should address.

### What Forge should add

The first proposal is intentionally small:

> A Forge `Sketch` must be a first-class feature handle that can be used as a
> suppression/configuration target.

Conceptually:

~~~python
with Sketch(name="installed", plane="XY") as installed:
    # installed-state geometry

model.configure(
    active="Free",
    columns=(installed,),
    rows={
        "Free": (True,),
        "Installed": (False,),
    },
)
~~~

The exact clamp history must then be qualified against SolidCraft dependency
behavior.

The required probe is:

1. create a named Sketch;
2. create geometry that depends on that Sketch;
3. configure the Sketch as suppressed/active;
4. reopen the saved design and switch rows;
5. verify whether the dependent feature follows the Sketch state correctly.

If SolidCraft requires the dependent Extrude to be suppressed separately, Forge
must not invent a deformation API. Instead the design must decide whether:

- the Sketch plus its direct dependent operation should be exposed as one
  logical suppressible feature; or
- the clamp should use an explicitly grouped suppression target.

That decision belongs to the Forge feature/configuration design.

### What was already built

The existing Forge configuration work is still useful:

- native saved configuration tables;
- stable Forge identity for Shape-producing history features;
- suppression rows that survive save/reopen;
- reusable-component feature references.

What it did **not** yet generalize is suppression of every native timeline
feature type. Sketch is the concrete missing case exposed by this clamp.

## Explicit non-solutions

Do not solve Installed with:

- a larger cylindrical bore cut;
- `radial_flex` or another generic deformation abstraction;
- body scaling;
- two independent clamp bodies;
- a Python `if installed:` branch;
- a second unrelated Installed sketch;
- multiple hidden history operations presented as one state.

A parameter-row implementation remains technically possible, but it does not
meet the requested one-suppressed-step history and is not the design proposed here.

## Scope after approval

After this record is approved:

1. add/qualify Forge support for a normal `Sketch` as a suppression/configuration target;
2. prove the saved SolidCraft behavior for a Sketch and its dependent geometry;
3. only if the dependent operation does not follow the Sketch state, design the
   smallest logical/grouped suppression contract needed by Forge;
4. do not add a generic deformation API for this clamp;
5. then implement the selected Free/Installed sketch history in the shared HUB75 clamp;
6. replace the current parameter Free/Installed table with the resulting suppression target;
7. keep Free active for the standalone model and STL.

## Verification

The eventual implementation is acceptable when:

1. Free remains the existing printable clamp.
2. Free has `installed` suppressed.
3. Installed is produced by activating exactly one point-edit history step.
4. Default Free inner diameter remains Ø9.6 mm.
5. Installed inner diameter becomes Ø10.0 mm.
6. Wall thickness remains 2.0 mm.
7. The opening changes from 90° to approximately 99° under the selected
   neutral-axis approximation.
8. The ring remains one continuous profile/body.
9. No material-removal feature creates Installed.
10. Female and male variants use the same shared ring edit.
11. The standalone STL remains Free.
12. Saved SolidCraft configuration switches Free/Installed without rerunning Forge Python.

## Approval gate

Approval means approval of:

- one suppressible Installed history step;
- implementing that step as movement of the existing ring's defining sketch
  points/arc centres;
- the Ø10 / 2.0 mm wall / approximately 99° Installed target for the current defaults;
- treating Sketch suppression as the first missing Forge capability to resolve;
- qualifying how dependent geometry follows that Sketch state.

It does **not** approve a generic deformation API or a new point-edit history API.