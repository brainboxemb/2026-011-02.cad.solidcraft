#!/usr/bin/env python3
"""Build a self-contained static CAD-results website (no third-party deps).

Content is generated from the current SCPF source and command JSON.
A rendered CAD screenshot is published only if native verification metadata
proves it belongs to exactly this source commit.
"""
import argparse
import html
import json
import re
import shutil
import zipfile
from urllib.parse import quote
from pathlib import Path
from model_catalog import (
    MODELS,
    SOURCES,
    SECTIONS,
    COMMAND_SOURCES,
    COMPONENT_SOURCES,
    COMPONENT_DEFINITION_PRIMARY,
    model_build_path,
    source_path,
)
from output_store import input_fingerprint
from model_item import stored_model_paths


ROOT = Path(__file__).resolve().parents[2]

# The official stable SolidCraft web app understands ?open= and ?embed&open=.
# Keep the .sc file on our existing GitHub Pages site: no custom web CAD
# runtime, frontend build, or CAD server is required for this first experiment.
PUBLIC_SITE = "https://brainboxemb.github.io/2026-011-02.cad.solidcraft"
SOLIDCRAFT_WEB = "https://docs.solidcraft.io/app/"
# Purely schematic line art; never mistaken for a native SolidCraft render.
DIAGRAMS = {
    "sample": """<path d="M65 115 300 50 425 100 185 175Z" fill="#bcd4ee" stroke="#285785" stroke-width="5"/><path d="M65 115 V160 L185 222 V175 M185 222 425 150 V100" fill="#8eb5db" stroke="#285785" stroke-width="4"/><ellipse cx="293" cy="100" rx="62" ry="39" fill="#5f92c6" stroke="#285785" stroke-width="4"/><path d="M231 100 V60 A62 39 0 0 1 355 60 V100" fill="#b4d0e9" stroke="#285785" stroke-width="4"/><ellipse cx="293" cy="60" rx="62" ry="39" fill="#d1e4f4" stroke="#285785" stroke-width="4"/><ellipse cx="293" cy="60" rx="29" ry="18" fill="#edf4fb" stroke="#285785" stroke-width="4"/><ellipse cx="130" cy="116" rx="15" ry="10" fill="#edf4fb" stroke="#285785" stroke-width="4"/><ellipse cx="385" cy="129" rx="15" ry="10" fill="#edf4fb" stroke="#285785" stroke-width="4"/>""",
    "plate": """<rect x="95" y="25" width="310" height="165" rx="16" fill="#d6e4f5" stroke="#285785" stroke-width="5"/><path d="M95 175 145 218 H420 V65 L405 25" fill="#99bad9" stroke="#285785" stroke-width="4"/><ellipse cx="155" cy="78" rx="12" ry="10" fill="#fff" stroke="#285785" stroke-width="4"/><ellipse cx="345" cy="78" rx="12" ry="10" fill="#fff" stroke="#285785" stroke-width="4"/><ellipse cx="155" cy="151" rx="12" ry="10" fill="#fff" stroke="#285785" stroke-width="4"/><ellipse cx="345" cy="151" rx="12" ry="10" fill="#fff" stroke="#285785" stroke-width="4"/>""",
    "csg": """<path d="M130 68 250 15 376 68 376 188 250 241 130 188Z" fill="#d6e4f5" stroke="#285785" stroke-width="5"/><path d="M130 68 250 125 376 68 M250 125 V241" fill="none" stroke="#285785" stroke-width="4"/><ellipse cx="250" cy="129" rx="39" ry="37" fill="#f1f6fc" stroke="#285785" stroke-width="5"/><ellipse cx="250" cy="130" rx="14" ry="34" fill="#acc6e3" stroke="#285785" stroke-width="3"/><path d="M196 90 307 162 M185 155 310 100" stroke="#285785" stroke-width="4" stroke-dasharray="8 8"/>""",
    "bracket": """<path d="M104 195 104 34 145 34 145 163 388 163 388 207 104 207Z" fill="#b4cde9" stroke="#285785" stroke-width="5"/><path d="M145 163 174 188 407 188 388 163 M388 207 407 188" fill="none" stroke="#285785" stroke-width="4"/><ellipse cx="230" cy="187" rx="14" ry="8" fill="#f4f7fc" stroke="#285785" stroke-width="4"/><ellipse cx="330" cy="187" rx="14" ry="8" fill="#f4f7fc" stroke="#285785" stroke-width="4"/>""",
    "guide-rail": """<path d="M55 150 380 62 445 88 120 177Z" fill="#c8d5e3" stroke="#285785" stroke-width="4"/><path d="M120 177 445 88 445 106 120 196Z" fill="#96aec8" stroke="#285785" stroke-width="4"/><path d="M88 141 412 54 M103 162 427 74" fill="none" stroke="#285785" stroke-width="4"/><path d="M155 132 177 126 189 131 167 137ZM275 100 297 94 309 99 287 105Z" fill="#eef4fb" stroke="#285785" stroke-width="3"/>""",
    "hub75": """<rect x="130" y="28" width="112" height="205" rx="2" fill="#b8b8b8" stroke="#374151" stroke-width="4"/><rect x="250" y="28" width="112" height="205" rx="2" fill="#b8b8b8" stroke="#374151" stroke-width="4"/><g fill="#f5f5f5" stroke="#374151" stroke-width="2"><circle cx="145" cy="42" r="3"/><circle cx="227" cy="42" r="3"/><circle cx="145" cy="130" r="3"/><circle cx="227" cy="130" r="3"/><circle cx="145" cy="218" r="3"/><circle cx="227" cy="218" r="3"/><circle cx="265" cy="42" r="3"/><circle cx="347" cy="42" r="3"/><circle cx="265" cy="130" r="3"/><circle cx="347" cy="130" r="3"/><circle cx="265" cy="218" r="3"/><circle cx="347" cy="218" r="3"/></g>""",
    "hub75-wood-frame": """<g stroke="#75532a" stroke-width="4" fill="#d6b17b">
<rect x="45" y="18" width="410" height="230" rx="2"/>
</g><g fill="#29323b" stroke="#151a21" stroke-width="1.5">
<rect x="76" y="43" width="68" height="180"/><rect x="145" y="43" width="68" height="180"/>
<rect x="214" y="43" width="68" height="180"/><rect x="283" y="43" width="68" height="180"/>
<rect x="352" y="43" width="68" height="180"/></g><g stroke="#d65a3f" stroke-width="7" fill="none">
<path d="M45 43 V18 H73"/><path d="M427 18 H455 V43"/>
<path d="M45 222 V248 H73"/><path d="M427 248 H455 V222"/></g>""",
    "hub75-screen": """<g fill="#b8b8b8" stroke="#374151" stroke-width="3"><rect x="24" y="32" width="84" height="192" rx="2"/><rect x="116" y="32" width="84" height="192" rx="2"/><rect x="208" y="32" width="84" height="192" rx="2"/><rect x="300" y="32" width="84" height="192" rx="2"/><rect x="392" y="32" width="84" height="192" rx="2"/></g><g fill="#f5f5f5" stroke="#374151" stroke-width="1.5"><circle cx="34" cy="44" r="3"/><circle cx="98" cy="44" r="3"/><circle cx="126" cy="44" r="3"/><circle cx="190" cy="44" r="3"/><circle cx="218" cy="44" r="3"/><circle cx="282" cy="44" r="3"/><circle cx="310" cy="44" r="3"/><circle cx="374" cy="44" r="3"/><circle cx="402" cy="44" r="3"/><circle cx="466" cy="44" r="3"/></g>""",
    "plastic-enclosure": """<path d="M82 78 250 25 420 78 420 185 250 238 82 185Z" fill="#a8c5e2" stroke="#285785" stroke-width="5"/><path d="M107 91 250 48 394 91 394 169 250 211 107 169Z" fill="#eef4fb" stroke="#285785" stroke-width="4"/><path d="M82 78 107 91 M420 78 394 91 M82 185 107 169 M420 185 394 169" stroke="#285785" stroke-width="4"/><ellipse cx="155" cy="153" rx="13" ry="9" fill="#7ba4cc" stroke="#285785" stroke-width="3"/><ellipse cx="345" cy="118" rx="13" ry="9" fill="#7ba4cc" stroke="#285785" stroke-width="3"/><rect x="218" y="128" width="64" height="38" rx="5" fill="#8db2d5" stroke="#285785" stroke-width="3"/><path d="M248 70 V128 M248 70 266 77 266 91" fill="none" stroke="#285785" stroke-width="5"/>""",
}


