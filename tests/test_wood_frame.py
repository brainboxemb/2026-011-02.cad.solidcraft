"""Regressions for the upright wooden HUB75 frame and native groups."""
from pathlib import Path
import unittest
from scpf.runner import run_script
from components.hub75_basic import Hub75PanelBasic
from components.hub75 import Hub75Panel
from components.corner_bracket import CornerBracket
from models.advanced.hub75_wood_frame.parts.wood import (
    SideWall, BottomBoard, RoofBoard, BackBoard, Window,
    GlassSideStrip, GlassCrossStrip,
)
ROOT = Path(__file__).resolve().parents[1]
WOOD = ROOT / "models/advanced/hub75_wood_frame/scpf/model.py"


def actions():
    return run_script(WOOD)["commands"]


class WoodenFrameTests(unittest.TestCase):
    def test_basic_and_advanced_panels_share_envelope(self):
        basic, detail = Hub75PanelBasic(), Hub75Panel()
        self.assertEqual((basic.width,basic.height,basic.depth),
                         (detail.width,detail.height,detail.depth))
        self.assertEqual((basic.width,basic.height,basic.depth), (159.70,319.71,14.50))

    def test_measured_parts(self):
        self.assertEqual((SideWall.thickness, SideWall.height, SideWall.depth), (15,362,100))
        self.assertEqual((BottomBoard.width,BottomBoard.depth,BottomBoard.thickness), (874,100,15))
        self.assertEqual((RoofBoard.width,RoofBoard.depth,RoofBoard.thickness), (874,124,15))
        self.assertEqual((BackBoard.width,BackBoard.height,BackBoard.thickness), (874,377,9))
        self.assertEqual((Window.width,Window.height,Window.thickness), (840,360,4))
        self.assertEqual((GlassSideStrip.width,GlassSideStrip.depth,GlassSideStrip.height), (15,15,362))
        self.assertEqual((GlassCrossStrip.length,GlassCrossStrip.depth,GlassCrossStrip.thickness), (814,15,15))

    def test_four_real_native_groups(self):
        commands=actions()
        created={c["params"]["name"]:c["params"] for c in commands
                 if c["command"]=="component.create"}
        groups={
            "HUB75Panels":("Hub75PanelBasic",),
            "WoodBoxFrame":("SideWall","BottomBoard","RoofBoard","BackBoard"),
            "WoodGlassFrame":("GlassSideStrip","GlassCrossStrip"),
            "CornerBrackets":("CornerBracket",),
        }
        for group, members in groups.items():
            self.assertFalse(created[group]["activate"])
            for member in members:
                self.assertEqual(created[member]["parent"],group)
        self.assertNotIn("parent",created["Window"])
        self.assertEqual(len(created),13)
        copies=[c["params"] for c in commands if c["command"]=="occurrence.copy"]
        for name,count in (("Hub75PanelBasic",4),("SideWall",1),
                           ("GlassSideStrip",1),("GlassCrossStrip",1),("CornerBracket",3)):
            self.assertEqual(sum(c["component"]==name for c in copies),count)

    def test_uniform_panel_positions_without_native_rotation(self):
        commands=actions()
        panel_moves=[c["params"] for c in commands if c["command"]=="occurrence.move"
                     and c["params"]["occurrence"].startswith("Hub75PanelBasic:")]
        self.assertEqual(len(panel_moves),1)
        self.assertNotIn("to",panel_moves[0])
        self.assertEqual([round(v,3) for v in panel_moves[0]["translate"]],
                         [0.0,7.25,21.145])
        copies=[c["params"] for c in commands if c["command"]=="occurrence.copy"
                and c["params"]["component"]=="Hub75PanelBasic"]
        self.assertEqual(sorted(c["translate"][0] for c in copies),
                         [-320.0,-160.0,160.0,320.0])
        for c in copies:
            self.assertEqual([round(x,3) for x in c["translate"][1:]],
                             [7.25,21.145])

    def test_roof_is_horizontal_and_corner_bracket_has_four_holes(self):
        commands=actions()
        def features(name,operation):
            start=next(i for i,c in enumerate(commands)
                       if c["command"]=="component.create"
                       and c["params"]["name"]==name)
            end=next(i for i in range(start+1,len(commands))
                     if commands[i]["command"]=="component.activate"
                     and commands[i]["params"]["component"]=="root")
            return [c["params"] for c in commands[start:end]
                    if c["command"]==operation]
        self.assertEqual(features("RoofBoard","solid.extrude")[0]["distance"],
                         "RoofBoard_thickness")
        self.assertEqual(features("Hub75PanelBasic","solid.extrude")[0]["distance"],
                         "Hub75PanelBasic_height")
        self.assertEqual(len(features("CornerBracket","solid.hole")),4)
        self.assertEqual(len(features("CornerBracket","solid.fillet")),1)
        self.assertEqual(len(features("CornerBracket","solid.chamfer")),3)
        self.assertEqual(CornerBracket.bracket_width,24)
        self.assertFalse(any(c["params"].get("name")=="CornerRailConcept"
                             for c in commands))

    def test_corner_brackets_cover_outside_wood_surfaces(self):
        placements=[c["params"] for c in actions()
                    if c["command"]=="occurrence.move"
                    and c["params"]["occurrence"].startswith("CornerBracket:")]
        self.assertEqual(len(placements),4)
        self.assertEqual(placements[0]["translate"],[-437.0,-13.0,377.0])
        rotated=[v["to"] for v in placements[1:]]
        self.assertEqual([v["angle"] for v in rotated],["180 deg"]*3)
        self.assertEqual([v["axis"] for v in rotated],
                         [[0.0,0.0,1.0],[1.0,0.0,0.0],[0.0,1.0,0.0]])
        self.assertEqual([(v["position"][0],v["position"][2]) for v in rotated],
                         [(437.0,377.0),(-437.0,-15.0),(437.0,-15.0)])

    def test_advanced_panel_still_has_rear_bays_and_blind_holes(self):
        commands=run_script(ROOT/"models/component-examples/hub75-panel/scpf/model.py")["commands"]
        self.assertEqual(sum(c["command"]=="solid.loft" for c in commands),1)
        self.assertEqual(sum(c["command"]=="solid.hole" for c in commands),6)
        self.assertIn("Rear electronics bays",
                      [c["params"]["name"] for c in commands if c["command"]=="sketch.create"])

if __name__=="__main__":
    unittest.main()
