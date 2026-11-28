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
                "    version: v0.13.2\n"
                "roots: {modules: modules, models: models, output: build}\n",
                encoding="utf-8",
            )
            config = load_project(repo)
            self.assertEqual(config.forge.version, "v0.13.2")
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

    def test_matching_build_yml_can_pin_exact_forge_qualification_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            ref = "a" * 40
            (repo / "build.yml").write_text(
                "schema: 1\n"
                "branch: chore/forge-candidate\n"
                "modules: [build]\n"
                "models: all\n"
                "tasks: [build]\n"
                "qualification:\n"
                "  forge:\n"
                f"    ref: {ref}\n",
                encoding="utf-8",
            )

            selection = load_build(repo, "chore/forge-candidate")

            self.assertEqual(selection.forge_ref, ref)

    def test_forge_qualification_ref_must_be_exact_commit_sha(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "build.yml").write_text(
                "schema: 1\n"
                "branch: chore/forge-candidate\n"
                "modules: [build]\n"
                "models: all\n"
                "tasks: [build]\n"
                "qualification:\n"
                "  forge:\n"
                "    ref: exp\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                "exact 40-character lowercase commit SHA",
            ):
                load_build(repo, "chore/forge-candidate")

    def test_forge_qualification_ref_requires_build_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "build.yml").write_text(
                "schema: 1\n"
                "branch: chore/forge-candidate\n"
                "modules: [build]\n"
                "models: []\n"
                "tasks: [test]\n"
                "qualification:\n"
                "  forge:\n"
                f"    ref: {'b' * 40}\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "requires the build task"):
                load_build(repo, "chore/forge-candidate")

    def test_mismatched_build_yml_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "build.yml").write_text(
                "schema: 1\n"
                "branch: issue/1-a\n"
                "modules: [build]\n"
                "models: all\n"
                "tasks: [build]\n"
                "qualification:\n"
                "  forge:\n"
                f"    ref: {'c' * 40}\n",
                encoding="utf-8",
            )
            self.assertIsNone(load_build(repo, "dev"))

    @patch.dict(os.environ, {"GITHUB_HEAD_REF": "issue/15-work"}, clear=False)
    def test_github_head_ref_is_the_work_branch(self):
        self.assertEqual(current_branch(Path(".")), "issue/15-work")


if __name__ == "__main__":
    unittest.main()