def esc(value):
    return html.escape(str(value), quote=True)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dependency_revision(name):
    """Read one explicit Git revision from the small vcs2l manifest."""
    manifest = (ROOT / "dependencies.repos").read_text(encoding="utf-8")
    section = re.search(
        rf"(?ms)^  {re.escape(name)}:\s*\n(.*?)(?=^  [\w-]+:|\Z)", manifest
    )
    if not section:
        raise ValueError(f"Missing {name} dependency section")
    sha = re.search(
        r"(?m)^    version:\s*([0-9a-f]{40})\s*$", section.group(1)
    )
    if not sha:
        raise ValueError(f"Missing exact {name} revision")
    return sha.group(1)


def library_revision():
    """Exact Forge/SCPF Git revision, not the independent SCPC version."""
    return dependency_revision("scpf")


def current_run_verification(native_root, commit, scpf_commit, scpc_commit):
    if native_root is None:
        return None
    manifest = native_root / "verification.json"
    if not manifest.is_file():
        return None
    metadata = read_json(manifest)
    if (
        metadata.get("source_commit") != commit
        or metadata.get("scpf_commit") != scpf_commit
        or metadata.get("scpc_commit") != scpc_commit
        or metadata.get("verified") is not True
    ):
        return None
    return metadata


def stored_model_output(store_root, slug):
    """Return current verified output from the durable model-root store.

    The path resolver also understands the old per-model layout during the
    cutover. Validation remains CAD-owned: stored geometry is accepted only
    when its model ID and declared input fingerprint still match this source.
    """

    if store_root is None:
        return None
    try:
        root, generated = stored_model_paths(store_root, slug)
    except RuntimeError:
        return None

    manifest = root / "verification.json"
    native = root / "native"
    metadata = read_json(manifest)
    if (
        metadata.get("model") != slug
        or metadata.get("verified") is not True
        or metadata.get("input_fingerprint") != input_fingerprint(slug)
    ):
        return None
    return {
        "root": root,
        "native": native,
        "generated": generated,
        "verification": metadata,
    }


