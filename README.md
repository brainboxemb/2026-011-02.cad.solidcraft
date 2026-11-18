# CAD build output

This branch stores verified technical CAD build output only.

- `main/<source-item-path>/` contains the last promoted successful main build.
- `pr/<number>/<source-item-path>/` contains isolated verified PR output.
- `<model-root>` mirrors the source model root, for example
  `models/basic/plate/`.
- Every built model directory carries its own `verification.json`.

The website lives on `gh-pages`. Do not edit generated build output by hand.
