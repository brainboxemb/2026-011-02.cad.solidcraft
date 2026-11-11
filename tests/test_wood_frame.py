"""Fast wooden display prototype: separate from the advanced HUB75 module."""
import unittest
from pathlib import Path

from scpf.runner import run_script
from models.components.hub75_basic import Hub75PanelBasic
from models.components.hub75 import Hub75Panel
from models.components.wood_box import SideWall, BottomBoard, RoofBoard, BackBoard, Window, CornerRailConcept

ROOT = Path(__file__).resolve().parents[1]


class WoodenFrameTests(unittest.TestCase):
    def test_measured_basic_and_advanced_panel_envelopes_agree(self):
        b, a = Hub75PanelBasic(), Hub75Panel()
        self.assertEqual((b.width,b.height,b.depth),(a.width,a.height,a.depth))
        self.assertEqual((b.width,b.height,b.depth),(159.70,319.71,14.50))

    def test_wood_dimensions_follow_prototype_reference(self):
        self.assertEqual((SideWall.thickness, SideWall.height, SideWall.depth),(15,362,100))
        self.assertEqual((BottomBoard.width, BottomBoard.thickness, BottomBoard.depth),(874,15,100))
        self.assertEqual((RoofBoard.width, RoofBoard.thickness, RoofBoard.depth),(874,15,124))
        self.assertEqual((BackBoard.width, BackBoard.height, BackBoard.thickness),(874,377,9))
        self.assertEqual((Window.width,Window.height,Window.thickness),(840,360,4))
        self.assertEqual(CornerRailConcept.arm_length,100)

    def test_fast_box_has_only_basic_native_features(self):
        result = run_script(ROOT / "models/hub75-wood-frame/scpf/model.py")
        commands = result["commands"]
        kinds = [item["command"] for item in commands]
        defs = [item["params"]["name"] for item in commands if item["command"]=="component.create"]
        self.assertEqual(len(defs),7)
        self.assertEqual(len(set(defs)),7)
        self.assertIn("Hub75PanelBasic",defs)
        self.assertIn("CornerRailConcept",defs)
        self.assertEqual(kinds.count("occurrence.copy"),8) # 4 panels, 1 side, 3 corner rails
        self.assertEqual(kinds.count("solid.loft"),0)
        self.assertEqual(kinds.count("solid.hole"),0)
        self.assertEqual(kinds.count("solid.fillet"),0)
        self.assertEqual(kinds.count("sketch.create"),7)
        self.assertEqual(kinds.count("material.assign"),7)
        self.assertEqual(kinds.count("occurrence.move"),11) # 2 panel rotations, 6 initial part poses, 3 rotated corners
        self.assertEqual(kinds.count("solid.extrude"),7)

    def test_wooden_box_has_real_z_up_geometry(self):
        commands = run_script(ROOT / "models/hub75-wood-frame/scpf/model.py")["commands"]

        def component(name):
            start = next(i for i, command in enumerate(commands)
                         if command["command"] == "component.create"
                         and command["params"]["name"] == name)
            end = next(i for i in range(start + 1, len(commands))
                       if commands[i]["command"] == "component.activate"
                       and commands[i]["params"]["component"] == "root")
            return commands[start:end]

        # The thin front-to-back depth belongs in the XY sketch footprint;
        # the 319.71 mm height is the actual Z-up extrude distance.
        panel = component("Hub75PanelBasic")
        footprint = next(c["params"] for c in panel
                         if c["command"] == "sketch.rectangle.two_point")
        self.assertIn("Hub75PanelBasic_width", str(footprint))
        self.assertIn("Hub75PanelBasic_depth", str(footprint))
        self.assertNotIn("Hub75PanelBasic_height", str(footprint))
        self.assertEqual(next(c["params"]["distance"] for c in panel
                              if c["command"] == "solid.extrude"),
                         "Hub75PanelBasic_height")

        for name in ("SideWall", "BackBoard", "Window"):
            part = component(name)
            self.assertEqual(next(c["params"]["distance"] for c in part
                                  if c["command"] == "solid.extrude"),
                             name + "_height")

        corner = component("CornerRailConcept")
        self.assertEqual(
            next(c["params"]["plane"] for c in corner
                 if c["command"] == "sketch.create"), "XZ")

        placements = [c["params"] for c in commands
                      if c["command"] == "occurrence.move"]
        panel_moves = [c for c in placements
                       if c["occurrence"].startswith("Hub75PanelBasic:")]
        self.assertEqual(len(panel_moves), 3)
        self.assertEqual(panel_moves[0]["translate"], [0.0, 7.25, 21.145])
        rotations = [p["to"] for p in panel_moves[1:]]
        self.assertEqual([p["angle"] for p in rotations],
                         ["180 deg", "180 deg"])
        self.assertTrue(all(p["axis"] == [0.0, 1.0, 0.0] for p in rotations))
        self.assertEqual([round(p["position"][2], 3) for p in rotations],
                         [340.855, 340.855])

        corners = [c for c in placements
                   if c["occurrence"].startswith("CornerRailConcept:")]
        self.assertEqual(len(corners), 4)
        self.assertEqual(corners[0]["translate"], [-437.0, 75.0, -15.0])
        self.assertEqual([c["to"]["angle"] for c in corners[1:]],
                         ["-90 deg", "180 deg", "90 deg"])
        self.assertTrue(all(c["to"]["axis"] == [0.0, 1.0, 0.0]
                            for c in corners[1:]))

    def test_advanced_panel_retains_bays_and_blind_bores(self):
        commands = run_script(ROOT / "models/hub75-panel/scpf/model.py")["commands"]
        kinds = [c["command"] for c in commands]
        self.assertEqual(kinds.count("solid.loft"),1)
        self.assertEqual(kinds.count("solid.hole"),6)
        self.assertIn("Rear electronics bays",
                      [c["params"]["name"] for c in commands
                       if c["command"]=="sketch.create"])


if __name__=="__main__":
    unittest.main()
