import json
from pathlib import Path
import tempfile
import unittest

from cad_model_build.publish import _update_scope


def write_plan(path: Path, namespace: str, source_sha: str, models: list[dict]) -> dict:
    plan = {
        "schema": 1,
        "namespace": namespace,
        "source_sha": source_sha,
        "forge": {"version": "0.14.0"},
        "solidcraft": {"version": "0.48.1"},
        "models": models,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan), encoding="utf-8")
    return plan


class PublishScopeTests(unittest.TestCase):
    def test_incremental_update_preserves_unselected_active_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            worktree = root / "worktree"
            candidate = root / "candidate"
            worktree.mkdir()
            candidate.mkdir()

            durable = worktree / "dev"
            old_a = durable / "models/a"
            old_b = durable / "models/b"
            old_a.mkdir(parents=True)
            old_b.mkdir(parents=True)
            (old_a / "model.sc").write_text("old-a", encoding="utf-8")
            (old_b / "model.sc").write_text("old-b", encoding="utf-8")
            write_plan(
                durable / "build-plan.json",
                "dev",
                "1" * 40,
                [
                    {"id": "a", "built_source_sha": "1" * 40},
                    {"id": "b", "built_source_sha": "1" * 40},
                ],
            )

            new_a = candidate / "models/a"
            new_a.mkdir(parents=True)
            (new_a / "model.sc").write_text("new-a", encoding="utf-8")
            candidate_plan = write_plan(
                candidate / "build-plan.json",
                "dev",
                "2" * 40,
                [{"id": "a", "built_source_sha": "2" * 40}],
            )

            _update_scope(
                worktree=worktree,
                candidate_scope=candidate,
                candidate_plan=candidate_plan,
                active_ids={"a", "b"},
                namespace="dev",
                full=False,
            )

            self.assertEqual(
                (durable / "models/a/model.sc").read_text(encoding="utf-8"),
                "new-a",
            )
            self.assertEqual(
                (durable / "models/b/model.sc").read_text(encoding="utf-8"),
                "old-b",
            )
            merged = json.loads(
                (durable / "build-plan.json").read_text(encoding="utf-8")
            )
            self.assertEqual([row["id"] for row in merged["models"]], ["a", "b"])
            self.assertEqual(merged["models"][0]["built_source_sha"], "2" * 40)
            self.assertEqual(merged["models"][1]["built_source_sha"], "1" * 40)

    def test_incremental_update_removes_inactive_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            worktree = root / "worktree"
            candidate = root / "candidate"
            worktree.mkdir()
            candidate.mkdir()

            stale = worktree / "dev/models/stale"
            stale.mkdir(parents=True)
            (stale / "model.sc").write_text("stale", encoding="utf-8")
            write_plan(
                worktree / "dev/build-plan.json",
                "dev",
                "1" * 40,
                [{"id": "stale", "built_source_sha": "1" * 40}],
            )
            current = candidate / "models/current"
            current.mkdir(parents=True)
            (current / "model.sc").write_text("current", encoding="utf-8")
            candidate_plan = write_plan(
                candidate / "build-plan.json",
                "dev",
                "2" * 40,
                [{"id": "current", "built_source_sha": "2" * 40}],
            )

            _update_scope(
                worktree=worktree,
                candidate_scope=candidate,
                candidate_plan=candidate_plan,
                active_ids={"current"},
                namespace="dev",
                full=False,
            )

            self.assertFalse(stale.exists())
            self.assertTrue((worktree / "dev/models/current/model.sc").is_file())

    def test_full_update_replaces_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            worktree = root / "worktree"
            candidate = root / "candidate"
            (worktree / "main/models/old").mkdir(parents=True)
            (worktree / "main/models/old/model.sc").write_text("old", encoding="utf-8")
            (candidate / "models/new").mkdir(parents=True)
            (candidate / "models/new/model.sc").write_text("new", encoding="utf-8")
            candidate_plan = write_plan(
                candidate / "build-plan.json",
                "main",
                "2" * 40,
                [{"id": "new", "built_source_sha": "2" * 40}],
            )

            _update_scope(
                worktree=worktree,
                candidate_scope=candidate,
                candidate_plan=candidate_plan,
                active_ids={"new"},
                namespace="main",
                full=True,
            )

            self.assertFalse((worktree / "main/models/old").exists())
            self.assertTrue((worktree / "main/models/new/model.sc").is_file())


if __name__ == "__main__":
    unittest.main()
