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
- [0006-canonical-native-screenshot-filename.md](0006-canonical-native-screenshot-filename.md) — normalize migrated primary screenshots to `native/model.png` before stable Pages generation (#140).
- [0007-parallel-hub75-display2.md](0007-parallel-hub75-display2.md) — add HUB75Display2 as a separately evolvable advanced model alongside the existing wooden display (#142).
- [0008-model-root-input-selection.md](0008-model-root-input-selection.md) — select model-root README/check metadata without propagating it through geometry dependencies (#144).
- [0009-model-page-warnings.md](0009-model-page-warnings.md) — render optional model-specific warnings from catalog metadata on result pages (#147).
- [0010-stable-catalog-growth.md](0010-stable-catalog-growth.md) — automatically build/promote catalog models missing from the modern stable store (#150).
- [0011-native-verification-status.md](0011-native-verification-status.md) — separate geometry verification fingerprints from page metadata and explain public verification states (#152).
