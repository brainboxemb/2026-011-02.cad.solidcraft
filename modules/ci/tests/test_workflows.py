from pathlib import Path
import unittest


class WorkflowBoundaryTests(unittest.TestCase):
    def test_ci_workflow_runs_internal_modules_from_source(self):
        text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("PYTHONPATH: modules/ci/src", text)
        self.assertIn("python -m cad_model_ci", text)
        self.assertNotIn("pip install -e modules/ci", text)
        self.assertNotIn("simple-box", text)
        self.assertNotIn("lib.py.solidcraft.forge", text)
        self.assertNotIn("python -m scpf", text)

    def test_pr_job_is_read_only_and_build_job_can_publish(self):
        text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("if: github.event_name == 'pull_request'", text)
        self.assertIn("contents: read", text)
        self.assertIn(
            "if: github.event_name != 'pull_request' && (github.ref_name == 'dev' || github.ref_name == 'main')",
            text,
        )
        self.assertIn("contents: write", text)
        self.assertIn("python -m cad_model_build.publish", text)
        self.assertIn("PYTHONPATH: modules/build/src", text)
        self.assertNotIn("cad_model_pages", text)
        self.assertNotIn("actions-hugo", text)
        self.assertNotIn("deploy-pages", text)

    def test_pages_are_dispatched_after_build_without_blocking_ci(self):
        ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        pages = Path(".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("push:\n    branches: [dev, main]", ci)
        self.assertIn(
            "if: github.event_name != 'pull_request' && (github.ref_name == 'dev' || github.ref_name == 'main')",
            ci,
        )
        self.assertIn("actions: write", ci)
        self.assertIn("gh workflow run pages.yml --ref main", ci)
        self.assertIn("workflow_dispatch:", pages)
        self.assertNotIn("workflow_run:", pages)
        self.assertIn("peaceiris/actions-hugo@v3", pages)
        self.assertIn("python -m cad_model_pages.publish", pages)
        self.assertIn("--repo source-main", pages)
        self.assertNotIn("actions/deploy-pages", pages)
        self.assertNotIn("github-pages", pages)

    def test_workflow_actions_use_readable_release_tags(self):
        for path in Path(".github/workflows").glob("*.yml"):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r"uses: [^\s]+@[0-9a-f]{40}")

    def test_merge_workflow_runs_merge_policy_from_source(self):
        text = Path(".github/workflows/merge-policy.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("PYTHONPATH: modules/merge-policy/src", text)
        self.assertIn("python -m cad_model_merge_policy", text)
        self.assertNotIn("pip install -e modules/merge-policy", text)
        self.assertNotIn("tool.cad.ci", text)


if __name__ == "__main__":
    unittest.main()
