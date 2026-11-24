import unittest

from cad_model_branch_cleanup.config import CleanupConfig
from cad_model_branch_cleanup.policy import (
    eligible_post_merge,
    eligible_sweep,
    is_temporary,
)


CONFIG = CleanupConfig(
    stable="main",
    development="dev",
    temporary_prefixes=("issue/", "fix/", "feature/", "docs/", "chore/"),
)


class PolicyTests(unittest.TestCase):
    def test_permanent_branches_are_never_temporary(self):
        self.assertFalse(is_temporary("main", CONFIG))
        self.assertFalse(is_temporary("dev", CONFIG))

    def test_allowed_prefix_is_temporary(self):
        self.assertTrue(is_temporary("issue/11-cleanup", CONFIG))

    def test_merged_same_repo_feature_to_dev_is_eligible(self):
        self.assertTrue(
            eligible_post_merge(
                head="fix/7-cleanup",
                base="dev",
                same_repository=True,
                merged=True,
                config=CONFIG,
            )
        )

    def test_unmerged_or_open_work_is_not_sweep_eligible(self):
        self.assertFalse(
            eligible_sweep(
                branch="issue/11-work",
                has_open_pr=True,
                has_merged_pr_to_development=True,
                config=CONFIG,
            )
        )
        self.assertFalse(
            eligible_sweep(
                branch="issue/12-unmerged",
                has_open_pr=False,
                has_merged_pr_to_development=False,
                config=CONFIG,
            )
        )


if __name__ == "__main__":
    unittest.main()
