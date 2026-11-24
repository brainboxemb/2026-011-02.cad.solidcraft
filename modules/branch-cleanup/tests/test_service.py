import unittest

from cad_model_branch_cleanup.config import CleanupConfig
from cad_model_branch_cleanup.service import post_merge_cleanup, sweep


CONFIG = CleanupConfig(
    stable="main",
    development="dev",
    temporary_prefixes=("issue/", "fix/"),
)


class FakeClient:
    def __init__(self):
        self.deleted = []
        self._branches = ["main", "dev", "issue/1-done", "fix/2-open", "other"]

    def branches(self):
        return list(self._branches)

    def open_pr_exists(self, branch):
        return branch == "fix/2-open"

    def merged_pr_to(self, branch, base):
        return branch in {"issue/1-done", "fix/2-open"} and base == "dev"

    def delete_branch(self, branch):
        self.deleted.append(branch)


class ServiceTests(unittest.TestCase):
    def test_post_merge_deletes_only_safe_temporary_branch(self):
        client = FakeClient()
        self.assertTrue(
            post_merge_cleanup(
                client,
                head="issue/1-done",
                base="dev",
                same_repository=True,
                merged=True,
                config=CONFIG,
            )
        )
        self.assertEqual(client.deleted, ["issue/1-done"])

    def test_sweep_keeps_permanent_open_and_unproven_branches(self):
        client = FakeClient()
        deleted = sweep(client, config=CONFIG)
        self.assertEqual(deleted, ("issue/1-done",))
        self.assertEqual(client.deleted, ["issue/1-done"])


if __name__ == "__main__":
    unittest.main()
