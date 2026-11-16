# Forge change 0022 — standard primitive origins

Forge now places the geometric CENTER of a new Box, Cylinder or Sphere at
(0, 0, 0). A direct native primitive and the same primitive inside CSG use
the same origin. Cylinder placement no longer means its native base by default.

This CAD migration makes the old bottom-datum intent explicit where needed.
These changes preserve the dimensions and native coordinates of the models;
they are not visual workarounds to keep an old API:

- **Plate:** bottom Z=0, through holes entering at Z=thickness.
- **Plastic enclosures:** bottom Z=0, including Pi connector/vent/engraving
  sketch reference planes and native boss positioning.
- **Detailed HUB75 panel:** bottom Z=0 for the 2 mm front face, tapered rear
  face and six blind rear bores.
- **Basic components and joint diagnostics:** preserve the original local
  bottom datum and expected native geometry selectors.

The HUB75 wooden Board and Window already place by explicit
`anchor=FRONT + BOTTOM` in `.at(...)`; their construction needs no migration.
The lightweight HUB75 panel is a coordinate-authored XZ Polygon2D and keeps
its authored reference coordinates. CSG Cube already centers its primitives.

The CAD repository now pins the exact Forge 0.5.0 release-candidate main
commit. The automatic release workflow must confirm the v0.5.0 tag points
to that same commit before this CAD branch is merged.

Verification requirements:
1. Run the CAD model unit and reference JSON tests.
2. Compile every supported CAD model against the pinned Forge revision.
3. Run native SolidCraft 0.42.0 Q3–Q6 on impacted models, especially detailed
   HUB75, wooden frame and Pi enclosure.
4. Check that the saved model's parameter changes keep the intended reference
   planes and no manual offsets were added solely to emulate old defaults.

Reference API syntax for PythonSCAD, pyBOSL2 and CadQuery stays in Forge's
local `docs/agent/reference-libraries.md`; do not re-fetch their upstream
repositories for normal comparison work.
