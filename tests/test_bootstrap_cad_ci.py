"""Tests for the exact external tool.cad.ci checkout."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    """Load the bootstrap helper without adding scripts/ci to sys.path."""

    path = ROOT / "scripts" / "ci" / "bootstrap_cad_ci.py"
    spec = importlib.util.spec_from_file_location("bootstrap_cad_ci", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def commit(repo: Path, text: str) -> str:
    """Create one commit in a small local dependency repository."""

    (repo / "tool.txt").write_text(text, encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(
        ["git", "commit", "-qm", text],
        cwd=repo,
        check=True,
    )
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        text=True,
    ).strip()


def manifest(root: Path, url: str, sha: str) -> None:
    """Write the minimum dependencies.repos data used by the bootstrap helper."""

    (root / "dependencies.repos").write_text(
        "repositories:\n"
        "  cad-ci:\n"
        "    type: git\n"
        f"    url: {url}\n"
        f"    version: {sha}\n",
        encoding="utf-8",
    )


class BootstrapCadCiTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_repository_pin_is_exact_released_commit(self):
        url, sha = self.module.dependency()
        self.assertEqual(
            url,
            "https://github.com/brainboxemb/tool.cad.ci.git",
        )
        self.assertEqual(
            sha,
            "aee6509975e28be996f460e09d2a2f9dece36d33",
        )

    def test_checkout_moves_to_new_exact_revision(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            upstream = root / "upstream"
            upstream.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=upstream, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.invalid"],
                cwd=upstream,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"],
                cwd=upstream,
                check=True,
            )
            first = commit(upstream, "first")
            second = commit(upstream, "second")
            target = root / "ext" / "cad-ci"

            manifest(root, str(upstream), first)
            self.assertEqual(
                self.module.ensure_checkout(root, target=target),
                first,
            )

            manifest(root, str(upstream), second)
            self.assertEqual(
                self.module.ensure_checkout(root, target=target),
                second,
            )

    def test_tracked_changes_are_not_overwritten(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            upstream = root / "upstream"
            upstream.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=upstream, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.invalid"],
                cwd=upstream,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test"],
                cwd=upstream,
                check=True,
            )
            first = commit(upstream, "first")
            second = commit(upstream, "second")
            target = root / "ext" / "cad-ci"

            manifest(root, str(upstream), first)
            self.module.ensure_checkout(root, target=target)
            (target / "tool.txt").write_text("local edit", encoding="utf-8")
            manifest(root, str(upstream), second)

            with self.assertRaisesRegex(
                RuntimeError,
                "tracked local changes",
            ):
                self.module.ensure_checkout(root, target=target)


if __name__ == "__main__":
    unittest.main()
