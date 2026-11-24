from pathlib import Path
import tempfile
import unittest

from cad_model_pages.publish import _replace_site


class PagesPublishTests(unittest.TestCase):
    def test_replace_site_removes_stale_files_and_adds_nojekyll(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "generated"
            target = root / "target"
            (source / "models/simple-box").mkdir(parents=True)
            (source / "index.html").write_text("home", encoding="utf-8")
            (source / "models/simple-box/index.html").write_text(
                "model",
                encoding="utf-8",
            )
            target.mkdir()
            (target / "stale.txt").write_text("stale", encoding="utf-8")

            _replace_site(source, target)

            self.assertFalse((target / "stale.txt").exists())
            self.assertEqual(
                (target / "models/simple-box/index.html").read_text(
                    encoding="utf-8"
                ),
                "model",
            )
            self.assertTrue((target / ".nojekyll").is_file())


if __name__ == "__main__":
    unittest.main()
