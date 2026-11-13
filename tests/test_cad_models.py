"""Project CAD model regression tests against installed SCPF.

Moved from lib.py.solidcraft/scpf/tests/test_models.py: these source fixtures
belong to the consumer CAD repository, not the reusable Python library.
"""
import ast
import json
import tempfile
import unittest
from pathlib import Path

from scpf.compiler import ModelError
from scpf.runner import run_script

ROOT = Path(__file__).resolve().parents[1]

class CADModelRegressions(unittest.TestCase):
    def test_model_scripts_use_plain_classes_and_explicit_returns(self):
        """No dataclass/type ceremony or implicit last geometry expression."""
        scripts = set((ROOT / "models").glob("**/scpf/model.py"))
        scripts.update(
            (ROOT / "models/advanced/hub75_wood_frame/scpf").glob("**/*.py")
        )
        scripts = sorted(scripts)
        self.assertGreaterEqual(len(scripts), 10)
        for script in scripts:
            with self.subTest(model=str(script.relative_to(ROOT))):
                module = ast.parse(script.read_text(encoding="utf-8"))
                classes = [node for node in module.body if isinstance(node, ast.ClassDef)]
                public_models = [
                    cls for cls in classes
                    if not cls.name.startswith("_")
                    and any(
                        isinstance(member, ast.FunctionDef)
                        and member.name == "build"
                        for member in cls.body
                    )
                ]
                if len(public_models) == 1:
                    root_name = public_models[0].name
                    redundant_calls = [
                        node for node in module.body
                        if isinstance(node, ast.Expr)
                        and isinstance(node.value, ast.Call)
                        and isinstance(node.value.func, ast.Name)
                        and node.value.func.id == root_name
                        and not node.value.args
                        and not node.value.keywords
                    ]
                    self.assertEqual(
                        redundant_calls,
                        [],
                        f"{script}: single-class SCPF files use the implicit root",
                    )

                for cls in classes:
                    decorators = {
                        item.id
                        for item in cls.decorator_list
                        if isinstance(item, ast.Name)
                    }
                    self.assertEqual(
                        decorators,
                        decorators & {"component", "assembly"},
                        cls.name,
                    )
                    # SCPF class parameters are simple numeric class attributes.
                    for statement in cls.body:
                        self.assertNotIsInstance(statement, ast.AnnAssign, cls.name)
                    for fn in (node for node in cls.body
                               if isinstance(node, ast.FunctionDef) and node.name == "build"):
                        self.assertIsInstance(fn.body[-1], ast.Return, cls.name)


    def test_corner_bracket_dimension_names_match_geometry(self):
        source = (
            ROOT / "models/components/corner_bracket/scpf/model.py"
        ).read_text(encoding="utf-8")
        module = ast.parse(source)
        cls = next(
            node for node in module.body
            if isinstance(node, ast.ClassDef) and node.name == "CornerBracket"
        )
        values = {
            node.targets[0].id: node.value.value
            for node in cls.body
            if isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, (int, float))
        }
        self.assertEqual(values["arm_width"], 24.0)
        self.assertEqual(values["arm_height"], 12.0)
        self.assertEqual(values["horizontal_arm_length"], 60.0)
        self.assertEqual(values["vertical_arm_length"], 60.0)
        self.assertNotIn("bracket_width", values)
        self.assertNotIn("wall_thickness", values)

    def test_corner_bracket_keeps_hub75_mounting_out_of_component(self):
        source = (
            ROOT / "models/components/corner_bracket/scpf/model.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("def anchors(", source)
        self.assertNotIn("frame_wood_thickness", source)

        assembly_source = (
            ROOT
            / "models/advanced/hub75_wood_frame/scpf/assemblies/corner_brackets.py"
        ).read_text(encoding="utf-8")
        self.assertIn("AnchorTopology(", assembly_source)
        self.assertIn(
            "self.frame_wood_thickness - self.corner_radius",
            assembly_source,
        )

    def test_hub75_corner_brackets_use_parametric_tangent_gap(self):
        commands = run_script(
            ROOT / "models/advanced/hub75_wood_frame/scpf/model.py"
        )["commands"]
        joints = [
            command["params"]
            for command in commands
            if command["command"] == "joint.create"
            and command["params"]["name"].startswith("Attach CornerBracket")
        ]
        self.assertEqual(len(joints), 8)
        self.assertTrue(all(
            joint["offset"] == "frame_wood_thickness - (corner_radius)"
            for joint in joints
        ))
        self.assertTrue(all("edge" in joint["a"] for joint in joints))
        self.assertTrue(all("corner" in joint["a"] for joint in joints))
        self.assertTrue(all("edge" in joint["b"] for joint in joints))
        self.assertTrue(all("corner" in joint["b"] for joint in joints))
        self.assertEqual(
            sum(joint["a"]["z"] == [0.0, 0.0, 1.0] for joint in joints),
            4,
        )
        self.assertEqual(
            sum(joint["a"]["z"] == [0.0, 0.0, -1.0] for joint in joints),
            4,
        )
        self.assertTrue(all(
            joint["b"]["z"] == [0.0, 0.0, -1.0]
            for joint in joints
        ))
        self.assertEqual(
            sorted(joint["angle"] for joint in joints),
            [0, 0, 0, 0, 180, 180, 180, 180],
        )
        self.assertFalse(any(
            command["command"] == "joint.origin"
            and "CornerBracket" in str(command["params"])
            for command in commands
        ))


    def test_reusable_component_sources_own_component_decorator(self):
        reusable = (
            ("models/components/corner_bracket/scpf/model.py", "CornerBracket"),
            ("models/components/hub75_panel/basic/scpf/model.py", "Hub75PanelBasic"),
            ("models/components/hub75_panel/detailed/scpf/model.py", "Hub75Panel"),
        )
        for relative, class_name in reusable:
            source = (ROOT / relative).read_text(encoding="utf-8")
            module = ast.parse(source)
            cls = next(
                node for node in module.body
                if isinstance(node, ast.ClassDef) and node.name == class_name
            )
            decorators = {
                item.id
                for item in cls.decorator_list
                if isinstance(item, ast.Name)
            }
            self.assertIn("component", decorators, relative)

        callers = (
            "models/advanced/hub75_wood_frame/scpf/assemblies/corner_brackets.py",
            "models/advanced/hub75_wood_frame/scpf/assemblies/hub75_panels.py",
            "models/advanced/hub75_screen/scpf/model.py",
        )
        for relative in callers:
            source = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("component(", source, relative)


    def test_single_joint_example_has_one_direct_face_joint(self):
        commands = run_script(
            ROOT / "examples/single-joint/scpf/model.py"
        )["commands"]

        joints = [
            command["params"]
            for command in commands
            if command["command"] == "joint.create"
        ]
        origins = [
            command
            for command in commands
            if command["command"] == "joint.origin"
        ]

        self.assertEqual(len(joints), 1)
        self.assertEqual(origins, [])
        self.assertEqual(joints[0]["type"], "rigid")
        self.assertEqual(
            joints[0]["a"],
            {"occurrence": "Base:1", "face": [40.0, 0.0, 10.0]},
        )
        self.assertEqual(
            joints[0]["b"],
            {"occurrence": "Child:1", "face": [40.0, 0.0, 10.0]},
        )
        self.assertEqual(
            commands[-1],
            {
                "command": "browser.visibility",
                "params": {"folder": "joints", "visible": False},
            },
        )


    def test_single_corner_joint_uses_edge_on_corner_reference(self):
        commands = run_script(
            ROOT / "examples/single-corner-joint/scpf/model.py"
        )["commands"]

        joints = [
            command["params"]
            for command in commands
            if command["command"] == "joint.create"
        ]
        origins = [
            command
            for command in commands
            if command["command"] == "joint.origin"
        ]

        self.assertEqual(len(joints), 1)
        self.assertEqual(origins, [])
        self.assertEqual(
            joints[0]["a"],
            {
                "occurrence": "Base:1",
                "edge": [40.0, -20.0, 40.0],
                "on": [0.0, -20.0, 40.0],
                "corner": [40.0, -20.0, 80.0],
            },
        )
        self.assertEqual(
            joints[0]["b"],
            {"occurrence": "Child:1", "face": [40.0, -20.0, 80.0]},
        )


    def test_single_custom_anchor_joint_is_inlined_without_origin(self):
        commands = run_script(
            ROOT / "examples/single-custom-anchor-joint/scpf/model.py"
        )["commands"]

        origins = [
            command["params"]
            for command in commands
            if command["command"] == "joint.origin"
        ]
        joints = [
            command["params"]
            for command in commands
            if command["command"] == "joint.create"
        ]

        self.assertEqual(origins, [])
        self.assertEqual(len(joints), 1)
        self.assertEqual(
            joints[0]["a"],
            {
                "occurrence": "Base:1",
                "edge": [40.0, -20.0, 40.0],
                "on": [0.0, -20.0, 40.0],
                "corner": [40.0, -20.0, 80.0],
            },
        )
        self.assertEqual(
            joints[0]["b"],
            {
                "occurrence": "Child:1",
                "point": [40.0, -20.0, 80.0],
                "z": [0.0, 1.0, 0.0],
                "x": [1.0, 0.0, 0.0],
            },
        )


    def test_csg_cube_matches_reviewed_native_commands(self):
        generated = run_script(ROOT / "models/basic/csg_cube/scpf/model.py")
        expected = json.loads((ROOT / "models/basic/csg_cube/scpf/reference.json").read_text())
        self.assertEqual(generated, expected)
        self.assertEqual(generated["commands"][0]["params"]["name"], "size")
        self.assertEqual(generated["commands"][1]["params"]["radius"], "size / 1.5")


    def test_plate_uses_generic_box_and_native_holes(self):
        generated = run_script(ROOT / "models/basic/plate/scpf/model.py")
        expected = json.loads((ROOT / "models/basic/plate/scpf/reference.json").read_text())
        self.assertEqual(generated, expected)
        commands = generated["commands"]
        self.assertEqual([c["params"]["name"] for c in commands[:3]],
                         ["length", "width", "thickness"])
        self.assertEqual([c["params"]["name"] for c in commands
                          if c["command"] == "sketch.create"], ["Plate footprint"])
        holes = [c["params"] for c in commands if c["command"] == "solid.hole"]
        self.assertEqual(len(holes), 4)
        self.assertEqual([c["position"] for c in holes],
                         [[-35, -15, 10], [35, -15, 10],
                          [35, 15, 10], [-35, 15, 10]])
        self.assertTrue(all(c["diameter"] == 8 for c in holes))
        self.assertTrue(all(c["targets"] == ["Plate"] for c in holes))
        self.assertTrue(all("references" not in c for c in holes))
        self.assertFalse(any(c["command"] == "solid.cylinder" for c in commands))
        self.assertEqual([c["command"] for c in commands].count("solid.fillet"), 1)


    def test_bracket_matches_corrected_native_commands(self):
        generated = run_script(ROOT / "models/basic/bracket/scpf/model.py")
        expected = json.loads(
            (ROOT / "models/basic/bracket/scpf/solidcraft.json").read_text()
        )
        self.assertEqual(generated, expected)

        original = json.loads(
            (ROOT / "models/basic/bracket/source/bracket.json").read_text()
        )
        # SCPF intentionally improves on the literal source profile: points
        # controlled by thickness remain native parameter expressions instead
        # of freezing the default 6 mm into the sketch. The extrusion still
        # follows the same negative-XZ construction intent.
        self.assertEqual(
            generated["commands"][2]["params"],
            original["commands"][2]["params"],
        )
        self.assertEqual(
            generated["commands"][4:6],
            original["commands"][4:6],
        )
        self.assertEqual(
            generated["commands"][3]["params"]["points"],
            [
                [0, 0], [40, 0], [40, "thickness"],
                ["thickness", "thickness"],
                ["thickness", 30], [0, 30],
            ],
        )
        self.assertEqual(generated["commands"][6]["params"]["body"], "Bracket")
        self.assertEqual([c["command"] for c in generated["commands"][7:]],
                         ["solid.hole", "solid.hole"])
        self.assertEqual([c["params"]["position"]
                          for c in generated["commands"][7:]],
                         [[25, -15, 0], [25, -45, 0]])
        self.assertEqual([c["params"]["depth"]
                          for c in generated["commands"][7:]],
                         ["thickness", "thickness"])
        self.assertEqual(generated["commands"][6]["params"]["edges"],
                         [[40, -30, -6]])


    def test_bracket_width_and_thickness_override(self):
        with tempfile.TemporaryDirectory() as directory:
            source = (ROOT / "models/basic/bracket/scpf/model.py").read_text()
            file = Path(directory) / "model.py"
            file.write_text(source + "\nBracket(70, 8)\n")
            generated = run_script(file)
        self.assertEqual(generated["commands"][0]["params"]["expression"], "70")
        self.assertEqual(generated["commands"][1]["params"]["expression"], "8")
        # The override changes the parameter value, while the sketch keeps
        # referring to the parameter name for later native edits.
        self.assertEqual(
            generated["commands"][3]["params"]["points"][2],
            [40, "thickness"],
        )
        self.assertEqual(generated["commands"][6]["params"]["edges"], [[40, -35, -8]])


    def test_sample_plate_preserves_original_sketch_and_feature_names(self):
        commands = run_script(ROOT / "models/basic/sample_plate/scpf/model.py")["commands"]
        self.assertEqual(
            [c["params"]["name"] for c in commands if c["command"] == "sketch.create"],
            ["Base", "Holes", "Boss", "Bore"],
        )
        self.assertEqual(
            [c["command"] for c in commands
             if c["command"] in ("solid.hole", "solid.cylinder")],
            [],
        )
        self.assertEqual(
            [c["params"]["operation"] for c in commands
             if c["command"] == "solid.extrude" and "operation" in c["params"]],
            ["cut", "join", "cut"],
        )
        self.assertEqual(
            [c["params"]["name"] for c in commands
             if c["command"] == "solid.extrude" and "operation" in c["params"]],
            ["Holes", "Boss", "Bore"],
        )
        self.assertEqual(
            [c["params"]["center"] for c in commands
             if c["command"] == "sketch.circle.center"],
            [[12, 25], [68, 25], [40, 25], [40, 25]],
        )
        self.assertEqual(
            [c["params"]["offset"] for c in commands
             if c["command"] == "sketch.create" and "offset" in c["params"]],
            ["thickness", "thickness + 14 mm"],
        )


    def test_sample_plate_parameter_override_preserves_sketch_centres(self):
        with tempfile.TemporaryDirectory() as directory:
            source = (ROOT / "models/basic/sample_plate/scpf/model.py").read_text()
            script = Path(directory) / "model.py"
            script.write_text(
                source + "\nSamplePlate(width=100, depth=60, thickness=10)\n"
            )
            commands = run_script(script)["commands"]
        self.assertEqual([c["params"]["expression"] for c in commands[:3]],
                         ["100", "60", "10"])
        self.assertEqual(
            [c["params"]["center"] for c in commands
             if c["command"] == "sketch.circle.center"],
            [[12, 30], [88, 30], [50, 30], [50, 30]],
        )
        self.assertFalse(any(c["command"] == "solid.hole" for c in commands))


    def test_sample_plate_uses_edge_enum(self):
        source = (ROOT / "models/basic/sample_plate/scpf/model.py").read_text()
        self.assertIn("edges=Edges.VERTICAL", source)
        run_script(ROOT / "models/basic/sample_plate/scpf/model.py")


    def test_plastic_enclosure_compiles_to_sketch_base_and_native_plastic_features(self):
        commands = run_script(
            ROOT / "models/basic/plastic_enclosure/scpf/model.py"
        )["commands"]
        feature_commands = [c for c in commands
                            if c["command"] != "parameters.add"]
        self.assertEqual(
            [c["command"] for c in feature_commands],
            [
                "sketch.create",
                "sketch.rectangle.two_point",
                "sketch.finish",
                "solid.extrude",
                "solid.shell",
                "plastic.lip",
                "plastic.snap_fit",
                "plastic.boss",
                "plastic.boss",
                "plastic.rest",
            ],
        )
        self.assertEqual(feature_commands[0]["params"]["name"], "Enclosure footprint")
        self.assertEqual(feature_commands[3]["params"]["body_name"], "Enclosure")
        self.assertTrue(all(
            c["params"].get("body") == "Enclosure"
            for c in feature_commands[4:]
        ))
        self.assertEqual(feature_commands[4]["params"]["faces"], [[0, 0, 30]])
        self.assertEqual(feature_commands[5]["params"]["face"], [-39, 0, 30])
        self.assertEqual(feature_commands[6]["params"]["position"], [0, 19, 2])
        self.assertEqual(feature_commands[6]["params"]["hook"], [0, -1, 0])
        self.assertEqual(
            [feature_commands[7]["params"]["position"],
             feature_commands[8]["params"]["position"]],
            [[-30, -15, 2], [30, 15, 2]],
        )
        self.assertEqual(feature_commands[9]["params"]["position"], [0, 0, 2])
        self.assertEqual(feature_commands[9]["params"]["length"], 24)


    def test_plastic_enclosure_pi_video_feature_sequence(self):
        commands = run_script(
            ROOT / "models/basic/plastic_enclosure_pi/scpf/model.py"
        )["commands"]
        self.assertEqual(
            [c["params"]["name"] for c in commands
             if c["command"] == "parameters.add"],
            ["board_w", "board_d", "height", "wall"],
        )
        features = [c for c in commands if c["command"] != "parameters.add"]
        self.assertEqual(
            [c["command"] for c in features],
            ["sketch.create", "sketch.rectangle.two_point", "sketch.finish",
             "solid.extrude", "solid.fillet", "solid.shell", "solid.fillet",
             "plastic.boss", "plastic.boss", "plastic.boss", "plastic.boss",
             "sketch.create", "sketch.rectangle.two_point",
             "sketch.rectangle.two_point", "sketch.rectangle.two_point",
             "sketch.finish", "solid.extrude",
             "sketch.create", "sketch.rectangle.two_point",
             "sketch.finish", "solid.extrude",
             "sketch.create", "sketch.rectangle.two_point",
             "sketch.rectangle.two_point", "sketch.rectangle.two_point",
             "sketch.rectangle.two_point", "sketch.rectangle.two_point",
             "sketch.finish", "solid.extrude",
             "sketch.create", "sketch.text", "sketch.finish", "solid.extrude",
             "material.create", "material.assign"],
        )
        self.assertIn("board_w", str(features[1]["params"]["p0"][0]))
        self.assertIn("board_d", str(features[1]["params"]["p1"][1]))
        self.assertEqual(features[4]["params"]["radius"], 5.0)
        self.assertEqual(features[6]["params"]["radius"], 1.0)
        bosses = [c["params"] for c in features if c["command"] == "plastic.boss"]
        self.assertEqual(
            [p["position"] for p in bosses],
            [[-39, -24.5, 2], [19, -24.5, 2],
             [-39, 24.5, 2], [19, 24.5, 2]],
        )
        self.assertTrue(all(p["hole_diameter"] == 2.5 for p in bosses))
        self.assertEqual(
            [c["params"]["name"] for c in features
             if c["command"] == "sketch.create"],
            ["PlasticEnclosurePi footprint", "Pi ports",
             "USB and Ethernet", "Floor vents", "Pi 4 engraving"],
        )
        cuts = [c for c in features if c["command"] == "solid.extrude"
                and c["params"].get("operation") == "cut"]
        self.assertEqual(len(cuts), 4)
        self.assertEqual([c["params"]["direction"] for c in cuts],
                         ["negative", "negative", "negative", "negative"])
        self.assertEqual(
            [c["command"] for c in features[-6:]],
            ["sketch.create", "sketch.text", "sketch.finish", "solid.extrude",
             "material.create", "material.assign"],
        )
        self.assertEqual(features[-5]["params"]["text"], "Pi 4")
        self.assertEqual(features[-2]["params"]["density_g_cm3"], 1.27)
        self.assertEqual(features[-1]["params"]["material"], "PETG")



if __name__ == "__main__":
    unittest.main()
