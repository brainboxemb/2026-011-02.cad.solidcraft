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

    def test_mismatched_build_yml_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "build.yml").write_text(
                "schema: 1\nbranch: issue/1-a\nmodules: [ci]\nmodels: []\ntasks: [test]\n",
                encoding="utf-8",
            )
            self.assertIsNone(load_build(repo, "dev"))

    def test_matching_build_yml_accepts_digest_pinned_runtime_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            digest = "a" * 64
            (repo / "build.yml").write_text(
                "schema: 1\n"
                "branch: issue/122-runtime\n"
                "modules: []\n"
                "models: all\n"
                "tasks: [test, build]\n"
                "runtime:\n"
                "  solidcraft:\n"
                f"    image: ghcr.io/brainboxemb/cad-solidcraft@sha256:{digest}\n"
                "    version: 0.50.0\n",
                encoding="utf-8",
            )

            selection = load_build(repo, "issue/122-runtime")

            self.assertIsNotNone(selection.solidcraft_candidate)
            self.assertEqual(
                selection.solidcraft_candidate.image,
                f"ghcr.io/brainboxemb/cad-solidcraft@sha256:{digest}",
            )
            self.assertEqual(selection.solidcraft_candidate.version, "0.50.0")

    def test_runtime_candidate_rejects_mutable_or_tagged_images(self):
        for image in (
            "ghcr.io/brainboxemb/cad-solidcraft:edge",
            "ghcr.io/brainboxemb/cad-solidcraft:sha-abcdef0",
            "ghcr.io/brainboxemb/cad-solidcraft:v0.3.8",
        ):
            with self.subTest(image=image), tempfile.TemporaryDirectory() as tmp:
                repo = Path(tmp)
                (repo / "build.yml").write_text(
                    "schema: 1\n"
                    "branch: issue/122-runtime\n"
                    "modules: []\n"
                    "models: all\n"
                    "tasks: [build]\n"
                    "runtime:\n"
                    "  solidcraft:\n"
                    f"    image: {image}\n"
                    "    version: 0.50.0\n",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValueError, "sha256 digest"):
                    load_build(repo, "issue/122-runtime")

    def test_mismatched_build_ignores_invalid_runtime_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "build.yml").write_text(
                "schema: 1\n"
                "branch: issue/122-runtime\n"
                "modules: []\n"
                "models: all\n"
                "tasks: [build]\n"
                "runtime:\n"
                "  solidcraft:\n"
                "    image: ghcr.io/brainboxemb/cad-solidcraft:edge\n"
                "    version: 0.50.0\n",
                encoding="utf-8",
            )
            self.assertIsNone(load_build(repo, "dev"))

    @patch.dict(os.environ, {"GITHUB_HEAD_REF": "issue/15-work"}, clear=False)
    def test_github_head_ref_is_the_work_branch(self):
        self.assertEqual(current_branch(Path(".")), "issue/15-work")


if __name__ == "__main__":
    unittest.main()
