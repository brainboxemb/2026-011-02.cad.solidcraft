# CAD result and provenance pipeline

The CAD site is generated from build evidence. It must never infer a native
verification result from filenames, screenshots or hardcoded engine versions.

## Evidence flow

```text
CAD source + dependency pins
        |
        v
SCPF / SCPC command generation
        |
        v
SolidCraft native run
        |
        +--> model.sc / STEP / measurements / screenshots
        |
        +--> output/native/verification.json
                    |
                    v
           scripts/ci/build-results.py
                    |
                    +--> static model pages
                    +--> provenance.json
                    |
                    v
           scripts/ci/test-results.py
```

## `verification.json`

This file belongs to one native CI run and is the authority for native
verification identity. It records:

- CAD source commit;
- exact SCPF commit;
- SCPF semantic release;
- exact SCPC commit;
- SolidCraft release;
- workflow run id;
- `verified: true`.

The static-site builder accepts native screenshots and editable `.sc` files
only when this metadata matches the current source and pinned library commits.

## Native SolidCraft file format

The internal document format stored inside a SolidCraft `.sc` archive, for
example `solidcraft/57`, is an engine implementation detail. The site must not
map a particular SolidCraft release to a hardcoded format number.

Instead the builder:

1. requires `document.json.format` to match `solidcraft/<number>`;
2. requires every published native model from one verification run to use the
   same document format;
3. records that observed format in `provenance.json`;
4. separately records the qualified SolidCraft release from
   `verification.json`.

The container format remains explicitly checked as
`solidcraft-container/1`.

## `provenance.json`

The published site records the evidence it actually used:

- source commit;
- SCPF release and exact commit;
- exact SCPC commit;
- SolidCraft release;
- observed native document format;
- workflow run;
- list of source-matched native-verified models.

This makes the generated page auditable without embedding version assumptions
in its HTML generator.

## Pull-request previews

A PR preview may reuse an older published screenshot only as a clearly labelled
illustration. Such a screenshot is not native evidence for the PR and must not
cause a native `.sc` file, SolidCraft Web link or verified badge to be
published for that model.

## Main publication

The verified site is published from `main` only after the native workflow
succeeds. The site smoke tests verify provenance and native archive consistency
before GitHub Pages publication.
