"""Execute repository-local /merge policy."""

from __future__ import annotations

import argparse
import json
import os
from urllib import error, request

from .policy import MergePolicyError, merge_method


_ALLOWED_CI_RESULTS = {"success", "neutral", "skipped"}


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
    base = pr["base"]["ref"]
    method = merge_method(head=pr["head"]["ref"], base=base)
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
