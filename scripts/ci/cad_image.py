#!/usr/bin/env python3
"""Resolve immutable CAD CI image metadata from versioned toolchain inputs.

Only dependencies baked into the image contribute to its identity. Repository
tools such as tool.cad.ci are mounted from ext/ at runtime and must not trigger
an expensive SolidCraft image rebuild when their pin changes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE = ROOT / "docker" / "cad" / "Dockerfile"
TOOLCHAIN = ROOT / "ci" / "toolchain.json"
DEPENDENCIES = ROOT / "dependencies.repos"
SELF = Path(__file__).resolve()


def load_toolchain() -> dict:
    """Read the fixed Python/SolidCraft versions used by the CAD image."""

    data = json.loads(TOOLCHAIN.read_text(encoding="utf-8"))
    if data.get("schema") != 1:
        raise ValueError("unsupported CAD toolchain schema")
    missing = sorted({"python_image", "solidcraft"} - set(data))
    if missing:
        raise ValueError("missing CAD toolchain fields: " + ", ".join(missing))
    return data


def dependency(name: str) -> tuple[str, str]:
    """Return one exact external URL/SHA pair from dependencies.repos."""

    text = DEPENDENCIES.read_text(encoding="utf-8")
    section = re.search(
        rf"(?ms)^  {re.escape(name)}:\s*\n(.*?)(?=^  [\w-]+:|\Z)",
        text,
    )
    if section is None:
        raise ValueError(f"missing {name} in dependencies.repos")
    url = re.search(r"(?m)^    url:\s*(\S+)\s*$", section[1])
    sha = re.search(r"(?m)^    version:\s*([0-9a-f]{40})\s*$", section[1])
    if url is None or sha is None:
        raise ValueError(f"{name} requires an exact URL and 40-character SHA")
    return url[1], sha[1]


def image_id() -> str:
    """Hash only inputs that are actually installed in the image."""

    digest = hashlib.sha256()
    for path in (DOCKERFILE, TOOLCHAIN, SELF):
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")

    # SCPF and SCPC are installed by docker/cad/Dockerfile. Other entries in
    # dependencies.repos are runtime repository tools and do not belong here.
    for name in ("scpf", "scpc"):
        url, sha = dependency(name)
        digest.update(f"dependency:{name}".encode("utf-8"))
        digest.update(b"\0")
        digest.update(url.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha.encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def metadata(repository: str) -> dict[str, str]:
    """Return image names, versions and exact library pins for Actions."""

    toolchain = load_toolchain()
    scpf_url, scpf_sha = dependency("scpf")
    scpc_url, scpc_sha = dependency("scpc")
    python_match = re.search(r"python:(\d+\.\d+)", toolchain["python_image"])
    if python_match is None:
        raise ValueError("python_image must contain a major.minor Python tag")

    digest = image_id()
    image = f"ghcr.io/{repository.lower()}/cad-ci"
    solidcraft = str(toolchain["solidcraft"])
    python_version = python_match.group(1)
    return {
        "image": image,
        "image_id": digest,
        "reference": f"{image}:toolchain-{digest}",
        "alias": f"{image}:sc-{solidcraft}-py-{python_version}",
        "python": python_version,
        "python_image": str(toolchain["python_image"]),
        "solidcraft": solidcraft,
        "scpf_url": scpf_url,
        "scpf_sha": scpf_sha,
        "scpc_url": scpc_url,
        "scpc_sha": scpc_sha,
    }


def write_github_output(path: Path, values: dict[str, str]) -> None:
    """Append resolved values using the GitHub Actions output-file format."""

    with path.open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    """Print image metadata and optionally expose it to a workflow step."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()

    values = metadata(args.repository)
    for key, value in values.items():
        print(f"{key}={value}")
    if args.github_output:
        write_github_output(args.github_output, values)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
