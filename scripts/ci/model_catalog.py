"""Central model catalog for CAD source, CI and the results site.

This follows the same pattern as Forge qualification/cases.py: one explicit
metadata table is consumed by workflows, site generation and tests. A model
slug should not need to be copied into other lists.
"""
from pathlib import Path
import argparse


SECTION_INFO = {
    "basic": (
        "Basic Models",
        "Small, transparent models used to develop and verify SCPF features.",
    ),
    "components": (
        "Components",
        "Reusable physical parts compiled directly from the same source assemblies import.",
    ),
    "advanced": (
        "Advanced Models",
        "Full designs and nested native assemblies built from reusable components.",
    ),
}


MODELS = {
    "plate": {
        "source": "models/basic/plate/scpf/model.py",
        "section": "basic",
        "title": "Plate",
        "tagline": "A rounded plate with four holes",
        "description": "A feature-based plate: sketch, extrusion, four vertical fillets and a through-hole sketch.",
        "parameters": "100 × 60 × 10 mm; four Ø8 mm holes",
        "diagram": "plate",
        "stages": [
            "Sketch the rectangle",
            "Extrude the base",
            "Fillet vertical corners",
            "Sketch four hole centres",
            "Cut the holes",
        ],
        "scpc_source": "models/basic/plate/scpc/model.py",
        "scpc_command_count": 9,
        "native": True,
        "native_snapshot_required": True,
    },
    "vent-plate": {
        "source": "models/basic/vent_plate/scpf/model.py",
        "section": "basic",
        "title": "Vent Plate",
        "tagline": "One source vent repeated by a native 6 × 3 feature pattern",
        "description": "Recreates the small SolidCraft Vent Plate example with a rounded 120 × 80 × 4 mm plate, one rectangular source cut and one native two-direction rectangular pattern.",
        "parameters": "120 × 80 × 4 mm; R8; 6 × 3 vents; 16 × 22 mm pitch",
        "diagram": "plate",
        "stages": [
            "Box — 120 × 80 × 4 mm from corner [0, 0, 0]",
            "Fillet — four vertical edges R8",
            "Vent — one 6 × 14 mm source rectangle at X=18..24, Y=12..26",
            "Cut — positive 4 mm through the plate",
            "RectangularPattern — 6 columns × 3 rows at 16 × 22 mm spacing",
        ],
        "scpc_source": "models/basic/vent_plate/scpc/model.py",
        "scpc_command_count": 10,
        "native": True,
        "native_snapshot_required": True,
    },
    "bolted-flange": {
        "source": "models/basic/bolted_flange/scpf/model.py",
        "section": "basic",
        "title": "Bolted Flange",
        "tagline": "Official SolidCraft flange with one native circular bolt-hole pattern",
        "description": "Recreates the compact SolidCraft flange sample: Ø100 × 10 disc, Ø44 × 16 hub, Ø24 bore and one Ø9 source bolt hole repeated by one native six-instance circular feature pattern.",
        "parameters": "Ø100 × 26 mm overall; Ø44 hub; Ø24 bore; 6 × Ø9 on 70 mm PCD",
        "diagram": "plate",
        "stages": [
            "Disc — Ø100 Sketch on XY, extrude 10 mm",
            "Hub — Ø44 top-face Sketch, join 16 mm",
            "Bore — central Ø24 cut through the 26 mm overall height",
            "BoltHole — one Ø9 source cut at pcd / 2",
            "CircularPattern — bolts instances around the Z axis",
        ],
        "scpc_source": "models/basic/bolted_flange/scpc/model.py",
        "scpc_command_count": 19,
        "native": True,
        "native_snapshot_required": True,
    },
    "csg-cube": {
        "source": "models/basic/csg_cube/scpf/model.py",
        "section": "basic",
        "title": "CsgCube",
        "tagline": "A box, sphere and three crossing bores",
        "description": "A constructive solid geometry demonstration: intersect a cube with a sphere, then subtract cylinders along three axes.",
        "parameters": "50 mm cube; three crossing cylindrical cuts",
        "diagram": "csg",
        "stages": [
            "Create the sphere",
            "Intersect with a cube",
            "Cut along X, Y and Z",
        ],
        "native": True,
        "native_snapshot_required": False,
    },
    "bracket": {
        "source": "models/basic/bracket/scpf/model.py",
        "section": "basic",
        "title": "Bracket",
        "tagline": "An L-shaped extrusion with two mounting holes",
        "description": "An XZ polygon extruded along Y with an edge fillet and two native SolidCraft Hole features.",
        "parameters": "60 mm wide; 6 mm wall; two Ø8 mm holes",
        "diagram": "bracket",
        "stages": [
            "Draw the L profile",
            "Extrude its width",
            "Round an exposed edge",
            "Sketch mounting holes",
            "Cut through the flange",
        ],
        "native": True,
        "native_snapshot_required": True,
    },
    "sample-plate": {
        "source": "models/basic/sample_plate/scpf/model.py",
        "section": "basic",
        "title": "SamplePlate",
        "tagline": "Original four-sketch history: Base, Holes, Boss, Bore",
        "description": "Recreates the original saved SolidCraft construction history with four named sketches and sketch-based cuts. The object-level Hole and Cylinder intent is compiled to the four editable sketches and matching cut/join history.",
        "parameters": "80 × 50 × 8 mm; R6; Ø24 × 14 boss",
        "diagram": "sample",
        "stages": [
            "Base — sketch XY rectangle (80 × 50)",
            "Extrude1 — extrude base by 8 mm",
            "Fillet1 — fillet four vertical corners, R6",
            "Holes — cut two mounting holes Ø8",
            "Boss — join Ø24 boss above plate, height 14",
            "Bore — cut central Ø12 bore through full 22 mm",
        ],
        "native": True,
        "native_snapshot_required": True,
    },
    "plastic-enclosure": {
        "source": "models/basic/plastic_enclosure/scpf/model.py",
        "section": "basic",
        "title": "Plastic Enclosure",
        "tagline": "A shelled enclosure with native plastic design features",
        "description": "Rebuilds the supplied enclosure with the normal SCPF Box sketch/extrusion, followed by native Shell, Lip, Snap Fit, Boss and Rest features.",
        "parameters": "80 × 50 × 30 mm; 2 mm wall; two Ø7 × 12 bosses",
        "diagram": "plastic-enclosure",
        "stages": [
            "Enclosure footprint — sketch the 80 × 50 mm base",
            "Extrude1 — create the 30 mm solid",
            "Shell1 — hollow to 2 mm with the top open",
            "Lip1 — add a 1 × 2 mm rim lip",
            "SnapFit1 — add the 14 mm cantilever snap",
            "Boss1 / Boss2 — add two Ø7 × 12 mm screw bosses",
            "Rest1 — add the 16 × 24 × 3 mm centre rest",
        ],
        "native": True,
        "native_snapshot_required": True,
    },
    "plastic-enclosure-pi": {
        "source": "models/basic/plastic_enclosure_pi/scpf/model.py",
        "section": "basic",
        "title": "Plastic Enclosure Pi",
        "tagline": "Raspberry Pi 4 case with connectors, vents and engraving",
        "description": "Reconstructs the Raspberry Pi 4 video using a rounded open-top shell, mounting bosses, connector cuts, floor vents, Pi 4 lettering and PETG material.",
        "parameters": "95 × 66 × 24 mm; R5; PETG; 4 × M2.5 standoffs",
        "diagram": "plastic-enclosure",
        "stages": [
            "Outline — centered 95 × 66 mm footprint",
            "Extrude — height 24 mm",
            "Fillet — four vertical corners R5",
            "Shell — open top, 2 mm wall",
            "Fillet upper rim — R1",
            "Four mounting bosses — Ø6 / Ø2.5, 58 × 49 pattern",
            "Sketch and cut USB-C and dual micro-HDMI ports",
            "Sketch and cut USB / Ethernet opening",
            "Sketch and cut five floor ventilation slots",
            "Engrave Pi 4 text, 0.6 mm",
            "Assign PETG physical material",
        ],
        "native": True,
        "native_snapshot_required": True,
    },
    "corner-bracket": {
        "source": "models/components/corner_bracket/scpf/model.py",
        "section": "components",
        "title": "CornerBracket",
        "tagline": "24 mm plywood corner bracket without mounting holes",
        "description": "One shared, hole-free CornerBracket is reused by the standalone model and the wooden HUB75 enclosure. Its native outline, inner R4 fillet and elephant-foot/outer chamfers remain editable. The older hole-containing experiment is archived separately.",
        "parameters": "24 mm width, 12 mm wall, 60 mm arms; no screw holes",
        "diagram": "bracket",
        "stages": [
            "Profile — 2D L outline with arm-end bevels",
            "Extrude — symmetric 24 mm body",
            "Fillet — rounded inside corner R4",
            "Chamfer — outer edges of both broad faces",
            "Chamfer — print-face elephant-foot relief",
            "Solid bracket — mounting-hole features deliberately omitted",
        ],
        "component_source": "models/components/corner_bracket/scpf/model.py",
        "component_definition_primary": True,
        "scpc_source": "models/components/corner_bracket/scpc/model.py",
        "scpc_command_count": 17,
        "native": True,
        "native_snapshot_required": True,
    },
    "hub75-panel": {
        "source": "models/components/hub75_panel/detailed/scpf/model.py",
        "section": "components",
        "title": "Hub75Panel",
        "tagline": "One measured reusable P5 HUB75 panel component",
        "description": "Shared panel component from the existing OpenSCAD reference: a 159.70 × 319.71 × 14.50 mm envelope with four rear pockets, six rear-side blind Ø3 mounting-hole centres and a grey housing material. Standalone uses the component's own local XY/Z axes; screen assemblies rotate the exact same class into world XZ.",
        "parameters": "159.70 × 319.71 × 14.50 mm; six Ø3 holes; direct shared component root",
        "diagram": "hub75",
        "stages": [
            "Run the shared Hub75Panel component directly",
            "Sketch and extrude the physical front envelope",
            "Cut four rear electronics bays from the rear plane",
            "Cut six blind rear-side Ø3 mounting holes",
            "Assign grey housing material",
            "Keep the standalone part in its local CAD axes",
            "Verify local front and rear views in SolidCraft 0.42.0",
        ],
        "component_source": "models/components/hub75_panel/detailed/scpf/model.py",
        "component_definition_primary": True,
        "native": True,
        "native_snapshot_required": True,
    },
    "guide-rail": {
        "source": "models/components/guide_rail/scpf/model.py",
        "section": "components",
        "title": "GuideRail — Festool profile",
        "tagline": "Parametric guide rail using the detailed Festool reference extrusion",
        "description": "The generic GuideRail component with its default Festool profile. The aluminium cross-section comes from the FS 1400/2 STEP reference and is calibrated to the TSO measured 184.20 × 10.50 mm envelope. Only rail length is a native CAD parameter.",
        "parameters": "184.20 × 10.50 mm profile; 600 mm standalone example; editable length",
        "diagram": "guide-rail",
        "stages": [
            "Load the fixed Festool cross-section profile",
            "Create one detailed XZ Polygon2D",
            "Extrude symmetrically along Y by the editable length",
            "Keep profile choice outside the native parameter list",
        ],
        "component_source": "models/components/guide_rail/scpf/model.py",
        "component_definition_primary": True,
        "native": True,
        "native_snapshot_required": True,
    },
    "guide-rail-makita": {
        "source": "models/components/guide_rail/scpf/makita.py",
        "section": "components",
        "title": "GuideRail — Makita profile",
        "tagline": "The same GuideRail component with the Makita 199141-8 profile",
        "description": "A second fixed cross-section of the generic GuideRail component. The aluminium shape comes from the Makita 199141-8 STEP reference and is calibrated to the TSO measured 182.50 × 10.28 mm envelope. The standalone CAD example uses 600 mm for compact visual inspection; Makita's referenced product length is 1500 mm.",
        "parameters": "182.50 × 10.28 mm profile; 600 mm standalone example",
        "diagram": "guide-rail",
        "stages": [
            "Select the fixed Makita cross-section at build time",
            "Create one detailed XZ Polygon2D",
            "Approximate the STEP's small round edges with short line segments",
            "Extrude symmetrically along Y to the 600 mm example length",
        ],
        "component_source": "models/components/guide_rail/scpf/model.py",
        "native": True,
        "native_snapshot_required": True,
    },
    "simple-mft": {
        "source": "models/advanced/simple_mft/scpf/model.py",
        "section": "advanced",
        "title": "Simple MFT",
        "tagline": "805 × 555 mm reusable worktop with a 9 × 7 dog-hole grid and eight native clamp slots",
        "description": "A reusable CRAFTMAKER-inspired worktop component: one 18 mm native Box, four straight 20 mm corner chamfers, 59 Ø20 dog holes on the nominal 9 × 7 / 76 mm grid with the four diagonal ring-2 positions omitted, and eight photo-measured native diagonal Slots.",
        "parameters": "805 × 555 × 18 mm; 59 × Ø20; nominal 9 × 7 at 76 mm; 8 Slots ≈104 × 24 mm",
        "diagram": "plate",
        "stages": [
            "Box — 805 × 555 × 18 mm",
            "Dog holes Sketch — one Circle seed and one native 9 × 7 rectangular pattern create 63 profiles",
            "One selective cut uses 59 profiles and leaves the four diagonal ring-2 positions at (±152, ±152) mm",
            "Clamp slots Sketch — one master Slot, one native sketch pattern and three mirrors create 8 Slots",
            "Two through-all cuts — one for dog holes and one for clamp slots",
            "Chamfer — four straight 20 × 20 mm plan-view corner cuts",
        ],
        "component_source": "models/advanced/simple_mft/scpf/model.py",
        "component_definition_primary": True,
        "native": True,
        "native_snapshot_required": True,
    },
    "simple-mft-assembly": {
        "source": "models/advanced/simple_mft/scpf/assemblies/guide_rail.py",
        "section": "advanced",
        "title": "Simple MFT assembly",
        "tagline": "Reusable Simple MFT worktop with a 1080 mm Festool-profile GuideRail",
        "description": "The first Simple MFT assembly reuses the exact worktop component and the generic GuideRail component. The rail runs along the short Y/depth direction, is centred over X=0 and rests on the parametrically shared worktop top face.",
        "parameters": "805 × 555 mm worktop; shared worktop thickness 18 mm; Festool GuideRail 1080 mm",
        "diagram": "guide-rail",
        "stages": [
            "Instantiate the reusable SimpleMFT worktop",
            "Share worktop_thickness with the worktop component",
            "Instantiate GuideRail with the Festool profile at 1080 mm",
            "Centre the 184.20 mm rail width over X=0",
            "Place the rail bottom at Z=worktop_thickness",
        ],
        "native": True,
        "native_snapshot_required": True,
    },
    "hub75-screen": {
        "source": "models/advanced/hub75_screen/scpf/model.py",
        "section": "advanced",
        "title": "BasicHub75Screen",
        "tagline": "Five shared native HUB75 occurrences with two 180° rotations",
        "description": "Five panels on the source project's 800 × 320 mm nominal grid. One rear-tapered, four-bay panel component is reused at X=−320, −160, 0, 160 and 320 mm. Columns 2 and 4 reverse direction around the assembled front-to-back axis for the rear data chain, and all occurrences stand upright in XZ. R5 corners, detailed rear reinforcements, PCB and connectors remain future phases.",
        "parameters": "Five 159.70 × 319.71 × 14.50 mm panels; X pitch 160 mm",
        "diagram": "hub75-screen",
        "stages": [
            "Create the reusable tapered HUB75 component",
            "Make six blind M3 rear bores and assign material once",
            "Ground the middle occurrence at X=0",
            "Place four copies on the 160 mm nominal grid",
            "Place native occurrences with translate, axis and angle",
            "Verify five saved native occurrences",
        ],
        "component_source": "models/components/hub75_panel/detailed/scpf/model.py",
        "native": True,
        "native_snapshot_required": True,
    },
    "hub75-wood-frame": {
        "source": "models/advanced/hub75_wood_frame/scpf/model.py",
        "section": "advanced",
        "title": "WoodenHub75Box",
        "tagline": "Parametrized 12 mm plywood box, eight brackets and one GlassStrip type",
        "description": "One clearly parametrized assembly: five lightweight HUB75 modules, 12 mm sidewalls/bottom/roof, 9 mm attached rear, 4 mm glass and four straight-mitred wooden retainers from one GlassStrip class. The roof extends 10 mm in front and 1 mm beyond the attached rear sheet. Eight printed corner brackets, two per corner, share the hole-free CornerBracket definition. The four rear brackets stop at the sidewall rear face (Y=75), before the 9 mm backboard (Y=75..84). The R4 fillets belong to the roof and bottom boards, not the glazing strips.",
        "parameters": "Outer 868 × 386 mm; 12 mm ply, 9 mm rear; roof 10/1 mm overhang; eight brackets",
        "diagram": "hub75-wood-frame",
        "stages": [
            "Define one central parameter set and the wooden component types",
            "Place five lightweight HUB75 panel occurrences on the 160 mm grid",
            "Place 12 mm sidewalls, R4 bottom and roof with 10/1 mm overhang",
            "Attach the 9 mm back board and place the 4 mm window behind the strips",
            "Create two length variants of ONE GlassStrip type and place four mitred pieces",
            "Place eight shared hole-free CornerBracket occurrences, front and rear",
            "Verify actual native positions and dimensions in SolidCraft 0.42.0",
        ],
        "native": True,
        "native_snapshot_required": True,
    },
}


