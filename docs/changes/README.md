# Change design records

Structural CAD-library changes are recorded here before implementation when a
change affects model behavior, modeling intent, repository contracts or other
decisions that should be reviewed independently from code.

Naming:

```text
NNNN-short-change-name.md
```

Rules:

- use a four-digit, monotonically increasing number;
- keep one logical design/change per document;
- link the matching GitHub issue;
- start new records with `Status: Proposed`;
- describe the problem before selecting an implementation;
- record physical/modeling intent, scope, non-goals and verification;
- call out unresolved capability questions explicitly;
- implementation starts only after the record is explicitly approved;
- change `Status: Proposed` to `Status: Approved` when that approval is given;
- later decisions add a new record instead of rewriting accepted historical
  decisions.

## History

Records 0001 through 0040 remain historical evidence in the archived repository
`brainboxemb/2026-011-02.cad.solidcraft.OLD`. Numbering continues from that
history after the catalog migration; those records are not copied into this
repository.

## Current records

- [0041-hub75-tube-clamp-installed-state.md](0041-hub75-tube-clamp-installed-state.md)
  — define a physically meaningful Free/Installed contract for the reusable
  HUB75 tube clamp before implementation (#281).
