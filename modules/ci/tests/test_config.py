from pathlib import Path
import os
import tempfile
import unittest
from unittest.mock import patch

from cad_model_ci.config import current_branch, load_build, load_project


class ConfigTests(unittest.TestCase):
    def test_project_reads_forge_pin_and_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "ci.yml").write_text(
                "schema: 1\n"
                "branches: {stable: main, development: dev}\n"
                "dependencies:\n"
                "  forge:\n"
                "    repository: brainboxemb/lib.py.solidcraft.forge\n"
                "    version: 0.13.2\n"
                "    commit: ea5710a5d2d33b0633b93c5da95dd5b74f126aa4\n"
                "roots: {modules: modules, models: models, output: build}\n",
                encoding="utf-8",
            )
            config = load_project(repo)
            self.assertEqual(config.forge.version, "0.13.2")
            self.assertEqual(config.modules_root, Path("modules"))
            self.assertEqual(config.output_root, Path("build"))

    def test_matching_build_yml_is_used(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "build.yml").write_text(
                "schema: 1\nbranch: issue/1-a\nmodules: [ci]\nmodels: []\ntasks: [test]\n",
                encoding="utf-8",
            )
            selection = load_build(repo, "issue/1-a")
            self.assertEqual(selection.modules, ("ci",))
            self.assertEqual(selection.tasks, ("test",))

    def test_mismatched_build_yml_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "build.yml").write_text(
                "schema: 1\nbranch: issue/1-a\nmodules: [ci]\nmodels: []\ntasks: [test]\n",
                encoding="utf-8",
            )
            self.assertIsNone(load_build(repo, "dev"))

    @patch.dict(os.environ, {"GITHUB_HEAD_REF": "issue/15-work"}, clear=False)
    def test_github_head_ref_is_the_work_branch(self):
        self.assertEqual(current_branch(Path(".")), "issue/15-work")


if __name__ == "__main__":
    unittest.main()
