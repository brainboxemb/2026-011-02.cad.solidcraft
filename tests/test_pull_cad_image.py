"""Tests for the CAD image pull race between image and CAD workflows."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    """Load the image-pull helper directly from scripts/ci."""

    path = ROOT / "scripts" / "ci" / "pull_cad_image.py"
    spec = importlib.util.spec_from_file_location("pull_cad_image", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PullCadImageTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def result(self, code: int, *, stderr: str = "", stdout: str = ""):
        """Return the small subprocess result shape used by the helper."""

        return subprocess.CompletedProcess(
            ["docker", "pull", "image"],
            code,
            stdout,
            stderr,
        )

    def test_successful_pull_does_not_wait(self):
        with patch.object(
            self.module.subprocess,
            "run",
            return_value=self.result(0, stdout="ok\n"),
        ) as run, patch.object(self.module.time, "sleep") as sleep:
            self.module.pull("example/image:sha")

        run.assert_called_once()
        sleep.assert_not_called()

    def test_missing_image_is_retried_until_available(self):
        with patch.object(
            self.module.subprocess,
            "run",
            side_effect=[
                self.result(1, stderr="manifest unknown: not found"),
                self.result(0, stdout="pulled\n"),
            ],
        ) as run, patch.object(self.module.time, "sleep") as sleep:
            self.module.pull(
                "example/image:sha",
                attempts=3,
                delay_seconds=0.5,
            )

        self.assertEqual(run.call_count, 2)
        sleep.assert_called_once_with(0.5)

    def test_authentication_failure_is_not_retried(self):
        with patch.object(
            self.module.subprocess,
            "run",
            return_value=self.result(1, stderr="unauthorized"),
        ) as run, patch.object(self.module.time, "sleep") as sleep:
            with self.assertRaisesRegex(RuntimeError, "unauthorized"):
                self.module.pull("example/image:sha")

        run.assert_called_once()
        sleep.assert_not_called()

    def test_missing_image_fails_after_bounded_attempts(self):
        with patch.object(
            self.module.subprocess,
            "run",
            return_value=self.result(1, stderr="not found"),
        ) as run, patch.object(self.module.time, "sleep") as sleep:
            with self.assertRaisesRegex(RuntimeError, "after 3 pull attempts"):
                self.module.pull(
                    "example/image:sha",
                    attempts=3,
                    delay_seconds=0,
                )

        self.assertEqual(run.call_count, 3)
        self.assertEqual(sleep.call_count, 2)


if __name__ == "__main__":
    unittest.main()
