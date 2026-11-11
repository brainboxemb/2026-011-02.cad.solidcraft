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
