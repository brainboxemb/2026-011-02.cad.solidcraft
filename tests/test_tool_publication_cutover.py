"""Repository-level checks for the tool.cad.ci publication cutover."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ToolPublicationCutoverTests(unittest.TestCase):
    def test_workflow_installs_pinned_host_tool_before_publication(self):
        workflow = (ROOT / ".github/workflows/cad.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("python -m pip install -e ext/cad-ci", workflow)
        self.assertIn('--pull-request "$PR_NUMBER"', workflow)

    def test_cleanup_needs_only_trusted_source_checkout(self):
        workflow = (ROOT / ".github/workflows/cad.yml").read_text(
            encoding="utf-8"
        )
        cleanup = workflow.split("  cleanup:", 1)[1]
        self.assertNotIn("Checkout build output", cleanup)
        self.assertNotIn("Checkout Pages", cleanup)
        self.assertIn("source/scripts/ci/bootstrap_cad_ci.py", cleanup)
        self.assertIn("source/ext/cad-ci", cleanup)

    def test_cad_publisher_contains_no_git_push_implementation(self):
        text = (ROOT / "scripts/ci/publish_ci.py").read_text(encoding="utf-8")
        self.assertNotIn('"git", "push"', text)
        self.assertNotIn("commit_and_push", text)
        self.assertIn('"publish",\n                "build"', text)
        self.assertIn('"publish",\n            "pages"', text)


if __name__ == "__main__":
    unittest.main()
