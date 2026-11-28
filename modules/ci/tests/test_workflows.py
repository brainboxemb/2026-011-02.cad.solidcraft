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

    def test_pr_verify_is_read_only_and_publish_jobs_are_explicit(self):
        text = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("if: github.event_name == 'pull_request'", text)
        self.assertIn("contents: read", text)
        self.assertIn(
            "if: github.event_name != 'pull_request' && (github.ref_name == 'dev' || github.ref_name == 'main' || github.ref_name == 'exp')",
            text,
        )
        self.assertIn("publish-test:", text)
        self.assertIn("group: cad-test-output", text)
        self.assertIn("build/test/build-plan.json", text)
        self.assertIn("actions/upload-artifact@v7", text)
        self.assertIn("actions/download-artifact@v7", text)
        self.assertIn("--namespace test", text)
        self.assertIn("--full", text)
        self.assertIn("contents: write", text)
        self.assertIn("python -m cad_model_build.publish", text)
        self.assertIn("PYTHONPATH: modules/build/src", text)
        self.assertNotIn("cad_model_pages", text)
        self.assertNotIn("actions-hugo", text)
        self.assertNotIn("deploy-pages", text)

    def test_pages_are_dispatched_after_build_without_blocking_ci(self):
        ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        pages = Path(".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("push:\n    branches: [dev, main, exp]", ci)
        self.assertIn(
            "if: github.event_name != 'pull_request' && (github.ref_name == 'dev' || github.ref_name == 'main' || github.ref_name == 'exp')",
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
