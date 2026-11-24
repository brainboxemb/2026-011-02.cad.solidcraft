from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_model_build.runtime import _snapshot


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


if __name__ == "__main__":
    unittest.main()