SOURCES = {slug: model["source"] for slug, model in MODELS.items()}
COMMAND_SOURCES = {
    slug: model["scpc_source"]
    for slug, model in MODELS.items()
    if model.get("scpc_source")
}
COMPONENT_SOURCES = {
    slug: model["component_source"]
    for slug, model in MODELS.items()
    if model.get("component_source")
}
COMPONENT_DEFINITION_PRIMARY = frozenset(
    slug
    for slug, model in MODELS.items()
    if model.get("component_definition_primary")
)
SECTIONS = {
    key: (
        title,
        description,
        tuple(
            slug
            for slug, model in MODELS.items()
            if model["section"] == key
        ),
    )
    for key, (title, description) in SECTION_INFO.items()
}


def model_slugs(kind="scpf"):
    if kind == "scpf":
        return tuple(MODELS)
    if kind == "scpc":
        return tuple(COMMAND_SOURCES)
    if kind == "native":
        return tuple(
            slug for slug, model in MODELS.items()
            if model.get("native")
        )
    if kind == "native-snapshot-required":
        return tuple(
            slug for slug, model in MODELS.items()
            if model.get("native_snapshot_required")
        )
    raise ValueError(f"unknown model selection: {kind}")


def source_path(root, slug, language="scpf"):
    if language == "scpf":
        return Path(root) / SOURCES[slug]
    if language == "scpc":
        return Path(root) / COMMAND_SOURCES[slug]
    raise ValueError("language must be scpf or scpc")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug", nargs="?")
    parser.add_argument("language", nargs="?", choices=("scpf", "scpc"), default="scpf")
    parser.add_argument(
        "--list",
        dest="list_kind",
        choices=("scpf", "scpc", "native", "native-snapshot-required"),
    )
    parser.add_argument(
        "--count",
        dest="count_kind",
        choices=("scpf", "scpc", "native", "native-snapshot-required"),
    )
    args = parser.parse_args()

    if args.list_kind:
        print(" ".join(model_slugs(args.list_kind)))
        return
    if args.count_kind:
        print(len(model_slugs(args.count_kind)))
        return
    if not args.slug:
        parser.error("provide a model slug or --list/--count")

    table = SOURCES if args.language == "scpf" else COMMAND_SOURCES
    if args.slug not in table:
        raise SystemExit(f"Unknown {args.language} model: {args.slug}")
    print(table[args.slug])


if __name__ == "__main__":
    main()
