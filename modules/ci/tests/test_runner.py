from pathlib import Path
import os
import unittest
from unittest.mock import patch

from cad_model_ci.config import BuildSelection, ForgeDependency, ProjectConfig
from cad_model_ci.items import CadModel, PythonModule
from cad_model_ci.runner import build_models, execute, test_module


class RunnerTests(unittest.TestCase):
    def project(self):
        return ProjectConfig(
            stable_branch="main",
            development_branch="dev",
            forge=ForgeDependency(
                "brainboxemb/lib.py.solidcraft.forge",
                "0.14.0",
                "a" * 40,
            ),
            modules_root=Path("modules"),
            models_root=Path("models"),
            output_root=Path("build"),
        )

    @patch("cad_model_ci.runner._run")
    def test_module_runs_from_source_without_installing_package(self, run):
        module = PythonModule("build", Path("modules/build"))
        test_module(module)

        command = run.call_args.args[0]
        env = run.call_args.kwargs["env"]
        self.assertEqual(command[:3], [os.sys.executable, "-m", "unittest"])
        self.assertIn(str(Path("modules/build/src").resolve()), env["PYTHONPATH"])

    @patch("cad_model_ci.runner._run")
    def test_model_batch_runs_build_module_from_source(self, run):
        model = CadModel(
            id="box",
            root=Path("models/box"),
            builder="forge",
            source=Path("scpf/model.py"),
        )
        build_models(
            repo=Path("."),
            build_module_root=Path("modules/build"),
            namespace="dev",
            models=(model,),
        )

        command = run.call_args.args[0]
        env = run.call_args.kwargs["env"]
        self.assertEqual(command[:3], [os.sys.executable, "-m", "cad_model_build"])
        self.assertIn(str(Path("modules/build/src").resolve()), env["PYTHONPATH"])
        self.assertIn("--model", command)
        self.assertIn("box", command)

    @patch("cad_model_ci.runner.build_models")
    @patch("cad_model_ci.runner.test_module")
    def test_execute_tests_modules_and_builds_models_only(
        self,
        test_module_mock,
        build_models_mock,
    ):
        module = PythonModule("ci", Path("modules/ci"))
        model = CadModel(
            id="box",
            root=Path("models/box"),
            builder="forge",
            source=Path("scpf/model.py"),
        )
        execute(
            repo=Path("."),
            project=self.project(),
            selection=BuildSelection(
                "issue/36",
                ("ci",),
                ("box",),
                ("test", "build"),
            ),
            namespace="dev",
            modules=(module,),
            models=(model,),
        )
        test_module_mock.assert_called_once_with(module)
        build_models_mock.assert_called_once()
        self.assertEqual(build_models_mock.call_args.kwargs["namespace"], "dev")
        self.assertEqual(build_models_mock.call_args.kwargs["models"], (model,))


if __name__ == "__main__":
    unittest.main()
