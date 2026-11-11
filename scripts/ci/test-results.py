#!/usr/bin/env python3
"""Lightweight site smoke checks: content, links and provenance labelling."""
import html.parser
import json
import re
import sys
import zipfile
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from model_catalog import COMPONENT_SOURCES, COMPONENT_DEFINITION_PRIMARY, COMMAND_SOURCES


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a":
            self.links.append(values.get("href", ""))
        if tag == "img":
            self.images.append(values.get("src", ""))


def check(site, commit):
    homepage = site / "index.html"
    assert homepage.is_file()
    assert (site / "results.css").is_file()
    provenance = json.loads((site / "provenance.json").read_text(encoding="utf-8"))
    assert provenance["source_commit"] == commit
    if provenance["native_verified_models"]:
        assert provenance.get("solidcraft_version") == "0.30.1"
    assert re.fullmatch(r"[0-9a-f]{40}", provenance["scpf_commit"])
    assert re.fullmatch(r"[0-9a-f]{40}", provenance["scpc_commit"])
    assert isinstance(provenance["native_verified_models"], list)
    assert len(set(provenance["native_verified_models"])) == len(provenance["native_verified_models"])
    cheatsheet = site / "cheatsheet" / "index.html"
    assert cheatsheet.is_file()
    guide = cheatsheet.read_text(encoding="utf-8")
    library_url = "https://brainboxemb.github.io/lib.py.solidcraft.forge/cheatsheet/"
    assert f'http-equiv="refresh" content="0; url={library_url}"' in guide
    assert f'rel="canonical" href="{library_url}"' in guide
    assert "Rectangle2D" not in guide  # no duplicated API reference

    text = homepage.read_text(encoding="utf-8")
    assert commit in text, "site must identify its source commit"
    assert 'href="https://brainboxemb.github.io/lib.py.solidcraft.forge/cheatsheet/"' in text
    assert "SCPF" in text and "SCRF" not in text
    assert "SolidCraft engine:" in text and "0.30.1 tested" in text
    assert 'href="https://brainboxemb.github.io/lib.py.solidcraft/"' in text
    assert "SolidCraft <span>CAD models</span>" in text
    assert text.index(">Basic Models<") < text.index(">Components<") < text.index(">Advanced Models<")
    for name in ("id=\"basic\"", "id=\"components\"", "id=\"advanced\""):
        assert name in text, name
    assert provenance["scpf_commit"] in text
    for slug in ("plate", "csg-cube", "bracket", "corner-bracket", "hub75-panel", "hub75-screen", "hub75-wood-frame", "sample-plate", "plastic-enclosure", "plastic-enclosure-pi"):
        model = site / "models" / slug
        assert (model / "index.html").is_file(), slug
        assert (model / "model.py").is_file(), slug
        assert (model / "solidcraft.json").is_file(), slug
        page = (model / "index.html").read_text(encoding="utf-8")
        assert "Native SolidCraft command sequence" in page
        assert "SolidCraft 0.30.1" in page
        assert "Show exact command and parameters" not in page
        assert "<details>" not in page
        assert "&quot;command&quot;" in page and "&quot;params&quot;" in page
        assert "Construction stages" in page
        assert 'class="two model-preview-layout"' in page
        component_source = COMPONENT_SOURCES.get(slug)
        if component_source is not None:
            # The prominent code sample must be the real shared part,
            # not only the tiny wrapper that imports the shared class.
            source_file = model / "source" / component_source
            assert source_file.is_file(), (slug, component_source)
            actual = Path(__file__).resolve().parents[2] / component_source
            assert source_file.read_bytes() == actual.read_bytes(), slug
            assert 'href="source/' + component_source + '"' in page
            assert '<h2>Python component — actual geometry</h2>' in page
            assert '<h2>Model script — how the component is used</h2>' in page
            geometry_index = page.index('<h2>Python component — actual geometry</h2>')
            launcher_index = page.index('<h2>Model script — how the component is used</h2>')
            if slug in COMPONENT_DEFINITION_PRIMARY:
                assert geometry_index < launcher_index, slug
            else:
                assert launcher_index < geometry_index, slug
            assert 'href="model.py"' in page, slug
        else:
            assert "<h2>Python model</h2>" in page, slug
        if (model / "native.png").is_file():
            assert 'class="preview-fullsize"' in page
            assert 'href="native.png"' in page
        assert "Native SolidCraft image" not in page or (model / "native.png").is_file()
        assert "Schematic drawing only" not in page or "not a SolidCraft geometry render" in page
        if "Previously verified render from main" in page:
            assert (model / "native.png").is_file()
            assert "not yet native-verified" in page
        if slug in provenance["native_verified_models"]:
            # Published .sc is the editable native ZIP document, not the
            # command JSON. It must belong to this exact verified build.
            native_file = model / "model.sc"
            assert native_file.is_file() and zipfile.is_zipfile(native_file), slug
            with zipfile.ZipFile(native_file) as archive:
                doc = json.loads(archive.read("document.json"))
                container = json.loads(archive.read("container.json"))
                assert doc["format"] == "solidcraft/48", slug
                assert container["format"] == "solidcraft-container/1", slug
            assert 'href="model.sc"' in page
            assert 'href="viewer.html"' not in page, slug
            assert not (model / "viewer.html").exists(), slug
            assert "<iframe" not in page, slug
            assert "Open in SolidCraft Web (external website)" in page
            assert "docs.solidcraft.io" in page
            assert "network traffic" in page
            assert "You are leaving" in page
            expected_model_url = (
                "https://brainboxemb.github.io/2026-011-02.cad.solidcraft/"
                f"models/{slug}/model.sc"
            )
            parser_page = Parser()
            parser_page.feed(page)
            full_urls = [
                href for href in parser_page.links
                if href.startswith("https://docs.solidcraft.io/app/?open=")
            ]
            assert len(full_urls) == 1, slug
            full_query = parse_qs(urlparse(full_urls[0]).query)
            assert full_query.get("open") == [expected_model_url], slug
            assert "?embed" not in full_urls[0], slug
            assert 'target="_blank" rel="noopener noreferrer"' in page
        else:
            # PR previews may reuse a stale screenshot but must NEVER
            # claim the browser can open a source-matched native design.
            assert "Open in SolidCraft Web (external website)" not in page, slug
            assert 'href="viewer.html"' not in page, slug
            assert not (model / "viewer.html").exists(), slug
            assert "<iframe" not in page, slug
        if slug in COMMAND_SOURCES:
            native_file = model / "scpc-model.py"
            native_json = model / "scpc-commands.json"
            assert native_file.is_file(), slug
            assert native_json.is_file(), slug
            actual = Path(__file__).resolve().parents[2] / COMMAND_SOURCES[slug]
            assert native_file.read_bytes() == actual.read_bytes(), slug
            assert "SCPC — explicit native SolidCraft commands" in page, slug
            assert 'href="scpc-model.py"' in page, slug
            assert 'href="scpc-commands.json"' in page, slug
            assert 'script.add' in page, slug
            data = json.loads(native_json.read_text(encoding="utf-8"))
            assert len(data["commands"]) == (12 if slug == "plate" else 17)
        else:
            assert not (model / "scpc-model.py").exists(), slug
            assert not (model / "scpc-commands.json").exists(), slug
        if slug == "hub75-panel" and slug in provenance["native_verified_models"]:
            for filename in ("front.png", "rear.png"):
                assert (model / filename).is_file()
                assert f'href="{filename}"' in page
                assert f'src="{filename}"' in page
            assert "Front and rear of the same upright panel" in page
        parser = Parser()
        parser.feed(page)
        for href in parser.links:
            if href.startswith(("http://", "https://", "#", "mailto:")):
                continue
            resolved = (model / href).resolve()
            if href.endswith("/") or href in ("../../",):
                assert resolved.is_dir(), (slug, href)
            else:
                assert resolved.exists(), (slug, href)
        for src in parser.images:
            assert (model / src).is_file(), (slug, src)
    print("Static CAD results site passed smoke checks")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: test-results.py <output/site> <git-sha>")
    check(Path(sys.argv[1]), sys.argv[2])
