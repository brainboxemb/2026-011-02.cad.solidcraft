"""Tests for CAD publication policy."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

import publish_ci  # noqa: E402


class PublishCiTests(unittest.TestCase):
    def test_stable_publication_is_main_only(self):
        publish = {
            "channel": "stable",
            "preview_key": "",
            "models": [],
            "source_commit": "a" * 40,
        }
        with self.assertRaisesRegex(ValueError, "only allowed from main"):
            publish_ci.validate_publication(
                publish,
                workflow_event="push",
                workflow_head_branch="feature/test",
                workflow_head_sha="a" * 40,
            )

    def test_preview_publication_requires_key(self):
        publish = {
            "channel": "preview",
            "preview_key": "",
            "models": [],
            "source_commit": "a" * 40,
        }
        with self.assertRaisesRegex(ValueError, "requires preview_key"):
            publish_ci.validate_publication(
                publish,
                workflow_event="pull_request",
                workflow_head_branch="feature/test",
                workflow_head_sha="a" * 40,
            )

    def test_commit_and_push_rebases_and_retries_after_concurrent_update(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(publish_ci, "run") as run, patch.object(
                publish_ci.subprocess,
                "run",
                side_effect=[
                    SimpleNamespace(returncode=1),
                    SimpleNamespace(returncode=1, stderr="rejected", stdout=""),
                    SimpleNamespace(returncode=0, stderr="", stdout=""),
                ],
            ) as process:
                changed = publish_ci.commit_and_push(
                    root,
                    branch="build",
                    message="Publish generated output",
                )

        self.assertTrue(changed)
        self.assertEqual(process.call_count, 3)
        commands = [call.args[0] for call in run.call_args_list]
        self.assertIn(["git", "fetch", "origin", "build"], commands)
        self.assertIn(["git", "rebase", "origin/build"], commands)
        self.assertNotIn(
            ["git", "push", "--force", "origin", "HEAD:build"],
            commands,
        )

    def test_commit_and_push_fails_after_bounded_retries(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(publish_ci, "run"), patch.object(
                publish_ci.subprocess,
                "run",
                side_effect=[
                    SimpleNamespace(returncode=1),
                    SimpleNamespace(returncode=1, stderr="rejected", stdout=""),
                    SimpleNamespace(returncode=1, stderr="rejected", stdout=""),
                ],
            ):
                with self.assertRaisesRegex(
                    RuntimeError,
                    "failed to publish build after 2 attempts",
                ):
                    publish_ci.commit_and_push(
                        root,
                        branch="build",
                        message="Publish generated output",
                        attempts=2,
                    )

    def test_replace_stable_pages_preserves_preview_namespace(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            site = root / "site"
            pages = root / "pages"
            site.mkdir()
            pages.mkdir()
            (site / "provenance.json").write_text("{}", encoding="utf-8")
            (site / "index.html").write_text("new", encoding="utf-8")
            (pages / "index.html").write_text("old", encoding="utf-8")
            preview = pages / "preview/pr-1"
            preview.mkdir(parents=True)
            (preview / "index.html").write_text("preview", encoding="utf-8")

            publish_ci.replace_stable_pages(site, pages)

            self.assertEqual(
                (pages / "index.html").read_text(encoding="utf-8"),
                "new",
            )
            self.assertEqual(
                (preview / "index.html").read_text(encoding="utf-8"),
                "preview",
            )


if __name__ == "__main__":
    unittest.main()
