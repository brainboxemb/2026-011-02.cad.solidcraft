from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_model_build.runtime import _export_drawings, _export_stl, _snapshot


class SnapshotRuntimeTests(unittest.TestCase):
    @patch("cad_model_build.runtime.subprocess.run")
    def test_primary_snapshot_uses_solidcraft_default_camera(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_text("model", encoding="utf-8")
            target = root / "model.png"

            def fake_run(command, **kwargs):
                Path(command[command.index("--out") + 1]).write_bytes(b"png")

            run.side_effect = fake_run
            _snapshot(saved, target, None)

            command = run.call_args.args[0]
            self.assertNotIn("--camera", command)

    @patch("cad_model_build.runtime.subprocess.run")
    def test_primary_snapshot_can_define_camera(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_text("model", encoding="utf-8")
            target = root / "model.png"

            def fake_run(command, **kwargs):
                Path(command[command.index("--out") + 1]).write_bytes(b"png")

            run.side_effect = fake_run
            _snapshot(saved, target, {"yaw": -0.4})

            command = run.call_args.args[0]
            self.assertIn("--camera", command)

    @patch("cad_model_build.runtime.subprocess.run")
    def test_additional_snapshot_can_define_camera(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_text("model", encoding="utf-8")
            target = root / "top.png"

            def fake_run(command, **kwargs):
                Path(command[command.index("--out") + 1]).write_bytes(b"png")

            run.side_effect = fake_run
            _snapshot(saved, target, {"pitch": -1.55})

            command = run.call_args.args[0]
            self.assertIn("--camera", command)


    @patch("cad_model_build.runtime.subprocess.run")
    def test_stl_export_uses_adapter_default_when_quality_is_unspecified(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_bytes(b"sc")
            target = root / "model.stl"

            def fake_run(command, **kwargs):
                target.write_bytes(b"solid")

            run.side_effect = fake_run
            _export_stl(
                saved=saved,
                target=target,
                artifact_options={},
            )

            command = run.call_args.args[0]
            self.assertNotIn("--quality", command)

    @patch("cad_model_build.runtime.subprocess.run")
    def test_stl_export_maps_explicit_quality_to_solidcraft(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_bytes(b"sc")
            target = root / "model.stl"

            def fake_run(command, **kwargs):
                target.write_bytes(b"solid")

            run.side_effect = fake_run
            _export_stl(
                saved=saved,
                target=target,
                artifact_options={"stl": {"quality": "fine"}},
            )

            command = run.call_args.args[0]
            quality = command.index("--quality")
            self.assertEqual(command[quality + 1], "fine")

    @patch("cad_model_build.runtime.subprocess.run")
    def test_drawing_export_uses_native_solidcraft_pdf(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "models/sample-plate/model.sc"
            saved.parent.mkdir(parents=True)
            saved.write_bytes(b"sc")
            work = root / "work"
            work.mkdir()
            row = {
                "id": "sample-plate",
                "drawings": [
                    {
                        "name": "SamplePlate",
                        "drawing": "$drawing_1",
                        "sheet": "$drawing_1_sheet",
                        "orientation": "$drawing_1_orientation",
                        "path": "models/sample-plate/drawings/SamplePlate.pdf",
                        "preview": "models/sample-plate/drawings/SamplePlate.png",
                        "inspect": "models/sample-plate/drawings/SamplePlate.json",
                    }
                ],
            }
            document = {
                "artifacts": {
                    "drawings": [
                        {
                            "name": "SamplePlate",
                            "drawing": "$drawing_1",
                            "sheet": "$drawing_1_sheet",
                            "orientation": "$drawing_1_orientation",
                            "pdf": "drawings/SamplePlate.pdf",
                            "png": "drawings/SamplePlate.png",
                            "inspect": "drawings/SamplePlate.json",
                            "expected": {},
                        }
                    ]
                }
            }

            def fake_run(command, **kwargs):
                script = Path(command[2])
                payload = __import__("json").loads(script.read_text())
                for export in (
                    item for item in payload["commands"]
                    if item["command"] == "drawing.export"
                ):
                    target = Path(export["params"]["path"])
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if export["params"]["format"] == "pdf":
                        target.write_bytes(b"%PDF-1.7\n")
                    else:
                        target.write_bytes(b"\x89PNG\r\n\x1a\npreview")
                return None

            run.side_effect = fake_run
            produced = _export_drawings(
                document=document,
                row=row,
                variables={
                    "$drawing_1": "D1",
                    "$drawing_1_sheet": "S1",
                    "$drawing_1_orientation": "landscape",
                },
                saved=saved,
                output_root=root,
                work_dir=work,
                replay_results=[{
                    "name": "SamplePlate",
                    "sheets": [],
                    "properties": {},
                }],
            )

            self.assertEqual(
                produced,
                (
                    root / "models/sample-plate/drawings/SamplePlate.pdf",
                    root / "models/sample-plate/drawings/SamplePlate.png",
                    root / "models/sample-plate/drawings/SamplePlate.json",
                ),
            )
            command = run.call_args.args[0]
            self.assertIn("--in", command)
            self.assertIn(str(saved), command)
            script = __import__("json").loads(Path(command[2]).read_text())
            self.assertEqual(
                script["commands"][0],
                {"command": "drawing.open", "params": {"drawing": "D1"}},
            )
            exports = [
                item for item in script["commands"]
                if item["command"] == "drawing.export"
            ]
            self.assertEqual(
                [item["params"]["format"] for item in exports],
                ["pdf", "png"],
            )
            self.assertEqual(exports[1]["params"]["dpi"], 144)

    @patch("cad_model_build.runtime.subprocess.run")
    def test_drawing_export_rejects_non_pdf_output(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            saved = root / "model.sc"
            saved.write_bytes(b"sc")
            work = root / "work"
            work.mkdir()
            row = {
                "id": "part",
                "drawings": [
                    {
                        "name": "Part",
                        "drawing": "$drawing_1",
                        "path": "models/part/drawings/Part.pdf",
                    }
                ],
            }
            document = {
                "artifacts": {
                    "drawings": [
                        {
                            "name": "Part",
                            "drawing": "$drawing_1",
                            "pdf": "drawings/Part.pdf",
                        }
                    ]
                }
            }

            def fake_run(command, **kwargs):
                payload = __import__("json").loads(Path(command[2]).read_text())
                export = next(
                    item for item in payload["commands"]
                    if item["command"] == "drawing.export"
                )
                target = Path(export["params"]["path"])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"not-a-pdf")

            run.side_effect = fake_run
            with self.assertRaisesRegex(RuntimeError, "not a PDF"):
                _export_drawings(
                    document=document,
                    row=row,
                    variables={"$drawing_1": "D1"},
                    saved=saved,
                    output_root=root,
                    work_dir=work,
                    replay_results=[],
                )

if __name__ == "__main__":
    unittest.main()
