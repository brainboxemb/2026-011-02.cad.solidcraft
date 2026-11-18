# 0003 — Reusable immutable CAD CI image

**Tracks:** issue #136  
**Scope:** CAD/native toolchain setup, immutable image identity and verification metadata.

## Problem

Every CAD/native run currently repeats the same heavy setup: Python, vcs2l,
SCPF/SCPC checkout/install and SolidCraft download/verification.

## Decision

Build one immutable CAD CI toolchain image in a separate `image.yml` workflow.

The image contains only fixed toolchain inputs:

- pinned Python base image;
- required system libraries;
- repository-defined SolidCraft version;
- exact SCPF and SCPC revisions from `dependencies.repos`;
- fixed CI runtime dependencies.

CAD model source is not baked into the image.

Image identity is content-addressed from versioned toolchain inputs. A mutable
`latest` tag is never used as qualification identity.

Normal `cad.yml` and `native.yml` runs pull the image and execute only the
models selected by the build plan. A new image does not imply an `all` model
build.

Per-model `verification.json` records the immutable image reference/digest in
addition to exact SCPF, SCPC and SolidCraft versions.

## Verification

The image workflow smoke-tests Python, SolidCraft, SCPF and SCPC plus one small
representative SCPF compile/native operation before publication. Tests prove
which files participate in image identity and that model-source changes do not.
