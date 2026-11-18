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

    def test_empty_modern_store_requires_legacy_bootstrap(self):
        with TemporaryDirectory() as temp:
            build = Path(temp)
            self.assertTrue(
                publish_ci.needs_legacy_bootstrap(
                    build,
                    ("hub75-display2",),
                )
            )

    def test_catalog_growth_skips_legacy_bootstrap_when_candidate_covers_missing(self):
        with TemporaryDirectory() as temp:
            build = Path(temp)
            expected = tuple(publish_ci.model_slugs("native"))
            missing = expected[-1]

            for slug in expected[:-1]:
                verification = (
                    build
                    / "main"
                    / publish_ci.model_build_path(slug)
                    / "verification.json"
                )
                verification.parent.mkdir(parents=True, exist_ok=True)
                verification.write_text(
                    '{"model":"' + slug + '","verified":true}',
                    encoding="utf-8",
                )

            self.assertFalse(
                publish_ci.needs_legacy_bootstrap(
                    build,
                    (missing,),
                )
            )

    def test_incomplete_modern_store_outside_candidate_fails(self):
        with TemporaryDirectory() as temp:
            build = Path(temp)
            expected = tuple(publish_ci.model_slugs("native"))
            keep = expected[0]
            verification = (
                build
                / "main"
                / publish_ci.model_build_path(keep)
                / "verification.json"
            )
            verification.parent.mkdir(parents=True, exist_ok=True)
            verification.write_text(
                '{"model":"' + keep + '","verified":true}',
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                RuntimeError,
                "outside the current candidate",
            ):
                publish_ci.needs_legacy_bootstrap(
                    build,
                    (expected[-1],),
                )

    def test_stable_publication_builds_site_outside_container_output(self):
        source_sha = "a" * 40
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = root / "output"
            build = root / "build"
            pages = root / "pages"
            source = root / "source"
            for path in (bundle, build, pages, source):
                path.mkdir()
            (bundle / "publish.json").write_text(
                '{"channel":"stable","preview_key":"","models":[],"source_commit":"'
                + source_sha
                + '"}',
                encoding="utf-8",
            )

            seen = {}

            def fake_build_stable_site(**kwargs):
                out = kwargs["out"]
                seen["out"] = out
                self.assertFalse(out.is_relative_to(bundle))
                out.mkdir(parents=True)
                (out / "provenance.json").write_text("{}", encoding="utf-8")
                return out

            with patch.object(
                publish_ci.subprocess,
                "check_output",
                return_value=source_sha + "\n",
            ), patch.object(
                publish_ci,
                "stable_complete",
                return_value=True,
            ), patch.object(
                publish_ci,
                "prune_removed_models",
            ), patch.object(
                publish_ci,
                "remove_legacy_build_layout",
            ), patch.object(
                publish_ci,
                "write_build_readme",
            ), patch.object(
                publish_ci,
                "commit_and_push",
                return_value=True,
            ), patch.object(
                publish_ci,
                "build_stable_site",
                side_effect=fake_build_stable_site,
            ), patch.object(
                publish_ci,
                "replace_stable_pages",
            ):
                published = publish_ci.execute(
                    bundle=bundle,
                    source_root=source,
                    build_root=build,
                    pages_root=pages,
                    workflow_event="push",
                    workflow_head_branch="main",
                    workflow_head_sha=source_sha,
                )

            self.assertTrue(published)
            self.assertIn("out", seen)

    def test_build_stable_site_uses_explicit_output_path(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            out = root / "host-site"
            with patch.object(publish_ci, "run") as run:
                result = publish_ci.build_stable_site(
                    source_root=root / "source",
                    build_root=root / "build",
                    pages_root=root / "pages",
                    out=out,
                    source_commit="a" * 40,
                )

        self.assertEqual(result, out)
        build_command = run.call_args_list[0].args[0]
        self.assertIn("--out", build_command)
        self.assertEqual(
            build_command[build_command.index("--out") + 1],
            str(out),
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
