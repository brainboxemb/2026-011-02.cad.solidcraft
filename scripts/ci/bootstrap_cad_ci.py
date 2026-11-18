#!/usr/bin/env python3
"""Check out the exact tool.cad.ci revision used by this CAD repository.

SCPF and SCPC are Python libraries and are installed by bootstrap.ps1 or baked
into the CAD image. tool.cad.ci is different: it remains a repository tool and
is invoked through ext/cad-ci/cad-ci.py. Keeping that boundary avoids a name
collision with this repository's existing scripts/ci/cad_ci.py module.
"""

from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "dependencies.repos"
TARGET = ROOT / "ext" / "cad-ci"


def dependency(root: Path = ROOT) -> tuple[str, str]:
    """Return the cad-ci Git URL and exact 40-character revision."""

    text = (root / "dependencies.repos").read_text(encoding="utf-8")
    section = re.search(
        r"(?ms)^  cad-ci:\s*\n(.*?)(?=^  [\w-]+:|\Z)",
        text,
    )
    if section is None:
        raise RuntimeError("dependencies.repos has no cad-ci entry")

    url = re.search(r"(?m)^    url:\s*(\S+)\s*$", section[1])
    sha = re.search(r"(?m)^    version:\s*([0-9a-f]{40})\s*$", section[1])
    if url is None or sha is None:
        raise RuntimeError("cad-ci requires a Git URL and exact commit SHA")
    return url[1], sha[1]


def _git(target: Path, *args: str, check: bool = True) -> str:
    """Run Git for one external checkout and return stripped stdout."""

    completed = subprocess.run(
        ["git", "-C", str(target), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(message or "git command failed")
    return completed.stdout.strip()


def ensure_checkout(
    root: Path = ROOT,
    *,
    target: Path | None = None,
) -> str:
    """Make the external checkout match dependencies.repos exactly.

    Existing tracked changes are never overwritten. Untracked files are left
    alone because the exact tracked Git tree is what controls tool behaviour.
    """

    url, wanted = dependency(root)
    target = target or (root / "ext" / "cad-ci")
    target.parent.mkdir(parents=True, exist_ok=True)

    if (target / ".git").is_dir():
        current = _git(target, "rev-parse", "HEAD")
        if current != wanted:
            dirty = _git(target, "status", "--porcelain", "--untracked-files=no")
            if dirty:
                raise RuntimeError(
                    "ext/cad-ci has tracked local changes; preserve them before updating"
                )
            _git(target, "remote", "set-url", "origin", url)
            _git(target, "fetch", "origin", wanted)
            _git(target, "-c", "advice.detachedHead=false", "checkout", "--detach", wanted)
    else:
        if target.exists():
            raise RuntimeError(
                f"{target} exists but is not a Git checkout; move it aside first"
            )
        subprocess.run(
            ["git", "clone", "--quiet", "--no-checkout", "--", url, str(target)],
            check=True,
        )
        _git(
            target,
            "-c",
            "advice.detachedHead=false",
            "checkout",
            "--detach",
            wanted,
        )

    actual = _git(target, "rev-parse", "HEAD")
    if actual != wanted:
        raise RuntimeError(
            f"cad-ci revision mismatch: expected {wanted}, found {actual}"
        )
    return actual


def main() -> int:
    """Bootstrap the pinned tool and print the exact ready revision."""

    actual = ensure_checkout()
    print(f"Ready: cad-ci at {actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
