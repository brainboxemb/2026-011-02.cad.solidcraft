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
                    '<section class="cad-catalog-group" data-cad-group="mft">'
                    '<h2>MFT</h2><div class="cad-model-grid">'
                    '<a href="/models/variant-a/">Variant A</a>'
                    '</div></section>'
                    if category == "components"
                    else '<div class="cad-model-grid"></div>'
                )
                (category_page / "index.html").write_text(
                    f'<main class="cad-category-page">{link}</main>',
                    encoding="utf-8",
                )

            (model / "model.yml").write_text(
                "section: components\ngroup: mft\ntitle: Variant A\nparameters: 10 × 20 mm\n",
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
                        "drawings": [
                            {
                                "name": "Variant A",
                                "drawing": "$drawing_1",
                                "sheet": "$drawing_1_sheet",
                                "orientation": "$drawing_1_orientation",
                                "path": "models/variant-a/drawings/Variant-A.pdf",
                                "preview": "models/variant-a/drawings/Variant-A.png",
                                "inspect": "models/variant-a/drawings/Variant-A.json",
                            }
                        ],
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
                json.dumps(
                    {
                        "commands": [{"command": "Part::Box"}],
                        "artifacts": {
                            "drawings": [
                                {
                                    "name": "Variant A",
                                    "drawing": "$drawing_1",
                                    "sheet": "$drawing_1_sheet",
                                    "orientation": "$drawing_1_orientation",
                                    "pdf": "drawings/Variant-A.pdf",
                                    "png": "drawings/Variant-A.png",
                                    "inspect": "drawings/Variant-A.json",
                                    "expected": {},
                                }
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            drawing = build / "models/variant-a/drawings/Variant-A.pdf"
            drawing.parent.mkdir(parents=True, exist_ok=True)
            drawing.write_bytes(b"%PDF-1.7\n")
            drawing.with_suffix(".png").write_bytes(b"\x89PNG\r\n\x1a\npreview")
            drawing.with_suffix(".json").write_text(
                json.dumps({"name": "Variant A"}),
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
                f"{blob}{native['stl']} · "
                f"{blob}models/variant-a/drawings/Variant-A.pdf · "
                f"{raw}models/variant-a/drawings/Variant-A.pdf · "
                f"{raw}models/variant-a/drawings/Variant-A.png",
                encoding="utf-8",
            )

            verify(repo=repo, site=site, build_scope=build)

            component_index = site / "models" / "components" / "index.html"
            grouped_html = component_index.read_text(encoding="utf-8")
            component_index.write_text(
                grouped_html.replace(' data-cad-group="mft"', ""),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                PagesVerificationError,
                "missing structural group",
            ):
                verify(repo=repo, site=site, build_scope=build)
            component_index.write_text(grouped_html, encoding="utf-8")

            (page / "model.stl").write_bytes(b"duplicate")
            with self.assertRaisesRegex(
                PagesVerificationError,
                "generated artifact duplicated in Pages",
            ):
                verify(repo=repo, site=site, build_scope=build)


    def test_accepts_exp_and_test_build_namespaces(self):
        for namespace in ("exp", "test"):
            with self.subTest(namespace=namespace), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                repo = root / "repo"
                site = root / "site"
                build = root / namespace
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
                        '<section class="cad-catalog-group" data-cad-group="mft">'
                        '<h2>MFT</h2><div class="cad-model-grid">'
                        '<a href="/models/variant-a/">Variant A</a>'
                        '</div></section>'
                        if category == "components"
                        else '<div class="cad-model-grid"></div>'
                    )
                    (category_page / "index.html").write_text(
                        f'<main class="cad-category-page">{link}</main>',
                        encoding="utf-8",
                    )

                (model / "model.yml").write_text(
                    "section: components\ngroup: mft\ntitle: Variant A\nparameters: 10 mm\n",
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
                }
                commands = "models/variant-a/solidcraft.json"
                plan = {
                    "schema": 1,
                    "namespace": namespace,
                    "source_ref": "issue/review" if namespace == "test" else "exp",
                    "source_sha": "a" * 40,
                    "solidcraft": {"version": "0.50.0"},
                    "models": [{
                        "id": "variant-a",
                        "root": "models/component-a",
                        "commands": commands,
                        "native": native,
                        "drawings": [],
                        "snapshots": [],
                    }],
                }
                (build / "build-plan.json").write_text(
                    json.dumps(plan),
                    encoding="utf-8",
                )
                for native_path in native.values():
                    target = build / native_path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(b"x")
                (build / commands).write_text(
                    json.dumps({"commands": [{"command": "Part::Box"}]}),
                    encoding="utf-8",
                )
                for name in ("scpf-source.py", "model.yml", "ci.yml"):
                    (page / name).write_text("source", encoding="utf-8")

                blob = f"https://github.com/example/cad/blob/build/{namespace}/"
                raw = f"https://raw.githubusercontent.com/example/cad/build/{namespace}/"
                (page / "index.html").write_text(
                    "Variant A · 10 mm · Built in SolidCraft 0.50.0 · "
                    f"<code>{namespace}</code> · "
                    f"{blob}{commands} · "
                    f"{raw}{native['png']} · "
                    f"{blob}{native['sc']} · "
                    f"{blob}{native['step']}",
                    encoding="utf-8",
                )

                verify(repo=repo, site=site, build_scope=build)


if __name__ == "__main__":
    unittest.main()
