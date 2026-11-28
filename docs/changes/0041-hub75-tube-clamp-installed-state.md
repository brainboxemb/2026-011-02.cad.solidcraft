# 0041 — HUB75 tube-clamp Installed state as one later suppressible history step

Status: Proposed  
Issue: #281

## Decision to review

This change must use the same generic history pattern that was already intended
and backend-qualified for configuration suppression:

~~~text
author base geometry
    |
    +-- later state-changing CAD step      [suppressed in base state]
~~~

For the HUB75 clamp:

~~~text
Free profile sketch
    |
    +-- Extrude -> physical Free clamp
    |
    +-- Installed geometry adjustment      [suppressed in Free]
~~~

For the previously qualified position example:

~~~text
normal body
    |
    +-- ServicePosition move               [suppressed in Normal]
~~~

These are the same configuration concept.

The last step is normal authored CAD history. Configuration does not rebuild the
model from another parameter set; it only suppresses or enables that last step.

No new configuration concept, Toggle, flex/deformation API or clamp-specific
state mechanism is required.

## What was already validated in Forge

The earlier `configuration-position-suppression` backend probe already proved
the essential pattern in SolidCraft:

1. create normal geometry;
2. author one later history operation (`solid.move`, named `ServicePosition`);
3. configure that exact history feature;
4. Normal suppresses it;
5. Service enables it;
6. saved row switching works without rerunning Forge Python.

The public Forge `feature(name, suppressed=...)` work then added stable Forge
identity and configuration targeting for one later authored CAD history operation.

So the clamp must not invent another state system. It must exercise that same
history contract with a geometry-changing operation suitable for the clamp.

## Where the previous acceptance went wrong

The original Installed work was not actually consumer-validated with the clamp
history above.

During #444 the backend probes proved native feature suppression, including the
`ServicePosition` move. The first clamp probe used a second cylindrical cut only
to prove suppression mechanics.

That probe was later correctly marked as insufficient consumer evidence.

However #506 was then closed by choosing:

- parameter-driven Free/Installed for the tube clamp; and
- the panel-pin revolve as the consumer proof for named feature suppression.

That means the real clamp scenario:

~~~text
Free clamp
    |
    +-- later Installed geometry change    [suppressible]
~~~

was not what ultimately closed the acceptance gap.

This change restores that missing consumer requirement.

## Required clamp history

The physical Free clamp remains the normal authored part.

For the current defaults:

~~~text
tube_d             = 10.0 mm
clamp_interference = 0.4 mm
clamp_wall         = 2.0 mm

Free bore          = 9.6 mm
Free opening       = 90 deg
~~~

The model is authored in this order:

1. create the Free ring profile;
2. extrude it to the physical clamp;
3. author one later Installed geometry-adjustment step;
4. keep that step suppressed by default;
5. let the final configuration select only the suppression state of that step.

Conceptually:

~~~python
body = build_free_clamp(...)

with feature("installed", suppressed=True) as installed:
    body = apply_installed_geometry(body, ...)

body.configure(
    active="Free",
    columns=(installed,),
    rows={
        "Free": (True,),
        "Installed": (False,),
    },
)
~~~

`apply_installed_geometry(...)` is not a proposed new Forge API name. It stands
for the ordinary generic CAD history operation needed to move the clamp's
existing geometry to the Installed position.

The configuration contract is already the existing named-feature contract.

## Installed geometry intent

Installed is the same manufactured clamp fitted around the Ø10 mm tube.

The later geometry adjustment must:

- act after the Free clamp has been authored;
- move the relevant existing geometry rather than cut material away;
- retain the 2.0 mm wall;
- open the clamp enough for Ø10 mm;
- keep the clamp as the same physical part;
- keep the rear/interface side as the stable datum;
- remain one logical later history step for configuration purposes.

Using the current neutral-axis approximation gives approximately:

~~~text
Free:
  inner diameter = 9.6 mm
  wall           = 2.0 mm
  opening        = 90 deg

Installed:
  inner diameter = 10.0 mm
  wall           = 2.0 mm
  opening        = 99 deg
~~~

The exact geometry calculation belongs to the consumer model.

## What Forge must provide

Forge does not need another configuration API.

The existing contract is the right one:

~~~python
with feature("installed", suppressed=True):
    # one later CAD history operation
    ...

model.configure(
    columns=(installed,),
    ...
)
~~~

The only question is whether Forge already exposes the generic CAD operation
needed to make the clamp's later geometry adjustment.

If the needed SolidCraft operation is already exposed by Forge, use it.

If SolidCraft already has the required ordinary history operation but Forge does
not expose it, add that generic CAD operation to Forge and keep the existing
`feature(...)` / `configure(...)` mechanism unchanged.

If SolidCraft itself lacks that ordinary history operation, that is a backend
capability gap.

Do not redesign configuration to work around a missing geometry operation.

## Relation to the position example

The intended equivalence is:

~~~text
Position example:
  create item
  -> later move item
  -> suppress later move in Normal

Clamp example:
  create Free clamp
  -> later adjust clamp geometry
  -> suppress later adjustment in Free
~~~

That is the acceptance criterion.

## Explicit non-solutions

Do not implement Installed as:

- `clamp_bore` switching between 9.6 and 10.0;
- a second independently rebuilt clamp;
- a larger cylindrical cut through the existing clamp;
- body scaling;
- a generic `radial_flex` abstraction;
- a Python `if installed:` geometry branch;
- a separate state mechanism outside normal feature suppression.

## Verification

The implementation is acceptable when all of the following are true:

1. The Free clamp is authored first as the normal physical part.
2. One later CAD history step represents the Installed geometry adjustment.
3. That later step is named `installed`.
4. Free suppresses that step.
5. Installed enables that same step.
6. Saved SolidCraft configuration switches the step without rerunning Forge Python.
7. The result follows the same history/suppression pattern already proven by
   `ServicePosition`.
8. Free remains Ø9.6 with a 2.0 mm wall.
9. Installed accommodates Ø10.0 while retaining the 2.0 mm wall.
10. No material-removal substitute is used merely to simulate opening.
11. Female and male variants use the same Installed-history mechanism.
12. The standalone STL remains Free.

## Approval gate

Approval of this record means approval of the history model:

~~~text
Free clamp -> later Installed geometry step -> suppress/enable that step
~~~

It does not approve a new configuration abstraction.

If implementation exposes a missing Forge capability, that capability must be
the smallest generic CAD operation required to author the later geometry step,
with the already-existing named-feature suppression/configuration contract left
intact.