def native_document_format(native_file):
    if not native_file.is_file() or not zipfile.is_zipfile(native_file):
        return None
    with zipfile.ZipFile(native_file) as archive:
        document = json.loads(archive.read("document.json"))
        container = json.loads(archive.read("container.json"))
    value = document.get("format")
    if not isinstance(value, str) or re.fullmatch(r"solidcraft/\d+", value) is None:
        raise ValueError(f"unsupported SolidCraft document format {value!r}")
    if container.get("format") != "solidcraft-container/1":
        raise ValueError("unsupported SolidCraft archive")
    return value

def diagram(model):
    return f'<svg role="img" aria-label="Schematic illustration; not a native CAD render" viewBox="0 0 500 260" xmlns="http://www.w3.org/2000/svg">{DIAGRAMS[MODELS[model]["diagram"]]}</svg>'


def layout(title, body, css_path, home_path):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · SolidCraft CAD projects</title><link rel="stylesheet" href="{esc(css_path)}"></head>
<body><header class="top"><div class="wrap nav">
<a class="brand" href="{esc(home_path)}">SolidCraft <span>CAD models</span></a>
<nav aria-label="Main"><a href="{esc(home_path)}">Models</a>
<a href="{LIBRARY_CHEATSHEET}">Cheatsheet</a>
<a href="https://brainboxemb.github.io/lib.py.solidcraft.forge/">SCPF library</a>
<a href="https://brainboxemb.github.io/lib.py.solidcraft.cmd/">SCPC library</a>
<a href="https://github.com/brainboxemb/2026-011-02.cad.solidcraft">Source</a></nav>
</div></header>
{body}<footer><div class="wrap"><strong>SolidCraft CAD</strong> renders and verifies the real geometry.
<a href="https://brainboxemb.github.io/lib.py.solidcraft.forge/">SCPF examples &amp; cheatsheet →</a>
<a href="https://brainboxemb.github.io/lib.py.solidcraft.cmd/">SCPC API &amp; examples →</a></div></footer>
</body></html>"""


def command_stages(commands):
    descriptions = {
        "parameters.add": "Named CAD parameter",
        "sketch.create": "Create sketch",
        "sketch.rectangle.two_point": "Rectangle",
        "sketch.line": "Profile edges",
        "sketch.circle.center": "Circle",
        "sketch.finish": "Finish sketch",
        "solid.extrude": "Extrusion / cut",
        "solid.fillet": "Rounded edge",
        "solid.chamfer": "Chamfered edge",
        "solid.box": "Box primitive",
        "solid.sphere": "Sphere primitive",
        "solid.cylinder": "Cylinder primitive",
        "solid.hole": "Native Hole feature",
        "component.create": "Create reusable component",
        "component.activate": "Activate component / root",
        "occurrence.copy": "Copy component occurrence",
        "occurrence.move": "Move component occurrence",
        "material.create": "Create physical material",
        "material.assign": "Assign material",
        "joint.create": "Assembly joint",
        "solid.shell": "Shell / hollow body",
        "solid.pattern.rectangular": "Rectangular feature pattern",
        "sketch.slot.center_to_center": "Center-to-center Slot",
        "sketch.pattern.rectangular": "Rectangular sketch pattern",
        "sketch.mirror": "Sketch mirror",
        "plastic.lip": "Plastic lip",
        "plastic.snap_fit": "Plastic snap fit",
        "plastic.boss": "Plastic screw boss",
        "plastic.rest": "Plastic support rest",
    }
    items = []
    for entry in commands:
        kind = entry["command"]
        description = descriptions.get(kind, kind)
        details = []
        params = entry.get("params", {})
        for key in ("name", "plane", "direction", "operation", "body_name"):
            if key in params:
                details.append(f"{key}: {params[key]}")
        items.append(
            f'<li><strong>{esc(description)}</strong>'
            f'<small>{esc(kind)}'
            + (f' · {esc(", ".join(details))}' if details else "")
            + '</small>'
            + f'<pre><code>{esc(json.dumps(entry, indent=2))}</code></pre>'
            + '</li>'
        )
    return "\n".join(items)


def copy_if_exists(source, target):
    if source.is_file():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def build(out, commit, native_root=None, generated_root=None, previous_site=None, stable_store=None, public_base=PUBLIC_SITE):
    out.mkdir(parents=True, exist_ok=True)
    copy_if_exists(ROOT / "site/results.css", out / "results.css")
    cards = {key: [] for key in SECTIONS}
    category_cards = {key: [] for key in SECTIONS}
    scpf_commit = library_revision()
    scpc_commit = dependency_revision("scpc")
    run_verification = current_run_verification(
        native_root,
        commit,
        scpf_commit,
        scpc_commit,
    )
    verified_models = []
    model_verifications = {}
    verified_count = 0
    for slug, info in MODELS.items():
        work = out / "models" / slug
        work.mkdir(parents=True, exist_ok=True)
        source = source_path(ROOT, slug)
        committed_command_file = (
            ROOT / "models" / slug / "scpf" / "solidcraft.json"
        )
        generated_command_file = (
            generated_root / slug / "scpf" / "solidcraft.json"
            if generated_root is not None
            else None
        )
        stored = stored_model_output(stable_store, slug)
        stored_command_file = (
            stored["generated"] / "scpf" / "solidcraft.json"
            if stored is not None
            else None
        )
        previous_command_file = (
            previous_site / "models" / slug / "solidcraft.json"
            if previous_site is not None
            else None
        )
        command_file = next(
            (
                candidate
                for candidate in (
                    generated_command_file,
                    stored_command_file,
                    previous_command_file,
                    committed_command_file,
                )
                if candidate is not None and candidate.is_file()
            ),
            None,
        )
        if command_file is None:
            raise FileNotFoundError(
                f"{slug}: no generated, previously published, or committed command JSON"
            )
        commands = read_json(command_file)["commands"]
        copy_if_exists(source, work / "model.py")
        copy_if_exists(command_file, work / "solidcraft.json")

        fresh_native = (
            native_root / slug
            if run_verification is not None
            and native_root is not None
            and (native_root / slug).is_dir()
            else None
        )
        if fresh_native is not None:
            model_verification = dict(run_verification)
            model_verification.update({
                "model": slug,
                "input_fingerprint": input_fingerprint(slug),
            })
            native_source = fresh_native
            native_origin = "current"
        elif stored is not None:
            model_verification = stored["verification"]
            native_source = stored["native"]
            native_origin = "stable"
        else:
            model_verification = None
            native_source = None
            native_origin = None

        screenshot = (
            native_source / "model.png"
            if native_source is not None
            and (native_source / "model.png").is_file()
            and (native_source / "model.png").stat().st_size
            else None
        )
        native_file = (
            native_source / "model.sc"
            if native_source is not None
            else None
        )
        has_native = (
            model_verification is not None
            and native_file is not None
            and native_file.is_file()
            and zipfile.is_zipfile(native_file)
        )
        if has_native:
            file_format = native_document_format(native_file)
            declared_format = model_verification.get("native_file_format")
            if declared_format is not None and declared_format != file_format:
                raise ValueError(
                    f"{slug}: verification format {declared_format!r} "
                    f"does not match native file {file_format!r}"
                )
            model_verification = dict(model_verification)
            model_verification["native_file_format"] = file_format
            model_verifications[slug] = model_verification
            verified_models.append(slug)
            verified_count += 1
            copy_if_exists(model_verification and native_source / "model.png", work / "native.png")
            copy_if_exists(native_file, work / "model.sc")
            (work / "verification.json").write_text(
                json.dumps(model_verification, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

        # A preview may still show the last published screenshot when this
        # resolved build has no current native image. It is presentation only:
        # the page never marks that older screenshot as verified for this run.
        previously_verified = None
        if not has_native and previous_site is not None and slug != "sample-plate":
            prior = previous_site / "models" / slug / "native.png"
            if prior.is_file() and prior.stat().st_size:
                previously_verified = prior
        preview_image = screenshot or previously_verified
        if preview_image is not None and not (work / "native.png").is_file():
            copy_if_exists(preview_image, work / "native.png")

        engine_version = (
            model_verification.get("solidcraft_version")
            if model_verification is not None
            else None
        )
        scpf_release = (
            model_verification.get("scpf_release")
            if model_verification is not None
            else None
        )
        model_source_commit = (
            model_verification.get("source_commit")
            if model_verification is not None
            else None
        )

        browser_controls = ""
        if has_native:
            model_url = f"{public_base}/models/{slug}/model.sc"
            encoded_url = quote(model_url, safe="")
            full_url = f"{SOLIDCRAFT_WEB}?open={encoded_url}"
            # The model page deliberately does NOT embed SolidCraft.
            # A direct outbound link makes it clear to visitors that they
            # leave GitHub Pages and load a different provider's web app.
            browser_controls = (
                '<section class="panel browser-open">'
                '<h2>Open this model in SolidCraft Web</h2>'
                '<p>The native editable model is available in SolidCraft’s '
                'official web application, hosted at '
                '<strong>docs.solidcraft.io</strong>.</p>'
                '<p><strong>External website:</strong> selecting the link '
                'below opens the SolidCraft website in a new tab. '
                'Your browser downloads the web application from '
                'SolidCraft’s servers, which generates network traffic '
                'for SolidCraft. The .sc model itself is hosted here on '
                'our GitHub Pages site. We do not embed the application.</p>'
                '<div class="links">'
                f'<a class="btn" href="{esc(full_url)}" target="_blank" '
                'rel="noopener noreferrer" '
                'aria-label="Open model on external website docs.solidcraft.io">'
                'Open in SolidCraft Web (external website)</a>'
                '<a class="btn secondary" href="model.sc" download>'
                'Download native .sc</a>'
                '</div><p class="small muted">You are leaving '
                'brainboxemb.github.io for docs.solidcraft.io. '
                'If you prefer not to use the external web app, download '
                'the native .sc file and open it locally in the matching '
                'SolidCraft release.'
                '</p></section>'
            )
        photo = (
            '<a class="preview-fullsize" href="native.png" '
            'target="_blank" rel="noopener noreferrer" '
            'aria-label="Open native CAD screenshot at full size">'
            '<img src="native.png" alt="Native SolidCraft CAD model, '
            'full-size image available"></a>'
            if preview_image else diagram(slug)
        )
        # Publish model-specific reference/native views next to the main render.
        extra_views = ""
        if slug == "simple-mft":
            expectation = ROOT / "models/advanced/simple_mft/expected-top-view.svg"
            if not expectation.is_file():
                raise FileNotFoundError(
                    f"Missing Simple MFT 2D expectation: {expectation}"
                )
            copy_if_exists(expectation, work / "expected-top-view.svg")
            reference_image = (
                "https://cdn.myshoptet.com/usr/www.craftmaker.nl/"
                "user/documents/upload/Product_description/"
                "craftmaker_pro_station_s30_accessories.jpg"
            )
            extra_views = (
                '<h2>Reference and 2D expectation</h2>'
                '<div class="panel-views">'
                '<figure><a href="' + reference_image + '" target="_blank" '
                'rel="noopener noreferrer">'
                '<img src="' + reference_image + '" '
                'alt="CRAFTMAKER ProStation S30 reference worktop"></a>'
                '<figcaption>Front product reference used to estimate the '
                'hole and Slot pattern.</figcaption></figure>'
                '<figure><a href="expected-top-view.svg" target="_blank" '
                'rel="noopener noreferrer">'
                '<img src="expected-top-view.svg" '
                'alt="Simple MFT expected top view"></a>'
                '<figcaption>2D expectation: nominal 9 × 7 grid at 76 mm pitch, '
                'four diagonal ring-2 holes omitted, with two Slots per quadrant.</figcaption></figure>'
                '</div>'
                '<p class="small muted">The 76 mm pitch, 20 mm corner cuts '
                'and ≈104 × 24 mm Slot dimensions are photo-based estimates, '
                'not manufacturer specifications.</p>'
            )
        if slug == "hub75-panel" and has_native:
            faces = []
            for title, filename in (("Front — LED mask", "front.png"),
                                    ("Rear — pockets and mounting bores", "rear.png")):
                candidate = native_source / filename
                if not candidate.is_file() or not candidate.stat().st_size:
                    raise ValueError(f"Verified HUB75 face view is missing: {candidate}")
                copy_if_exists(candidate, work / filename)
                faces.append(
                    f'<figure><a href="{filename}" target="_blank" rel="noopener">'
                    f'<img src="{filename}" alt="Native SolidCraft {esc(title)}">'
                    f'</a><figcaption>{esc(title)}</figcaption></figure>'
                )
            extra_views = ('<h2>Front and rear of the same local component</h2>'
                           '<div class="panel-views">' + ''.join(faces) + '</div>'
                           '<p class="small muted">Both are native SolidCraft '
                           'snapshots of the same single-component design.</p>')
        version_label = (
            f"SolidCraft {engine_version} · verified"
            if has_native and engine_version else
            "SolidCraft native version not verified"
        )
        if has_native:
            short_source = (model_source_commit or "")[:8]
            status = (
                "Native verified · current build"
                if native_origin == "current"
                else f"Native verified · stored build {short_source}"
            )
        elif previously_verified:
            status = "Older native render · not verified for current source"
        else:
            status = "Command plan only · native output not verified"
        badge = "verified" if has_native else "pending"
        stage_summary = "".join(f"<li>{esc(s)}</li>" for s in info["stages"])
        launcher_code = esc(source.read_text(encoding="utf-8"))
        component_path = COMPONENT_SOURCES.get(slug)
        if component_path is None:
            # Self-contained models have only one source file.
            python_source = f"<h2>Python model</h2><pre><code>{launcher_code}</code></pre>"
            source_links = '<a class="btn" href="model.py">SCPF source</a>'
        else:
            component_file = ROOT / component_path
            if not component_file.is_file():
                raise FileNotFoundError(f"Missing shared CAD component: {component_file}")

            component_code = esc(component_file.read_text(encoding="utf-8"))
            component_label = esc(component_path)
            direct_component_root = source.resolve() == component_file.resolve()

            if direct_component_root:
                # The published model.py is simply the exact reusable component
                # source compiled by SCPF. Do not invent a launcher section.
                python_source = (
                    '<section class="source-section source-definition">'
                    '<h2>Python component — actual geometry</h2>'
                    f'<p><code>{component_label}</code> is compiled directly by SCPF '
                    'and imported unchanged by assemblies. There is no launcher or '
                    'standalone wrapper model.</p>'
                    '<p><a class="btn secondary" href="model.py">'
                    'Download component source</a></p>'
                    f'<pre><code>{component_code}</code></pre></section>'
                )
                source_links = (
                    '<a class="btn" href="model.py">Component source</a>'
                )
            else:
                # Assembly pages show both their composition script and the
                # shared component geometry they import.
                downloadable = "source/" + component_path
                copy_if_exists(component_file, work / downloadable)
                definition_section = (
                    '<section class="source-section source-definition">'
                    '<h2>Python component — actual geometry</h2>'
                    f'<p>The sketch, extrusion, fillets and other editable CAD features live in '
                    f'<code>{component_label}</code>. This file is reused by other models.</p>'
                    f'<p><a class="btn secondary" href="{downloadable}">Download component source</a></p>'
                    f'<pre><code>{component_code}</code></pre></section>'
                )
                launcher_section = (
                    '<section class="source-section source-launcher">'
                    '<h2>Model script — how the component is used</h2>'
                    '<p><code>model.py</code> is the assembly entry point. It imports '
                    'and places the shared definition; it is not a second copy of '
                    'the component geometry.</p>'
                    '<p><a class="btn secondary" href="model.py">'
                    'Download model.py</a></p>'
                    f'<pre><code>{launcher_code}</code></pre></section>'
                )
                python_source = (
                    definition_section + launcher_section
                    if slug in COMPONENT_DEFINITION_PRIMARY
                    else launcher_section + definition_section
                )
                source_links = (
                    f'<a class="btn" href="{downloadable}">Actual component source</a>'
                    '<a class="btn secondary" href="model.py">Model entry point</a>'
                )
        # When the CAD project has an independent, manually authored SCPC
        # variant, publish BOTH Python scripts and both command plans.
        # Never fabricate SCPC code by exporting or decompiling SCPF JSON.
        scpc_source_block = ""
        if slug in COMMAND_SOURCES:
            native_script = source_path(ROOT, slug, "scpc")
            if not native_script.is_file():
                raise ValueError(f"Missing SCPC model for {slug}")
            copy_if_exists(native_script, work / "scpc-model.py")
            generated_scpc_plan = (
                generated_root / slug / "scpc" / "solidcraft.json"
                if generated_root is not None
                else None
            )
            stored_scpc_plan = (
                stored["generated"] / "scpc" / "solidcraft.json"
                if stored is not None
                else None
            )
            previous_scpc_plan = (
                previous_site / "models" / slug / "scpc-commands.json"
                if previous_site is not None
                else None
            )
            committed_scpc_plan = native_script.parent / "solidcraft.json"
            scpc_plan = next(
                (
                    candidate
                    for candidate in (
                        generated_scpc_plan,
                        stored_scpc_plan,
                        previous_scpc_plan,
                        committed_scpc_plan,
                    )
                    if candidate is not None and candidate.is_file()
                ),
                None,
            )
            if scpc_plan is None:
                raise ValueError(f"Missing independently compiled SCPC JSON for {slug}")
            copy_if_exists(scpc_plan, work / "scpc-commands.json")
            scpc_source_block = (
                '<section class="source-section scpc-source">'
                '<h2>SCPC — explicit native SolidCraft commands</h2>'
                '<p>This is an independent second implementation using '
                '<code>Script.add("native.command", ...)</code>. '
                'It does not call SCPF or re-export its generated JSON. '
                'Both versions are checked against the native CAD engine.</p>'
                '<div class="links"><a class="btn secondary" href="scpc-model.py">'
                'Download SCPC model.py</a>'
                '<a class="btn secondary" href="scpc-commands.json">'
                'SCPC command JSON</a></div>'
                f'<pre><code>{esc(native_script.read_text(encoding="utf-8"))}</code></pre>'
                '</section>'
            )
            source_links += ('<a class="btn secondary" href="scpc-model.py">'
                             'SCPC native-command script</a>')
        warning = info.get("warning")
        warning_html = ""
        if warning:
            warning_html = (
                '<section class="model-warning" role="note">'
                f'<strong>{esc(warning["title"])}</strong>'
                f'<p>{esc(warning["body"])}</p>'
                '</section>'
            )

        view = f"""<section class="hero cad-hero"><div class="wrap"><div class="eyebrow">CAD design / {esc(slug)}</div>
