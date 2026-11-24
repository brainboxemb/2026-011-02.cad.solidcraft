"""Publish one complete generated site to the configured Pages branch."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

import yaml


class PagesPublishError(RuntimeError):
    """Pages publication failed."""


def _run(
    command: list[str],
    *,
    cwd: Path,
    check: bool = True,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
    )


def _load_pages_branch(repo: Path) -> str:
    data = yaml.safe_load((repo / "ci.yml").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise PagesPublishError("ci.yml must be a mapping")
    generated = data.get("generated")
    if not isinstance(generated, dict):
        raise PagesPublishError("ci.yml.generated must be a mapping")
    value = generated.get("pages_branch")
    if not isinstance(value, str) or not value:
        raise PagesPublishError("ci.yml.generated.pages_branch is required")
    return value


def _remote_sha(repo: Path, ref: str) -> str | None:
    result = _run(
        ["git", "ls-remote", "--heads", "origin", f"refs/heads/{ref}"],
        cwd=repo,
    )
    line = result.stdout.strip()
    return line.split()[0] if line else None


def _require_fresh_source(repo: Path, source_ref: str, source_sha: str) -> None:
    actual = _remote_sha(repo, source_ref)
    if actual != source_sha:
        raise PagesPublishError(
            f"source ref moved: {source_ref} expected {source_sha}, found {actual}"
        )


def _prepare_worktree(repo: Path, branch: str, target: Path) -> bool:
    fetch = _run(
        [
            "git",
            "fetch",
            "--no-tags",
            "origin",
            f"refs/heads/{branch}:refs/remotes/origin/{branch}",
        ],
        cwd=repo,
        check=False,
    )
    exists = fetch.returncode == 0
    if exists:
        _run(
            [
                "git",
                "worktree",
                "add",
                "--detach",
                str(target),
                f"refs/remotes/origin/{branch}",
            ],
            cwd=repo,
        )
    else:
        _run(["git", "worktree", "add", "--detach", str(target), "HEAD"], cwd=repo)
        _run(["git", "switch", "--orphan", branch], cwd=target)
        _run(["git", "rm", "-rf", "."], cwd=target, check=False)

    _run(["git", "config", "user.name", "github-actions[bot]"], cwd=target)
    _run(
        [
            "git",
            "config",
            "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com",
        ],
        cwd=target,
    )
    return exists


def _replace_site(source: Path, target: Path) -> None:
    if not source.is_dir():
        raise PagesPublishError(f"generated site does not exist: {source}")

    for child in tuple(target.iterdir()):
        if child.name == ".git":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()

    for child in source.iterdir():
        destination = target / child.name
        if child.is_dir():
            shutil.copytree(child, destination)
        else:
            shutil.copy2(child, destination)

    (target / ".nojekyll").write_text("", encoding="utf-8")


def publish(
    *,
    repo: Path,
    site: Path,
    source_ref: str,
    source_sha: str,
) -> str:
    repo = repo.resolve()
    site = site.resolve()
    branch = _load_pages_branch(repo)
    _require_fresh_source(repo, source_ref, source_sha)

    with tempfile.TemporaryDirectory(prefix="cad-pages-publish-") as tmp:
        worktree = Path(tmp) / "gh-pages"
        try:
            _prepare_worktree(repo, branch, worktree)
            _replace_site(site, worktree)
            _run(["git", "add", "-A"], cwd=worktree)

            diff = _run(
                ["git", "diff", "--cached", "--quiet"],
                cwd=worktree,
                check=False,
            )
            if diff.returncode == 0:
                return _run(["git", "rev-parse", "HEAD"], cwd=worktree).stdout.strip()

            _run(
                ["git", "commit", "-m", f"pages: {source_ref} {source_sha}"],
                cwd=worktree,
            )
            commit = _run(["git", "rev-parse", "HEAD"], cwd=worktree).stdout.strip()
            _require_fresh_source(repo, source_ref, source_sha)
            _run(
                ["git", "push", "origin", f"HEAD:refs/heads/{branch}"],
                cwd=worktree,
            )
            return commit
        finally:
            _run(
                ["git", "worktree", "remove", "--force", str(worktree)],
                cwd=repo,
                check=False,
            )
            _run(["git", "worktree", "prune"], cwd=repo, check=False)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--site", type=Path, required=True)
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args(argv)

    commit = publish(
        repo=args.repo,
        site=args.site,
        source_ref=args.source_ref,
        source_sha=args.source_sha,
    )
    print(f"Pages commit: {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
