# template.cad.model-project

Self-contained template for CAD model repositories.

Models and Python capabilities are independent build items.

```text
ci.yml
build.yml

modules/
  ci/
    ci.yml
    pyproject.toml
    src/
    tests/
  build/
    ci.yml
    pyproject.toml
    src/
    tests/
  merge-policy/
    ci.yml
    pyproject.toml
    src/
    tests/

models/
  simple-box/
    ci.yml
    model.yml
    scpf/model.py

build/                  # generated, ignored
```

## Selection

`ci.yml` is stable project configuration and contains the exact Forge pin.

`build.yml` is the current branch's execution plan. A module-only PR selects
only that module; a model-only PR selects only that model.

`main` ignores `build.yml` and runs the complete repository.

## Branches

- short-lived branch -> `dev`: squash;
- `dev` -> `main`: merge commit;
- `main` -> `dev`: merge commit.