<h1>{esc(info["title"])}</h1><p>{esc(info["tagline"])}</p></div></section>
<main class="wrap"><div class="metadata"><span class="badge {badge}">{esc(status)}</span>
<span class="badge">{len(commands)} commands</span><span class="badge">{esc(info["parameters"])}</span><span class="badge">{esc(version_label)}</span></div>
{warning_html}
<div class="two model-preview-layout"><section class="panel"><h2>Model preview</h2><div class="picture">{photo}</div>
<p class="small muted">{"Verified native SolidCraft image. See verification metadata below for the exact source and tool versions. Click to view full size." if has_native else "Previously verified SolidCraft render from main; this PR revision is not yet native-verified. Click to view full size." if previously_verified else "Schematic drawing only; it is not a SolidCraft geometry render."}</p>
<p>{esc(info["description"])}</p></section>
<section class="panel"><h2>Files</h2><p>Download the original Python sources and generated command plan.</p>
<div class="links">{source_links}<a class="btn secondary" href="solidcraft.json">Command JSON</a>
</div>
<p class="small muted">Command JSON describes CAD actions; it is not an already-saved .sc design.</p>
<h3>Construction stages</h3><ol>{stage_summary}</ol></section></div>
{browser_controls}
{extra_views}
{python_source}
{scpc_source_block}
<h2>Native SolidCraft command sequence (SCPF)</h2><section class="panel"><ol class="timeline">{command_stages(commands)}</ol></section>
<div class="notice"><strong>Verification:</strong> {esc(status)}.
The source and JSON here are from this checkout. Native qualification is reported only when the stored input fingerprint matches the current model inputs. Exact source and tool versions are recorded in this model's verification.json.</div>
<p><a href="../../">← Back to all models</a></p></main>"""
        (work / "index.html").write_text(
            layout(info["title"], view, "../../results.css", "../../"),
            encoding="utf-8",
        )
        group = next(key for key, (_, _, names) in SECTIONS.items() if slug in names)
        card = f"""<article class="card"><div class="picture">{f'<img src="models/{slug}/native.png" alt="SolidCraft model render">' if preview_image else diagram(slug)}</div>
