"""Execute repository-local /merge policy."""

from __future__ import annotations

import argparse
import json
import os
from urllib import error, request

from .policy import MergePolicyError, is_main_governance, merge_method


_ALLOWED_CI_RESULTS = {"success", "neutral", "skipped"}
_MAIN_GOVERNANCE_PATHS = frozenset({
    "AGENTS.md",
    "docs/plan.md",
    "docs/handoff.md",
})


def api(repository: str, path: str, token: str, *, method: str = "GET", body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = request.Request(
        f"https://api.github.com/repos/{repository}/{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with request.urlopen(req) as response:
            if response.status == 204:
                return None
            return json.load(response)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise MergePolicyError(f"GitHub API {exc.code}: {detail}") from exc


def pull_request_files(
    repository: str,
    pull_request_number: int,
    token: str,
) -> tuple[str, ...]:
    """Return every changed path, following GitHub's PR-files pagination."""

    result = []
    page = 1
    while True:
        rows = api(
            repository,
            f"pulls/{pull_request_number}/files?per_page=100&page={page}",
            token,
        )
        if not isinstance(rows, list):
            raise MergePolicyError("pull request files response must be a list")
        for row in rows:
            filename = row.get("filename") if isinstance(row, dict) else None
            if not isinstance(filename, str) or not filename:
                raise MergePolicyError("pull request file has no filename")
            result.append(filename)
        if len(rows) < 100:
            break
        page += 1
    return tuple(result)


def require_main_governance_paths(
    repository: str,
    pull_request_number: int,
    token: str,
) -> None:
    """Fail closed unless a docs->main PR is governance-only."""

    paths = pull_request_files(repository, pull_request_number, token)
    if not paths:
        raise MergePolicyError("main governance pull request has no changed files")
    forbidden = sorted(set(paths) - _MAIN_GOVERNANCE_PATHS)
    if forbidden:
        raise MergePolicyError(
            "main governance pull request may change only "
            "AGENTS.md, docs/plan.md and docs/handoff.md; "
            f"forbidden: {', '.join(forbidden)}"
        )


def require_green_ci(
    repository: str,
    sha: str,
    pull_request_number: int,
    token: str,
) -> None:
    checks = api(repository, f"commits/{sha}/check-runs", token).get("check_runs", [])
    ci_checks = [
        check
        for check in checks
        if check.get("name") == "ci"
        and any(
            pr.get("number") == pull_request_number
            for pr in check.get("pull_requests", [])
        )
    ]

    if not ci_checks:
        raise MergePolicyError("pull request has no central ci check")

    pending = [
        check
        for check in ci_checks
        if check.get("status") != "completed"
    ]
    if pending:
        raise MergePolicyError("central ci check is still running")

    failed = [
        check
        for check in ci_checks
        if check.get("conclusion") not in _ALLOWED_CI_RESULTS
    ]
    if failed:
        raise MergePolicyError("central ci check is not green")


def merge_required(pr: dict) -> bool:
    if pr.get("merged"):
        return False
    if pr.get("state") != "open":
        raise MergePolicyError("pull request is closed without merge")
    return True


def dispatch_workflow(repository: str, workflow: str, ref: str, token: str) -> None:
    api(
        repository,
        f"actions/workflows/{workflow}/dispatches",
        token,
        method="POST",
        body={"ref": ref},
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True)
    parser.add_argument("--pull-request-number", required=True, type=int)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--repository-owner", required=True)
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN")
    if not token:
        raise MergePolicyError("GH_TOKEN is required")
    if args.actor != args.repository_owner:
        raise MergePolicyError("only the repository owner may execute /merge")

    pr = api(args.repository, f"pulls/{args.pull_request_number}", token)
    if not merge_required(pr):
        print(pr.get("merge_commit_sha") or "already merged")
        return

    base = pr["base"]["ref"]
    head = pr["head"]["ref"]
    method = merge_method(head=head, base=base)
    if is_main_governance(head=head, base=base):
        require_main_governance_paths(
            args.repository,
            args.pull_request_number,
            token,
        )
    head_sha = pr["head"]["sha"]
    require_green_ci(
        args.repository,
        head_sha,
        args.pull_request_number,
        token,
    )

    result = api(
        args.repository,
        f"pulls/{args.pull_request_number}/merge",
        token,
        method="PUT",
        body={"sha": head_sha, "merge_method": method},
    )
    if not result.get("merged"):
        raise MergePolicyError(result.get("message", "GitHub did not merge PR"))

    dispatch_workflow(args.repository, "ci.yml", base, token)
    dispatch_workflow(args.repository, "branch-cleanup.yml", base, token)
    print(result["sha"])


if __name__ == "__main__":
    main()
