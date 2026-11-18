"""Tests for CAD closed-PR cleanup through tool.cad.ci."""

from pathlib import Path
import os
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

import cleanup_ci  # noqa: E402


class CleanupCiTests(unittest.TestCase):
    def test_cleanup_delegates_both_generated_namespaces_to_tool(self):
        with TemporaryDirectory() as temp:
            source = Path(temp) / "source"
            source.mkdir()
            calls = []
            with patch.object(
                cleanup_ci,
                "run_tool",
                side_effect=lambda _source, *args: calls.append(args),
            ):
                cleanup_ci.execute(
                    source_root=source,
                    pull_request=12,
                )

        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][:2], ("publish", "build-cleanup"))
        self.assertEqual(calls[1][:2], ("publish", "pages-cleanup"))
        self.assertIn("12", calls[0])
        self.assertIn("12", calls[1])


    def test_cleanup_resolves_relative_source_root_once(self):
        """A nested checkout must not become source/source/ext/cad-ci."""

        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "source").mkdir()
            previous = Path.cwd()
            calls = []
            try:
                os.chdir(root)
                with patch.object(
                    cleanup_ci,
                    "run_tool",
                    side_effect=lambda source, *args: calls.append(
                        (source, args)
                    ),
                ):
                    cleanup_ci.execute(
                        source_root=Path("source"),
                        pull_request=12,
                    )
            finally:
                os.chdir(previous)

        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0], (root / "source").resolve())
        self.assertEqual(calls[1][0], (root / "source").resolve())

    def test_cleanup_rejects_invalid_pr_number(self):
        with TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "positive"):
                cleanup_ci.execute(
                    source_root=Path(temp),
                    pull_request=0,
                )


if __name__ == "__main__":
    unittest.main()
