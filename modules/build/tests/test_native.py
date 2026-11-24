from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_model_build.native import run_native_batch


class NativeBatchTests(unittest.TestCase):
    @patch("cad_model_build.native.subprocess.run")
    def test_non_empty_batch_uses_one_docker_run(self, run):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "build/dev"
            output.mkdir(parents=True)
            plan = output / "build-plan.json"
            plan.write_text("{}\n", encoding="utf-8")
            wheel_dir = root / "forge"
            wheel_dir.mkdir()
            wheel = wheel_dir / "scpf-0.14.0-py3-none-any.whl"
            wheel.write_text("", encoding="utf-8")

            run_native_batch(
                repo=root,
                output_root=output,
                plan_path=plan,
                forge_wheel=wheel,
                image="ghcr.io/brainboxemb/cad-solidcraft:v0.3.5",
                solidcraft_version="0.48.1",
            )

            commands = [call.args[0] for call in run.call_args_list]
            docker_runs = [
                command for command in commands
                if command[:2] == ["docker", "run"]
            ]
            self.assertEqual(len(docker_runs), 1)
            self.assertEqual(commands[0][:2], ["docker", "pull"])
            self.assertIn("EXPECTED_SOLIDCRAFT_VERSION=0.48.1", docker_runs[0])


if __name__ == "__main__":
    unittest.main()
