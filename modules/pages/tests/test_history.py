from pathlib import Path
import json
import tempfile
import unittest

from cad_model_pages.history import (
    ModelHistoryError,
    build_manifest,
    physical_model_roots,
    write_manifest,
)


class ModelHistoryTests(unittest.TestCase):
    def test_discovers_nested_physical_model_roots(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for root in ("simple-box", "basic/plate", "components/rail"):
                path = repo / "models" / root
                path.mkdir(parents=True)
                (path / "model.yml").write_text("title: x\n", encoding="utf-8")
                (path / "ci.yml").write_text("schema: 1\n", encoding="utf-8")

            self.assertEqual(
                physical_model_roots(repo),
                ("basic/plate", "components/rail", "simple-box"),
            )

    def test_requires_model_local_ci_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            path = repo / "models/basic/plate"
            path.mkdir(parents=True)
            (path / "model.yml").write_text("title: x\n", encoding="utf-8")

            with self.assertRaises(ModelHistoryError):
                physical_model_roots(repo)

    def test_manifest_maps_each_root_to_resolved_lastmod(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for root in ("basic/plate", "components/rail"):
                path = repo / "models" / root
                path.mkdir(parents=True)
                (path / "model.yml").write_text("title: x\n", encoding="utf-8")
                (path / "ci.yml").write_text("schema: 1\n", encoding="utf-8")

            manifest = build_manifest(
                repo,
                source_commit="a" * 40,
                lastmod_resolver=lambda _repo, root: {
                    "basic/plate": "2026-11-20T10:00:00+00:00",
                    "components/rail": "2026-11-21T10:00:00+00:00",
                }[root],
            )

            self.assertEqual(manifest["schema"], 1)
            self.assertEqual(manifest["source_commit"], "a" * 40)
            self.assertEqual(
                manifest["roots"]["components/rail"],
                "2026-11-21T10:00:00+00:00",
            )

            target = write_manifest(repo, manifest)
            self.assertEqual(
                json.loads(target.read_text(encoding="utf-8")),
                manifest,
            )


if __name__ == "__main__":
    unittest.main()
