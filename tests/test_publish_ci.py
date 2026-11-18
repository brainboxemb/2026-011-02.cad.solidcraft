"""Tests for CAD-to-tool.cad.ci publication orchestration."""

from pathlib import Path
import json
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

import publish_ci  # noqa: E402


def write_plan(bundle: Path, *, channel: str, publishable: bool = True) -> None:
    """Write the minimum CAD and tool plans consumed by the publisher."""

    bundle.mkdir(parents=True, exist_ok=True)
    preview = "pr-12" if channel == "preview" else ""
    (bundle / "plan.json").write_text(
        json.dumps(
            {
                "schema": 1,
                "channel": channel,
                "preview_key": preview,
                "publishable": publishable,
            }
        ),
        encoding="utf-8",
    )
    (bundle / "tool-cad-ci-plan.json").write_text(
        json.dumps(
            [{"id": "plate", "path": "models/basic/plate"}]
        ),
        encoding="utf-8",
    )


class PublishCiTests(unittest.TestCase):
    def run_execute(
        self,
        root: Path,
        *,
        channel: str,
        generic_main: bool,
        event: str,
        branch: str,
        pull_request: int,
    ):
        """Run publication with Git/tool/site operations replaced by records."""

        bundle = root / "output"
        source = root / "source"
        build = root / "generated-build"
        pages = root / "pages"
        for path in (source, build, pages):
            path.mkdir(parents=True, exist_ok=True)
        (source / "build/models/basic/plate").mkdir(parents=True)
        write_plan(bundle, channel=channel)
        if generic_main:
            (build / "main").mkdir(parents=True)
            (build / "main/build.json").write_text("{}", encoding="utf-8")

        calls = []

        def fake_tool(_source, *args):
            calls.append(args)
            if args[:2] == ("build", "prepare-main"):
                out = Path(args[args.index("--out") + 1])
                out.mkdir(parents=True, exist_ok=True)
                (out / "build.json").write_text("{}", encoding="utf-8")
            elif args[:2] == ("build", "update-main"):
                out = Path(args[args.index("--out") + 1])
                out.mkdir(parents=True, exist_ok=True)
                (out / "build.json").write_text("{}", encoding="utf-8")
            elif args[:2] == ("build", "prepare-pr"):
                out = Path(args[args.index("--out") + 1])
                out.mkdir(parents=True, exist_ok=True)
                (out / "build.json").write_text("{}", encoding="utf-8")
            elif args[:2] == ("build", "resolve"):
                out = Path(args[args.index("--out") + 1])
                out.mkdir(parents=True, exist_ok=True)
                (out / "build.json").write_text("{}", encoding="utf-8")

        def fake_site(**kwargs):
            out = kwargs["out"]
            out.mkdir(parents=True, exist_ok=True)
            (out / "provenance.json").write_text("{}", encoding="utf-8")
            return out

        with patch.object(
            publish_ci.subprocess,
            "check_output",
            return_value="a" * 40 + "\n",
        ), patch.object(
            publish_ci,
            "run_tool",
            side_effect=fake_tool,
        ), patch.object(
            publish_ci,
            "build_site",
            side_effect=fake_site,
        ):
            result = publish_ci.execute(
                bundle=bundle,
                source_root=source,
                build_root=build,
                pages_root=pages,
                workflow_event=event,
                workflow_head_branch=branch,
                workflow_head_sha="a" * 40,
                pull_request=pull_request,
            )
        return result, calls

    def test_first_stable_cutover_prepares_complete_main(self):
        with TemporaryDirectory() as temp:
            result, calls = self.run_execute(
                Path(temp),
                channel="stable",
                generic_main=False,
                event="push",
                branch="main",
                pull_request=0,
            )

        self.assertTrue(result)
        self.assertTrue(any(call[:2] == ("build", "prepare-main") for call in calls))
        self.assertTrue(
            any(
                call[:2] == ("publish", "build")
                and "main" in call
                for call in calls
            )
        )
        self.assertTrue(
            any(
                call[:2] == ("publish", "pages")
                and "--pull-request" not in call
                for call in calls
            )
        )

    def test_later_stable_run_updates_only_selected_items(self):
        with TemporaryDirectory() as temp:
            result, calls = self.run_execute(
                Path(temp),
                channel="stable",
                generic_main=True,
                event="push",
                branch="main",
                pull_request=0,
            )

        self.assertTrue(result)
        update = next(call for call in calls if call[:2] == ("build", "update-main"))
        self.assertIn("--items", update)
        self.assertIn("plate", update)

    def test_pr_publishes_overlay_resolves_view_and_publishes_preview(self):
        with TemporaryDirectory() as temp:
            result, calls = self.run_execute(
                Path(temp),
                channel="preview",
                generic_main=True,
                event="pull_request",
                branch="feature/test",
                pull_request=12,
            )

        self.assertTrue(result)
        self.assertTrue(any(call[:2] == ("build", "prepare-pr") for call in calls))
        self.assertTrue(any(call[:2] == ("build", "resolve") for call in calls))
        pages = next(
            call
            for call in calls
            if call[:2] == ("publish", "pages")
        )
        self.assertIn("--pull-request", pages)
        self.assertIn("12", pages)

    def test_manual_branch_run_checks_but_does_not_publish(self):
        with TemporaryDirectory() as temp:
            result, calls = self.run_execute(
                Path(temp),
                channel="preview",
                generic_main=True,
                event="workflow_dispatch",
                branch="feature/test",
                pull_request=0,
            )

        self.assertFalse(result)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
