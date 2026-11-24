import unittest
from unittest.mock import patch

from cad_model_merge_policy.__main__ import (
    dispatch_workflow,
    require_green_ci,
)
from cad_model_merge_policy.policy import MergePolicyError, merge_method


def check(name, status, conclusion, *prs):
    return {
        "name": name,
        "status": status,
        "conclusion": conclusion,
        "pull_requests": [{"number": number} for number in prs],
    }


class MergePolicyTests(unittest.TestCase):
    def test_feature_to_dev_is_squash(self):
        self.assertEqual(merge_method(head="issue/10-change", base="dev"), "squash")

    def test_dev_to_main_is_merge_commit(self):
        self.assertEqual(merge_method(head="dev", base="main"), "merge")

    def test_main_to_dev_is_merge_commit(self):
        self.assertEqual(merge_method(head="main", base="dev"), "merge")

    def test_feature_to_main_is_rejected(self):
        with self.assertRaises(MergePolicyError):
            merge_method(head="issue/10-change", base="main")

    @patch("cad_model_merge_policy.__main__.api")
    def test_green_ci_allows_unrelated_pending_merge_check(self, api):
        api.return_value = {
            "check_runs": [
                check("ci", "completed", "success", 25),
                check("merge", "in_progress", None, 25),
                check("cleanup", "queued", None, 25),
            ]
        }
        require_green_ci("owner/repo", "sha", 25, "token")

    @patch("cad_model_merge_policy.__main__.api")
    def test_pending_ci_blocks_merge(self, api):
        api.return_value = {
            "check_runs": [check("ci", "in_progress", None, 25)]
        }
        with self.assertRaisesRegex(MergePolicyError, "still running"):
            require_green_ci("owner/repo", "sha", 25, "token")

    @patch("cad_model_merge_policy.__main__.api")
    def test_failed_ci_blocks_merge(self, api):
        api.return_value = {
            "check_runs": [check("ci", "completed", "failure", 25)]
        }
        with self.assertRaisesRegex(MergePolicyError, "not green"):
            require_green_ci("owner/repo", "sha", 25, "token")

    @patch("cad_model_merge_policy.__main__.api")
    def test_missing_pr_specific_ci_blocks_merge(self, api):
        api.return_value = {
            "check_runs": [
                check("ci", "completed", "success", 99),
                check("merge", "completed", "success", 25),
            ]
        }
        with self.assertRaisesRegex(MergePolicyError, "no central ci"):
            require_green_ci("owner/repo", "sha", 25, "token")

    @patch("cad_model_merge_policy.__main__.api")
    def test_dispatch_workflow_targets_local_workflow_and_base_ref(self, api):
        dispatch_workflow("owner/repo", "ci.yml", "dev", "token")
        api.assert_called_once_with(
            "owner/repo",
            "actions/workflows/ci.yml/dispatches",
            "token",
            method="POST",
            body={"ref": "dev"},
        )

    @patch("cad_model_merge_policy.__main__.api")
    def test_cleanup_workflow_uses_same_target_ref(self, api):
        dispatch_workflow("owner/repo", "branch-cleanup.yml", "dev", "token")
        api.assert_called_once_with(
            "owner/repo",
            "actions/workflows/branch-cleanup.yml/dispatches",
            "token",
            method="POST",
            body={"ref": "dev"},
        )


if __name__ == "__main__":
    unittest.main()
