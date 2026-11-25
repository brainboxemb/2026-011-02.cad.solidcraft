from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_model_build.forge import compile_plan, install_url


class ForgeBuildTests(unittest.TestCase):
    def test_install_url_contains_release_version(self):
        version = "v0.15.0"
        self.assertIn(
            "@v0.15.0#subdirectory=cadlib",
            install_url("brainboxemb/lib.py.solidcraft.forge", version),
        )

    @patch("cad_model_build.forge.subprocess.run")
    def test_compile_plan_writes_each_solidcraft_json(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "models" / "box" / "scpf" / "model.py"
            source.parent.mkdir(parents=True)
            source.write_text("object()\n", encoding="utf-8")
            output = root / "build" / "dev"
            wheel = root / "scpf.whl"
            wheel.write_text("", encoding="utf-8")
            plan = {
                "models": [
                    {
                        "id": "box",
                        "source": "models/box/scpf/model.py",
                        "commands": "models/box/solidcraft.json",
                    }
                ]
            }

            def fake_run(command, **kwargs):
                target = Path(command[-1])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}\n", encoding="utf-8")

            run.side_effect = fake_run
            compile_plan(repo=root, output_root=output, plan=plan, wheel=wheel)
            self.assertTrue((output / "models/box/solidcraft.json").is_file())
            self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
