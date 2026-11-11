"""Verify that vcs2l checked out *both* exact library revisions.

The declarative manifest remains dependencies.repos; this lightweight
reader handles only its explicit two-repository form, not arbitrary YAML.
"""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
text = (ROOT / "dependencies.repos").read_text(encoding="utf-8")

for name in ("scpf", "scpc"):
    section = re.search(
        rf"(?ms)^  {re.escape(name)}:\s*\n(.*?)(?=^  [\w-]+:|\Z)", text
    )
    if not section:
        raise SystemExit(f"Missing {name} in dependencies.repos")
    sha = re.search(r"(?m)^    version:\s*([0-9a-f]{40})\s*$", section[1])
    if not sha:
        raise SystemExit(f"Missing exact SHA for {name}")
    actual = subprocess.check_output(
        ["git", "-C", str(ROOT / "ext" / name), "rev-parse", "HEAD"],
        text=True
    ).strip()
    if actual != sha[1]:
        raise SystemExit(f"{name} revision mismatch: expected {sha[1]}, got {actual}")
    print(f"{name}: {actual}")
