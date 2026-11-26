# Source reference

Design reference supplied for the tube-supported HUB75 frame:

- `hub75-screen-2panel-couplers-clamp.json`
- `hub75-screen-2panel-couplers-clamp.sc`

The native parent document owns separate **Aluminium buis boven** and
**Aluminium buis onder** components, but both use the same geometry:

- `tube_od = 10 mm`;
- `tube_wall = 1 mm`;
- inside diameter = 8 mm;
- `panel_w = 160 mm`;
- `tube_ref_margin = 20 mm`;
- `tube_length = 2*panel_w + 2*tube_ref_margin = 360 mm`;
- assembly tube axis: `tube_axis_y = -tube_front_offset - tube_od/2 = -6 mm`
  with `tube_front_offset = 1 mm`.

Native feature pairs 167/168 (top) and 171/172 (bottom) create equivalent
hollow profiles. The catalog therefore owns one reusable physical tube and the
assembly owns top/bottom placement.

## Local component frame

The reusable catalog component is centered at its local origin and runs along
local X. The later frame subassembly places the two occurrences at the
source-derived world datums.

Forge v0.19 supports one closed profile in a standalone Sketch. Until a single
standalone annular sketch is public, this owner keeps both boundaries native:
one Ø10 sketch/extrusion plus one Ø8 concentric sketch/extrusion cut. This
preserves editable hollow geometry and does not approximate the tube as a solid
rod.
