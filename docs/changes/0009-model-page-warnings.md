# 0009 — Model-page warnings from catalog metadata

Issue: #147

## Problem

The CAD results site is generated from the central model catalog. Model README
content is not rendered on the published detail page.

GuideRail therefore had a prominent source/verification warning in its README,
but the public `/models/guide-rail/` page could never display that text even
after the model was correctly selected and rebuilt.

## Decision

Add optional warning metadata to a catalog model:

```python
"warning": {
    "title": "...",
    "body": "...",
}
```

The results builder renders this metadata near the top of the model detail page,
before the preview.

Warnings are rendered as escaped text, not raw HTML. Styling is owned by the
site stylesheet and uses a red border/text with a light red background.

Models without warning metadata render no warning block.

GuideRail uses this mechanism for the TSO/reference-source warning.

## Verification

- GuideRail generated HTML contains the warning title and body;
- the warning block is visibly styled through the shared site CSS;
- models without warning metadata do not contain an empty warning section;
- static site smoke tests cover the generic warning contract.
