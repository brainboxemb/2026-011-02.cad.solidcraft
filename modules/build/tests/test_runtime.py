from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_model_build.runtime import _export_drawings, _snapshot


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
                        "path": "models/sample-plate/drawings/SamplePlate.pdf",
                        "preview": "models/sample-plate/drawings/SamplePlate.png",
                    }
                ],
            }
            document = {
                "artifacts": {
                    "drawings": [
                        {
                            "name": "SamplePlate",
                            "drawing": "$drawing_1",
                            "pdf": "drawings/SamplePlate.pdf",
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
                    if export["params"]["format"] == "pdf":
                        target.write_bytes(b"%PDF-1.7\n")
                    elif export["params"]["format"] == "png":
                        target.write_bytes(b"\x89PNG\r\n\x1a\npreview")
                return None

            run.side_effect = fake_run
            produced = _export_drawings(
                document=document,
                row=row,
                variables={"$drawing_1": "D1", "$drawing_1_sheet": "S1"},
                saved=saved,
                output_root=root,
                work_dir=work,
            )

            self.assertEqual(
                produced,
                (
                    root / "models/sample-plate/drawings/SamplePlate.pdf",
                    root / "models/sample-plate/drawings/SamplePlate.png",
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
            self.assertEqual(exports[1]["params"]["sheet"], "S1")

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
                        "sheet": "$drawing_1_sheet",
                        "path": "models/part/drawings/Part.pdf",
                        "preview": "models/part/drawings/Part.png",
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
                preview = root / "models/part/drawings/Part.png"
                preview.write_bytes(b"\x89PNG\r\n\x1a\npreview")

            run.side_effect = fake_run
            with self.assertRaisesRegex(RuntimeError, "not a PDF"):
                _export_drawings(
                    document=document,
                    row=row,
                    variables={"$drawing_1": "D1", "$drawing_1_sheet": "S1"},
                    saved=saved,
                    output_root=root,
                    work_dir=work,
                )

    @patch("cad_model_build.runtime.subprocess.run")
    def test_drawing_export_rejects_non_png_preview(self, run):
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
                        "sheet": "$drawing_1_sheet",
                        "path": "models/part/drawings/Part.pdf",
                        "preview": "models/part/drawings/Part.png",
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
                for export in (
                    item for item in payload["commands"]
                    if item["command"] == "drawing.export"
                ):
                    target = Path(export["params"]["path"])
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if export["params"]["format"] == "pdf":
                        target.write_bytes(b"%PDF-1.7\n")
                    else:
                        target.write_bytes(b"not-a-png")

            run.side_effect = fake_run
            with self.assertRaisesRegex(RuntimeError, "not a PNG"):
                _export_drawings(
                    document=document,
                    row=row,
                    variables={"$drawing_1": "D1", "$drawing_1_sheet": "S1"},
                    saved=saved,
                    output_root=root,
                    work_dir=work,
                )

if __name__ == "__main__":
    unittest.main()
