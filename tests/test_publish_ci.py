"""Tests for CAD publication policy."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest


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