<div class="inside"><span class="badge {badge}">{'Native verified' if has_native else 'Older native render — not current verification' if previously_verified else 'Command plan only'}</span>
<h3><a href="models/{slug}/">{esc(info["title"])}</a></h3><p>{esc(info["tagline"])}</p>
<p class="small muted">{esc(info["parameters"])}</p>
<a class="btn" href="models/{slug}/">Explore model →</a></div></article>"""
        category_cards[group].append(
            card.replace(f"models/{slug}/", f"../{slug}/")
        )
        if info.get("featured", True):
            cards[group].append(card)
    sections_html = "".join(
        f'<section class="model-category" id="{key}"><h2>{esc(title)}</h2>'
        f'<p class="muted">{esc(description)}</p>'
        f'<p><a href="models/{key}/">Browse all {esc(title.lower())} →</a></p>'
        f'<div class="grid">{"".join(cards[key])}</div></section>'
        for key, (title, description, _names) in SECTIONS.items()
    )

    # Category pages list every model in that section, independent of the
    # curated home-page featured flag.
    for key, (title, description, _names) in SECTIONS.items():
        category = out / "models" / key
        category.mkdir(parents=True, exist_ok=True)
        category_body = f"""<section class="hero cad-hero"><div class="wrap">
<div class="eyebrow">CAD model category</div><h1>{esc(title)}</h1>
<p>{esc(description)}</p></div></section>
<main class="wrap"><p><a href="../../">← Back to model overview</a></p>
<div class="grid">{"".join(category_cards[key])}</div></main>"""
        (category / "index.html").write_text(
            layout(title, category_body, "../../results.css", "../../"),
            encoding="utf-8",
        )
    home = f"""<section class="hero cad-hero"><div class="wrap"><div class="eyebrow">SCPF · SolidCraft</div>
