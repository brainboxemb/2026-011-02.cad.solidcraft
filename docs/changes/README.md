# Change design records

Structural CAD-library changes are recorded here before or together with implementation.

Naming:

```text
NNNN-short-change-name.md
```

Rules:

- four-digit, monotonically increasing number;
- one design/change per document;
- link the matching GitHub issue;
- describe the problem, decision, repository/API/CI contract and verification;
- implementation follows the recorded decision;
- later changes add a new record instead of rewriting an older decision.

Current records:

- [0001-targeted-model-builds.md](0001-targeted-model-builds.md) — targeted model selection, per-model verified output and incremental publication (#129).
- [0002-tested-ci-orchestration.md](0002-tested-ci-orchestration.md) — move selection, model checks and publication policy out of workflow YAML into tested Python (#134).
- [0003-reusable-cad-ci-image.md](0003-reusable-cad-ci-image.md) — build and reuse one immutable CAD/SolidCraft/SCPF/SCPC CI toolchain image (#136).
- [0004-concurrent-generated-publication.md](0004-concurrent-generated-publication.md) — retry generated-branch publication safely when CAD cleanup or promotion races (#138).
- [0005-host-owned-stable-pages-workspace.md](0005-host-owned-stable-pages-workspace.md) — build/test stable Pages in a host-owned temporary workspace (#139).
