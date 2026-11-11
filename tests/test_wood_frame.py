"""Regressions for the upright wooden HUB75 frame and native groups."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'models/advanced/hub75-wood-frame/scpf'))
import unittest
from scpf.runner import run_script
from components.hub75_basic import Hub75PanelBasic
from components.hub75 import Hub75Panel
from components.corner_bracket import CornerBracket
from hub75_wood_frame.parts.wood import (
    SideWall, BottomBoard, RoofBoard, BackBoard, Window,
    GlassSideStrip, GlassCrossStrip,
)
ROOT = Path(__file__).resolve().parents[1]
WOOD = ROOT / "models/advanced/hub75-wood-frame/scpf/model.py"


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
        self.assertEqual((GlassCrossStrip.length,GlassCrossStrip.depth,GlassCrossStrip.thickness), (844,15,15))

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

    def test_basic_panels_have_independent_native_positions(self):
        """Five copies must be placed separately, never moved cumulatively."""
        commands = actions()
        copies = [c["params"] for c in commands
                  if c["command"] == "occurrence.copy"
                  and c["params"]["component"] == "Hub75PanelBasic"]
        moves = [c["params"] for c in commands
                 if c["command"] == "occurrence.move"
                 and c["params"]["occurrence"].startswith("Hub75PanelBasic:")]
        self.assertEqual(copies, [{"component": "Hub75PanelBasic"}] * 4)
        self.assertEqual(len(moves), 5)
        self.assertEqual(sorted(round(m["translate"][0], 3) for m in moves),
                         [-320., -160., 0., 160., 320.])
        self.assertTrue(all([round(x, 3) for x in m["translate"][1:]]
                            == [7.25, 21.145] for m in moves))
        self.assertTrue(all("matrix" not in m and "to" not in m for m in moves))

    def test_copy_then_place_is_used_for_all_shared_components(self):
        """No inherited native offsets, no special-case inverse matrices."""
        commands = actions()
        names = ("SideWall", "GlassSideStrip", "GlassCrossStrip", "CornerBracket")
        for name in names:
            copies = [(i, c["params"]) for i, c in enumerate(commands)
                      if c["command"] == "occurrence.copy"
                      and c["params"]["component"] == name]
            moves = [(i, c["params"]) for i, c in enumerate(commands)
                     if c["command"] == "occurrence.move"
                     and c["params"]["occurrence"].startswith(name + ":")]
            self.assertTrue(copies, name)
            self.assertTrue(moves, name)
            self.assertLess(max(i for i, _ in copies),
                            min(i for i, _ in moves), name)
            self.assertTrue(all(p == {"component": name} for _, p in copies))
        def placement(name):
            return [c["params"]["translate"] for c in commands
                    if c["command"] == "occurrence.move"
                    and c["params"]["occurrence"].startswith(name + ":")]
        self.assertEqual([p[0] for p in placement("SideWall")],
                         [-429.5, 429.5])
        self.assertEqual([p[0] for p in placement("GlassSideStrip")],
                         [-422.0, 422.0])
        self.assertEqual([p[2] for p in placement("GlassCrossStrip")],
                         [0.0, 362.0])

    def test_glass_frame_is_mitred_rounded_and_in_front(self):
        from math import sqrt
        from hub75_wood_frame.parts.wood import (
            _rounded_side_profile, _rounded_cross_profile,
        )
        radius = CornerBracket.inside_corner_radius
        d = radius*(1-1/sqrt(2))
        side = _rounded_side_profile(15,362,radius)
        cross = _rounded_cross_profile(844,15,radius)
        def has_point(points,x,z):
            return any(abs(px-x)<1e-6 and abs(pz-z)<1e-6
                       for px,pz in points)
        self.assertEqual(radius, 4.0)
        self.assertTrue(has_point(side,d,d))
        self.assertTrue(has_point(side,15,15))
        self.assertTrue(has_point(cross,-422+d,d))
        self.assertTrue(has_point(cross,-407,15))
        self.assertTrue(has_point(side, d,362-d))
        # Each bar is symmetrical through Y=-25.5, covering -33..-18:
        # it lies before the glass whose front is at -18.
        places=[c["params"] for c in actions()
                if c["command"]=="occurrence.move"
                and c["params"]["occurrence"] in
                ("GlassSideStrip:1","GlassCrossStrip:1")]
        self.assertEqual(len(places),2)
        self.assertEqual(places[0]["translate"],[-422.0,-25.5,0.0])
        self.assertEqual(places[1]["translate"],[0.0,-25.5,0.0])
        for part in (GlassSideStrip,GlassCrossStrip):
            self.assertEqual(part.corner_radius,radius)

    def test_glazing_strips_have_different_finishes_from_box_wood(self):
        """Three readable finishes identify the correct manufactured parts."""
        materials = {
            c["params"]["name"]: c["params"]["color"]
            for c in actions() if c["command"] == "material.create"
        }
        side = materials["LIGHTPLY glazing side strip"]
        cross = materials["LIGHTPLY glazing cross strip"]
        box = materials["LIGHTPLY side wall"]
        self.assertEqual(side, "#A9793E")
        self.assertEqual(cross, "#E3BF80")
        self.assertEqual(box, "#CBA36B")
        self.assertEqual(len({side, cross, box}), 3)

    def test_glazing_uses_native_mirroring_not_duplicate_geometry(self):
        """The opposite strips reuse the same native component definition."""
        commands = actions()
        copies = [c for c in commands if c["command"] == "occurrence.copy"
                  and c["params"]["component"] in
                  ("GlassSideStrip", "GlassCrossStrip")]
        self.assertEqual(len(copies), 2)
        self.assertTrue(all(c["params"].get("translate") is None for c in copies))
        placements = {
            c["params"]["occurrence"]: c["params"]
            for c in commands if c["command"] == "occurrence.move"
            and c["params"]["occurrence"].startswith(
                ("GlassSideStrip:", "GlassCrossStrip:")
            )
        }
        self.assertEqual(len(placements), 4)
        self.assertEqual(placements["GlassSideStrip:1"]["translate"],
                         [-422., -25.5, 0.])
        self.assertEqual(placements["GlassSideStrip:2"]["translate"],
                         [422., -25.5, 0.])
        self.assertEqual(placements["GlassCrossStrip:1"]["translate"],
                         [0., -25.5, 0.])
        self.assertEqual(placements["GlassCrossStrip:2"]["translate"],
                         [0., -25.5, 362.])
        self.assertEqual(placements["GlassSideStrip:2"]["axis"],
                         [0., 0., 1.])
        self.assertEqual(placements["GlassCrossStrip:2"]["axis"],
                         [1., 0., 0.])
        self.assertEqual(placements["GlassSideStrip:2"]["angle"], "180 deg")
        self.assertEqual(placements["GlassCrossStrip:2"]["angle"], "180 deg")

    def test_back_board_ends_below_roof(self):
        commands=actions()
        back=next(c["params"] for c in commands if
                  c["command"]=="occurrence.move" and
                  c["params"]["occurrence"]=="BackBoard:1")
        self.assertEqual(back["translate"],[0.0,79.5,-15.0])
        # BackBoard height 377: -15+377 = 362, roof starts at 362.
        self.assertEqual(back["translate"][2]+BackBoard.height,362.0)

    def test_roof_and_corner_bracket_are_editable_without_holes(self):
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
        # No native mounting holes in ANY corner-bracket occurrence.
        self.assertEqual(len(features("CornerBracket","solid.hole")),0)
        self.assertFalse(any(c["command"] == "solid.hole" and
                             "CornerBracket" in str(c["params"])
                             for c in commands))
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
        # SolidCraft handles each rotation directly; never emit matrices.
        for pose, axis in zip(placements[1:],
                              ([0., 0., 1.], [1., 0., 0.], [0., 1., 0.])):
            self.assertEqual(pose["axis"], axis)
            self.assertEqual(pose["angle"], "180 deg")
            self.assertNotIn("matrix", pose)
            self.assertNotIn("to", pose)
        self.assertEqual([(p["translate"][0], p["translate"][2])
                          for p in placements[1:]],
                         [(437.0, 377.0), (-437.0, -15.0),
                          (437.0, -15.0)])

    def test_advanced_panel_still_has_rear_bays_and_blind_holes(self):
        commands=run_script(ROOT/"models/component-examples/hub75-panel/scpf/model.py")["commands"]
        self.assertEqual(sum(c["command"]=="solid.loft" for c in commands),1)
        self.assertEqual(sum(c["command"]=="solid.hole" for c in commands),6)
        self.assertIn("Rear electronics bays",
                      [c["params"]["name"] for c in commands if c["command"]=="sketch.create"])

if __name__=="__main__":
    unittest.main()
