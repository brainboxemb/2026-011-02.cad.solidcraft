# 0011 — Separate native verification from site metadata

Issue: #152

## Problem

The model site currently uses one input-path set for two different jobs:

1. deciding which model/site output must be rebuilt after a repository change;
2. deciding whether stored native SolidCraft verification still matches the
   current model geometry.

Those are not the same contract.

A README-only change must select the owning model page for republication, but it
must not invalidate an unchanged native .sc file and screenshot. The same
selection/fingerprint coupling caused existing verified models to lose their
"Native verified" status after model-root metadata was added to targeted CI.

The public labels are also too vague. "Published render" can be an older image
carried forward only as a visual reference and is not proof of current native
verification.

## Decision

Keep two explicit path sets:

- `verification_input_paths(slug)`
  - geometry/source inputs for the model and its declared geometry
    dependencies;
  - used only for the native verification fingerprint.

- `model_input_paths(slug)`
  - verification inputs plus model-root README/check metadata;
  - used for change selection and site/native reruns.

A check.py change still selects and reruns its owning model. README/check files
do not define the geometry fingerprint.

## Public status wording

The Models overview explains these states explicitly:

- **Native verified** — a real editable SolidCraft .sc exists and its
  verification fingerprint matches the current geometry/source inputs. The
  shown native screenshot belongs to that verified output.
- **Older native render — not verified for current source** — an older
  published screenshot is shown only for visual reference.
- **Command plan only — native output not verified** — the generated command
  plan exists, but no matching native SolidCraft result is accepted.

The external SolidCraft Web link and downloadable .sc are user actions, not
verification evidence.

The home-page model count comes from the central catalog; no literal model
count is written in prose.

## Verification

- README/check metadata changes leave `input_fingerprint()` unchanged.
- geometry/source changes change the fingerprint.
- README and check.py still select the owning model.
- the generated Models homepage explains all three statuses.
- cards and model pages use explicit old/unverified wording.
- model count text is derived from `len(MODELS)`.
