# 0005 — Host-owned stable Pages workspace

**Tracks:** issue #139  
**Scope:** temporary workspace used while rebuilding stable Pages.

## Problem

CAD compilation and native verification run inside the immutable toolchain
container. The mounted `output/` tree can therefore be owned by the container
user.

Stable publication runs on the GitHub host. Building the final site under
`output/stable-site` made host publication depend on container filesystem
ownership and failed with `PermissionError`.

## Decision

The stable Pages build is a host-side publication step and uses a fresh
host-owned temporary directory.

The publisher:

1. promotes verified technical output to `build/main`;
2. creates a host temporary directory;
3. builds and tests the stable site there;
4. copies the tested site into the checked-out `gh-pages` tree;
5. discards the temporary directory.

Do not chmod/chown the complete Docker output tree just to publish Pages.
Do not move publication policy back into workflow shell.

## Verification

Unit tests prove that stable publication passes an explicit temporary output
path to the site builder and that this path is outside the container-owned
bundle/output directory.
