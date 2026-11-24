from pathlib import Path
import tempfile
import unittest

from cad_model_pages.build import _stage_build_scope


class PagesBuildTests(unittest.TestCase):
    def test_keeps_scope_when_already_at_mount_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            scope = source / "prepared-build/main"
            scope.mkdir(parents=True)
            (scope / "build-plan.json").write_text(
                '{"schema": 1}',
                encoding="utf-8",
            )

            staged = _stage_build_scope(source, scope)

            self.assertEqual(staged, scope.resolve())
            self.assertTrue((staged / "build-plan.json").is_file())

    def test_stages_any_build_scope_at_site_mount_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            build_scope = root / "build-dev"
            source.mkdir()
            build_scope.mkdir()
            (build_scope / "build-plan.json").write_text(
                '{"schema": 1}',
                encoding="utf-8",
            )

            staged = _stage_build_scope(source, build_scope)

            self.assertEqual(staged, source / "prepared-build/main")
            self.assertEqual(
                (staged / "build-plan.json").read_text(encoding="utf-8"),
                '{"schema": 1}',
            )


if __name__ == "__main__":
    unittest.main()
