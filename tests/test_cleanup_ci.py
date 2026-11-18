"""Tests for CAD closed-PR cleanup."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

import cleanup_ci  # noqa: E402


class CleanupCiTests(unittest.TestCase):
    def test_cleanup_removes_only_requested_pr_namespaces(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            build = root / "build"
            pages = root / "pages"
            (build / "pr/12").mkdir(parents=True)
            (build / "pr/13").mkdir(parents=True)
            (pages / "preview/pr-12").mkdir(parents=True)
            (pages / "preview/pr-13").mkdir(parents=True)

            with patch.object(cleanup_ci, "commit_and_push") as commit:
                cleanup_ci.execute(
                    build_root=build,
                    pages_root=pages,
                    pull_request=12,
                )

            self.assertFalse((build / "pr/12").exists())
            self.assertTrue((build / "pr/13").is_dir())
            self.assertFalse((pages / "preview/pr-12").exists())
            self.assertTrue((pages / "preview/pr-13").is_dir())
            self.assertEqual(commit.call_count, 2)

    def test_cleanup_rejects_invalid_pr_number(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(ValueError, "positive"):
                cleanup_ci.execute(
                    build_root=root / "build",
                    pages_root=root / "pages",
                    pull_request=0,
                )


if __name__ == "__main__":
    unittest.main()
