import unittest
from unittest.mock import patch

from cad_model_merge_policy.__main__ import (
    dispatch_workflow,
    merge_required,
    pull_request_files,
    require_green_ci,
    require_main_governance_paths,
)
from cad_model_merge_policy.policy import (
    MergePolicyError,
    is_main_governance,
    merge_method,
)


def check(name, status, conclusion, *prs):
    return {
        "name": name,
        "status": status,
        "conclusion": conclusion,
        "pull_requests": [{"number": number} for number in prs],
    }


class MergePolicyTests(unittest.TestCase):
    def test_open_pull_request_requires_merge(self):
        self.assertTrue(merge_required({"state": "open", "merged": False}))

    def test_already_merged_pull_request_is_idempotent_noop(self):
        self.assertFalse(
            merge_required(
                {
                    "state": "closed",
                    "merged": True,
                    "merge_commit_sha": "abc123",
                }
            )
        )

    def test_closed_unmerged_pull_request_is_rejected(self):
        with self.assertRaisesRegex(MergePolicyError, "closed without merge"):
            merge_required({"state": "closed", "merged": False})

    def test_feature_to_dev_is_squash(self):
        self.assertEqual(merge_method(head="issue/10-change", base="dev"), "squash")

    def test_governance_docs_to_main_is_squash(self):
        self.assertTrue(
            is_main_governance(head="docs/125-plan", base="main")
        )
        self.assertEqual(
            merge_method(head="docs/125-plan", base="main"),
            "squash",
        )
        self.assertFalse(
            is_main_governance(head="docs/125-plan", base="dev")
        )

    @patch("cad_model_merge_policy.__main__.api")
    def test_main_governance_paths_are_allowlisted(self, api):
        api.return_value = [
            {"filename": "AGENTS.md"},
            {"filename": "docs/plan.md"},
            {"filename": "docs/handoff.md"},
        ]
        require_main_governance_paths("owner/repo", 25, "token")

    @patch("cad_model_merge_policy.__main__.api")
    def test_main_governance_rejects_non_governance_path(self, api):
        api.return_value = [
            {"filename": "docs/plan.md"},
            {"filename": "models/example/model.py"},
        ]
        with self.assertRaisesRegex(MergePolicyError, "forbidden"):
            require_main_governance_paths("owner/repo", 25, "token")

    @patch("cad_model_merge_policy.__main__.api")
    def test_pull_request_files_paginates_before_validation(self, api):
        api.side_effect = [
            [{"filename": "docs/plan.md"} for _ in range(100)],
            [{"filename": "README.md"}],
        ]
        self.assertEqual(
            len(pull_request_files("owner/repo", 25, "token")),
            101,
        )
        self.assertEqual(api.call_count, 2)
        with patch(
            "cad_model_merge_policy.__main__.pull_request_files",
            return_value=("docs/plan.md", "README.md"),
        ):
            with self.assertRaisesRegex(MergePolicyError, "README.md"):
                require_main_governance_paths("owner/repo", 25, "token")

    def test_dev_to_main_is_merge_commit(self):
        self.assertEqual(merge_method(head="dev", base="main"), "merge")

    def test_main_to_dev_is_merge_commit(self):
        self.assertEqual(merge_method(head="main", base="dev"), "merge")

    def test_feature_to_exp_is_squash(self):
        self.assertEqual(merge_method(head="issue/10-change", base="exp"), "squash")

    def test_dev_to_exp_is_merge_commit(self):
        self.assertEqual(merge_method(head="dev", base="exp"), "merge")

    def test_exp_to_dev_is_merge_commit(self):
        self.assertEqual(merge_method(head="exp", base="dev"), "merge")

    def test_exp_to_main_is_rejected(self):
        with self.assertRaises(MergePolicyError):
            merge_method(head="exp", base="main")

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
