# Repository plan

This file contains unfinished work only.

## Now

### #1 — final historical catalog migration

Accepted stages:

1. one real physical owner;
2. five real physical owners;
3. ten real physical owners;
4. accepted template catalog presentation synced;
5. accepted primary snapshot-camera and physical dependency contracts synced;
6. accepted build-branch artifact ownership fix synced.

Current stage migrates the six remaining historical physical roots:

- `corner-bracket`;
- `hub75-panel`;
- `hub75-screen`;
- `hub75-wood-frame` — Hub75DisplayCase;
- `hub75-display2` — Hub75DisplayCase v2;
- `simple-mft` — standalone + assembly variants.

The final PR deliberately selects all sixteen real physical owners so the whole
migrated catalog is accepted together.

## Dependency graph

Explicit physical-owner edges used by the final batch:

- `hub75-screen` -> `hub75-panel`;
- `hub75-wood-frame` -> `hub75-panel`, `corner-bracket`;
- `hub75-display2` -> `hub75-panel`, `corner-bracket`;
- `simple-mft` -> `guide-rail`.

Directory priorities remain ordering metadata only:

```text
models/basic       10
models/components  20
models/advanced    30
```

## Migration boundaries

The historical repository remains the source for current geometry and open
model-design issues until this batch is accepted.

Do not silently solve open geometry work during transfer:

- CornerBracket #362 remains separate;
- Bolted Flange #135 remains separate;
- DisplayCase path/id rename #417 remains separate.

The current ids `hub75-wood-frame` and `hub75-display2` stay stable during
migration even though their presentation titles are Hub75DisplayCase and
Hub75DisplayCase v2.

Generated CAD artifacts remain owned exclusively by the generated `build`
branch. Pages links them and does not copy them into `gh-pages`.

## Next

Accept the complete sixteen-owner catalog on PR, durable `dev`, build
publication and Pages. Then migrate the remaining open issues and relevant open
pull requests from the historical repository.