<h1>CAD models, from readable code to native geometry</h1>
<p>Explore {len(MODELS)} CAD designs and their construction stages. Python SCPF emits native SolidCraft commands; SolidCraft creates the final BRep model.</p></div></section>
<main class="wrap"><section class="intro"><h2>Getting started</h2><p>New to SCPF? <a href="{LIBRARY_CHEATSHEET}">Open the SCPF cheatsheet</a> for 2D/3D primitives, operations and examples.</p><h2>Model catalog</h2>
<p>Each model has its Python source, generated command JSON and a readable operation timeline. The link to SolidCraft Web and a downloadable .sc file are user actions only; they are not evidence that a model is verified.</p>
<h3>Verification status</h3>
<ul>
<li><strong>Native verified</strong> — CI executed the model in SolidCraft and produced a real editable .sc file. Its verification fingerprint still matches the current geometry/source inputs, and the shown native screenshot belongs to that verified output.</li>
<li><strong>Older native render — not verified for current source</strong> — an older published SolidCraft screenshot is shown only as a visual reference. It is not proof that the current source revision has been verified.</li>
<li><strong>Command plan only — native output not verified</strong> — the SCPF command plan is available, but there is no matching native SolidCraft result accepted for the current geometry/source inputs.</li>
</ul>
<p>Nothing from the external CAD application loads automatically on this site. PR previews may reuse an older main render only when it is clearly marked as not current verification.</p>
<p><span class="badge">{len(MODELS)} models</span> <span class="badge verified">{verified_count} native verified</span></p></section>
{sections_html}<h2>How it works</h2>
<div class="two"><section class="panel"><h3>1 · Write the model</h3><p>Use a plain Python class and a <code>build()</code> method, without a mandatory <code>show()</code> and with an explicit <code>return</code>.</p>
<h3>2 · Compile commands</h3><p>SCPF outputs native SolidCraft commands, with named parameters and a sequence of CAD operations.</p></section>
<section class="panel"><h3>3 · Execute in SolidCraft</h3><p>The SolidCraft engine creates editable geometry, and CI validates its results. CAD and verification assets are only published when they match the source revision.</p>
<h3>4 · Inspect the result</h3><p>Review the command timeline, native measurements and optional rendered preview. An unverified model is labelled as such.</p></section></div>
<p class="small muted">Catalog source revision: <code>{esc(commit)}</code><br>
Current SCPF dependency: <a href="https://github.com/brainboxemb/lib.py.solidcraft.forge/commit/{esc(scpf_commit)}"><code>{esc(scpf_commit)}</code></a><br>
Current SCPC dependency: <a href="https://github.com/brainboxemb/lib.py.solidcraft.cmd/commit/{esc(scpc_commit)}"><code>{esc(scpc_commit)}</code></a><br>
Each native model page records the exact Forge, SolidCraft and source revision used for that model.</p></main>"""
    provenance = {
        "schema": 2,
        "source_commit": commit,
        "catalog_commit": commit,
        "scpf_commit": scpf_commit,
        "scpc_commit": scpc_commit,
        "native_verified_models": verified_models,
        "models": model_verifications,
    }
    for key in (
        "scpf_release",
        "solidcraft_version",
        "native_file_format",
    ):
        values = {
            row.get(key)
            for row in model_verifications.values()
            if row.get(key) is not None
        }
        if len(values) == 1:
            provenance[key] = values.pop()
    (out / "provenance.json").write_text(
        json.dumps(provenance, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "index.html").write_text(
        layout("Models", home, "results.css", "./"), encoding="utf-8"
    )
    redirect_legacy_cheatsheet(out)
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built {len(MODELS)} CAD result pages in {out} ({verified_count} native screenshots)")



LIBRARY_CHEATSHEET = "https://brainboxemb.github.io/lib.py.solidcraft.forge/cheatsheet/"


def redirect_legacy_cheatsheet(out):
    """Keep bookmarked CAD cheat URLs working without duplicating the API."""
    dest = out / "cheatsheet"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta http-equiv="refresh" content="0; url=' + LIBRARY_CHEATSHEET + '">'
        '<link rel="canonical" href="' + LIBRARY_CHEATSHEET + '">'
        '<title>SCPF cheatsheet moved to library</title></head><body>'
        '<p>The API cheatsheet lives in the '
        '<a href="' + LIBRARY_CHEATSHEET + '">SCPF library</a>.</p>'
        '</body></html>',
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--native", type=Path)
    parser.add_argument("--previous-site", type=Path,
                        help="Published main site renders for non-verified previews")
    parser.add_argument("--generated", type=Path,
                        help="Root of freshly compiled output/models")
    parser.add_argument("--stable-store", type=Path,
                        help="build/main root containing source-mirrored model output")
    parser.add_argument("--public-base", default=PUBLIC_SITE,
                        help="Published base URL used by external SolidCraft open links")
    args = parser.parse_args()
    build(
        args.out,
        args.commit,
        args.native,
        args.generated,
        args.previous_site,
        args.stable_store,
        args.public_base,
    )


if __name__ == "__main__":
    main()
