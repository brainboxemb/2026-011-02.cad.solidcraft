from pathlib import Path
import json
import tempfile
import unittest

from cad_model_pages.verify import PagesVerificationError, verify


class PagesVerifyTests(unittest.TestCase):
    def test_verifies_models_from_build_plan_without_fixed_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            site = root / "site"
            build = root / "build"
            model = repo / "models" / "component-a"
            page = site / "models" / "variant-a"
            model.mkdir(parents=True)
            page.mkdir(parents=True)
            build.mkdir(parents=True)
            (site / "index.html").write_text(
                "home · Recently updated models",
                encoding="utf-8",
            )
            (site / "models/index.html").write_text(
                "Basic Models · Components · Advanced Models",
                encoding="utf-8",
            )
            for category in ("basic", "components", "advanced"):
                category_page = site / "models" / category
                category_page.mkdir(parents=True)
                (category_page / "index.html").write_text(
                    f'<main class="cad-category-page"><div class="cad-model-grid">{"<a href=/models/variant-a/>Variant A</a>" if category == "components" else ""}</div></main>',
                    encoding="utf-8",
                )

            (model / "model.yml").write_text(
                "section: components\ntitle: Variant A\nparameters: 10 × 20 mm\n",
                encoding="utf-8",
            )
            plan = {
                "schema": 1,
                "solidcraft": {"version": "0.48.1"},
                "models": [
                    {
                        "id": "variant-a",
                        "root": "models/component-a",
                        "native": {"stl": "models/variant-a/model.stl"},
                        "snapshots": [{"name": "top.png"}],
                    }
                ],
            }
            (build / "build-plan.json").write_text(
                json.dumps(plan),
                encoding="utf-8",
            )

            (page / "index.html").write_text(
                "Variant A · 10 × 20 mm · Built in SolidCraft 0.48.1",
                encoding="utf-8",
            )
            for name in (
                "model.png",
                "model.sc",
                "model.step",
                "model.stl",
                "scpf-source.py",
                "model.yml",
                "ci.yml",
                "top.png",
            ):
                (page / name).write_bytes(b"x")
            (page / "solidcraft.json").write_text(
                json.dumps({"commands": [{"command": "Part::Box"}]}),
                encoding="utf-8",
            )

            verify(repo=repo, site=site, build_scope=build)
            (site / "models/components/index.html").write_text("cad-model-detail", encoding="utf-8")
            with self.assertRaisesRegex(PagesVerificationError, "expected a category grid"):
                verify(repo=repo, site=site, build_scope=build)


if __name__ == "__main__":
    unittest.main()
