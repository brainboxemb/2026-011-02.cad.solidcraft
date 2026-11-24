import unittest
from unittest.mock import patch

from cad_model_ci.history import changed_paths, last_successful_dev_sha


class HistoryTests(unittest.TestCase):
    @patch("cad_model_ci.history._json")
    def test_last_successful_dev_excludes_pull_request_and_current_target(self, get):
        get.return_value = {
            "workflow_runs": [
                {
                    "id": 20,
                    "event": "pull_request",
                    "status": "completed",
                    "conclusion": "success",
                    "head_sha": "pr",
                },
                {
                    "id": 19,
                    "event": "push",
                    "status": "completed",
                    "conclusion": "success",
                    "head_sha": "target",
                },
                {
                    "id": 18,
                    "event": "push",
                    "status": "completed",
                    "conclusion": "success",
                    "head_sha": "baseline",
                },
            ]
        }
        self.assertEqual(
            last_successful_dev_sha(
                repository="owner/repo",
                branch="dev",
                token="token",
                current_run_id=21,
                target_sha="target",
            ),
            "baseline",
        )

    @patch("cad_model_ci.history.subprocess.run")
    def test_non_ancestor_baseline_forces_full_fallback(self, run):
        run.return_value.returncode = 1
        self.assertIsNone(changed_paths(".", "old", "new"))

    @patch("cad_model_ci.history.subprocess.run")
    def test_changed_paths_uses_exact_baseline_and_target(self, run):
        ancestor = type("Result", (), {"returncode": 0})()
        diff = type("Result", (), {"stdout": "modules/build/ci.yml\nmodels/box/model.yml\n"})()
        run.side_effect = [ancestor, diff]
        self.assertEqual(
            changed_paths(".", "aaa", "bbb"),
            ("modules/build/ci.yml", "models/box/model.yml"),
        )
        self.assertEqual(
            run.call_args_list[1].args[0],
            ["git", "-C", ".", "diff", "--name-only", "aaa", "bbb", "--"],
        )


if __name__ == "__main__":
    unittest.main()
