from pathlib import Path
import json
import tempfile
import unittest

from cad_model_pages.verify import PagesVerificationError, verify


class PagesVerifyTests(unittest.TestCase):
    def test_verifies_durable_build_links_without_page_copies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            site = root / "site"
            build = root / "dev"
            model = repo / "models" / "component-a"
            page = site / "models" / "variant-a"
            model.mkdir(parents=True)
            page.mkdir(parents=True)
            build.mkdir(parents=True)
            config = repo / "site/config/_default"
            config.mkdir(parents=True)
            (config / "hugo.toml").write_text(
                '[params]\ncadSourceRepository = "example/cad"\n',
                encoding="utf-8",
            )
            catalog = repo / "site/data/cad"
            catalog.mkdir(parents=True)
            (catalog / "catalog.yml").write_text(
                """sections:
  - id: basic
    title: Basic
  - id: components
    title: Components
  - id: subassemblies
    title: Sub Assemblies
  - id: assemblies
    title: Assemblies
groups:
  - id: display
    title: Display
  - id: mft
    title: MFT
""",
                encoding="utf-8",
            )

            (site / "index.html").write_text(
                "home · Recently updated models",
                encoding="utf-8",
            )
            (site / "models/index.html").write_text(
                "Basic · Components · Sub Assemblies · Assemblies",
                encoding="utf-8",
            )
            for category in ("basic", "components", "subassemblies", "assemblies"):
                category_page = site / "models" / category
                category_page.mkdir(parents=True)
                link = (
                    '<a href="/models/variant-a/">Variant A</a>'
                    if category == "components"
                    else ""
                )
                (category_page / "index.html").write_text(
                    f'<main class="cad-category-page">'
                    f'<div class="cad-model-grid">{link}</div></main>',
                    encoding="utf-8",
                )

            (model / "model.yml").write_text(
                "section: components\ntitle: Variant A\nparameters: 10 × 20 mm\n",
                encoding="utf-8",
            )
            (model / "ci.yml").write_text(
                "schema: 1\nid: variant-a\nbuilder: forge\nsource: scpf/model.py\n",
                encoding="utf-8",
            )

            native = {
                "png": "models/variant-a/model.png",
                "sc": "models/variant-a/model.sc",
                "step": "models/variant-a/model.step",
                "stl": "models/variant-a/model.stl",
            }
            commands = "models/variant-a/solidcraft.json"
            snapshot = "models/variant-a/top.png"
            plan = {
                "schema": 1,
                "namespace": "dev",
                "solidcraft": {"version": "0.48.1"},
                "models": [
                    {
                        "id": "variant-a",
                        "root": "models/component-a",
                        "commands": commands,
                        "native": native,
                        "snapshots": [{"name": "top.png", "path": snapshot}],
                    }
                ],
            }
            (build / "build-plan.json").write_text(
                json.dumps(plan),
                encoding="utf-8",
            )
            for path in native.values():
                target = build / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"x")
            snapshot_path = build / snapshot
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            snapshot_path.write_bytes(b"x")
            command_path = build / commands
            command_path.write_text(
                json.dumps({"commands": [{"command": "Part::Box"}]}),
                encoding="utf-8",
            )

            for name in ("scpf-source.py", "model.yml", "ci.yml"):
                (page / name).write_text("source", encoding="utf-8")

            blob = "https://github.com/example/cad/blob/build/dev/"
            raw = "https://raw.githubusercontent.com/example/cad/build/dev/"
            (page / "index.html").write_text(
                "Variant A · 10 × 20 mm · Built in SolidCraft 0.48.1 · "
                "<code>dev</code> · "
                f"{blob}{commands} · "
                f"{raw}{native['png']} · "
                f"{blob}{native['sc']} · "
                f"{blob}{native['step']} · "
                f"{blob}{native['stl']}",
                encoding="utf-8",
            )

            verify(repo=repo, site=site, build_scope=build)

            (page / "model.stl").write_bytes(b"duplicate")
            with self.assertRaisesRegex(
                PagesVerificationError,
                "generated artifact duplicated in Pages",
            ):
                verify(repo=repo, site=site, build_scope=build)


if __name__ == "__main__":
    unittest.main()
