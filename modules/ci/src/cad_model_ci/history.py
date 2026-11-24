"""Find a safe incremental baseline and changed Git paths."""

from __future__ import annotations

import json
import subprocess
from urllib import parse, request


class HistoryError(RuntimeError):
    """GitHub or Git history cannot provide a safe incremental baseline."""


def _json(url: str, token: str):
    req = request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with request.urlopen(req) as response:
        return json.load(response)


def last_successful_dev_sha(
    *,
    repository: str,
    branch: str,
    token: str,
    current_run_id: int,
    target_sha: str,
    workflow_file: str = "ci.yml",
) -> str | None:
    branch_value = parse.quote(branch, safe="")
    workflow_value = parse.quote(workflow_file, safe="")
    url = (
        f"https://api.github.com/repos/{repository}/actions/workflows/"
        f"{workflow_value}/runs?branch={branch_value}&status=success&per_page=100"
    )
    runs = _json(url, token).get("workflow_runs", [])
    for run in runs:
        if run.get("id") == current_run_id:
            continue
        if run.get("event") not in {"push", "workflow_dispatch"}:
            continue
        if run.get("status") != "completed" or run.get("conclusion") != "success":
            continue
        sha = run.get("head_sha")
        if isinstance(sha, str) and sha and sha != target_sha:
            return sha
    return None


def changed_paths(repo, baseline: str, target: str) -> tuple[str, ...] | None:
    ancestor = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", baseline, target],
        check=False,
    )
    if ancestor.returncode != 0:
        return None

    result = subprocess.run(
        ["git", "-C", str(repo), "diff", "--name-only", baseline, target, "--"],
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    )
