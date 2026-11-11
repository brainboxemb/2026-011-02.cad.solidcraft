# Interactive SolidCraft models from GitHub Pages

The CAD model pages can open the actual **native SolidCraft `.sc` design**
in the official SolidCraft browser app. That includes editable component
occurrences, sketches, feature history and joints; a STEP file or a screenshot
would not preserve the same design history.

## Where it runs

We do **not** self-host a second SolidCraft application.

- The **CAD website and model files** are on GitHub Pages.
- The **web CAD application** is SolidCraft's official stable
  [browser version](https://docs.solidcraft.io/app/).
- Each native-verified model page gets a download and two opt-in links:
  **Open in SolidCraft (browser)** and **Show embedded viewer**.
- The embedded view is a separate `viewer.html` page, so the large
  WebAssembly viewer does not start for everyone browsing the catalog.

This follows SolidCraft's official
[Design links and embeds](https://docs.solidcraft.io/guide/getting-started.html#design-links-and-embeds)
API: `?open=<HTTPS .sc URL>` and `?embed&open=<HTTPS .sc URL>`.

## Why the actual native .sc is published

SCPF's `solidcraft.json` is a *command plan*, not a saved design. Browser
`?open=` expects a real `.sc` document. The native CI creates it with

```bash
solidcraft-cli run commands.json --param-check strict \
    --results --save model.sc --out model.step
```

The site builder publishes `model.sc` **only after** the same commit and
SCPF library SHA are verified in `verification.json`, a native snapshot
exists, and the native `.sc` archive is checked:

- ZIP contains `document.json` in SolidCraft **`solidcraft/48`** format;
- ZIP contains `container.json` with `solidcraft-container/1`;
- the source/engine provenance is the same as the published model page.

In particular, a reused screenshot from an older build never enables a
new browser-open link.

## Example

For the wooden HUB75 model, GitHub Pages hosts:

```text
https://brainboxemb.github.io/2026-011-02.cad.solidcraft/models/hub75-wood-frame/model.sc
```

The model page constructs the full-app link by encoding that URL as the
`open` query argument of:

```text
https://docs.solidcraft.io/app/?open=...
```

The embedded viewer uses `?embed&open=...` and an iframe on a separate
page. Both have a plain `model.sc` download fallback.

## What still needs a real browser test

Publishing and opening across origins involves conditions that cannot be
proven just from command JSON:

1. GitHub Pages must serve `.sc` with **CORS** allowed for
   `https://docs.solidcraft.io`. Public Pages generally returns
   `Access-Control-Allow-Origin: *`, but confirm the header on the
   newly published binary.
2. The official app's CSP/iframe permissions must permit embedding, as
   indicated by SolidCraft's documentation.
3. The current official stable web engine must actually open
   `solidcraft/48` designs produced by our pinned CLI **0.30.1**.
4. Check at least the corner bracket and the five-panel wooden assembly
   interactively: component tree, feature history and orbit controls.

If direct opening succeeds but the iframe does not, keep the full app
link and download and remove/hide the embedded variant.

## When self-hosting would be useful

SolidCraft offers its own official Docker image
(`ghcr.io/tangency-labs/solidcraft-web`). Hosting that behind the
same origin as the `.sc` files eliminates cross-origin fetching and
allows control over headers/version pinning. That is justified **only if**
the documented public browser app and GitHub Pages cannot reliably
open/embed the verified files, or if we need to lock the web viewer to
an exact SolidCraft release.

A custom geometry viewer or second CAD engine is **not** needed.
