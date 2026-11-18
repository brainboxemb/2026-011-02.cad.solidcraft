# 0004 — Concurrent generated publication

**Tracks:** issue #138  
**Scope:** writes to the generated `build` and `gh-pages` branches.

## Problem

A merge creates two legitimate CAD operations close together:

- the main run promotes verified output and rebuilds stable Pages;
- the closed-PR path removes that PR's build and Pages preview.

Both may update the same generated branch after checking out the same older
commit. A normal push from the second writer can therefore be rejected as
non-fast-forward even when the changes are independent.

## Decision

Generated branches use optimistic concurrency with normal pushes.

After preparing and committing a generated change:

1. push normally;
2. when the push is rejected, fetch the current target branch;
3. rebase the prepared commit onto `origin/<branch>`;
4. retry the normal push;
5. stop after a small bounded number of attempts.

A real rebase conflict fails the publication. Do not force-push generated
branches and do not drop the other writer's change.

This rule applies equally to `build` and `gh-pages`.

## Result

Stable promotion and closed-PR cleanup may run independently. For example,
removing `build/pr/137` must be preserved while a concurrent stable run
migrates or updates `build/main`.

## Verification

Unit tests prove that a rejected first push causes fetch + rebase + retry and
that publication fails clearly after the bounded retry count.
