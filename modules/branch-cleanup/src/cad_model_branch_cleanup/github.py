"""Small GitHub API client used only by branch cleanup."""

from __future__ import annotations

import json
from urllib import error, parse, request


class GitHubError(RuntimeError):
    """GitHub API request failed."""


class GitHubClient:
    def __init__(self, repository: str, token: str):
        self.repository = repository
        self.token = token

    def _request(self, path: str, *, method: str = "GET"):
        req = request.Request(
            f"https://api.github.com/repos/{self.repository}/{path}",
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        try:
            with request.urlopen(req) as response:
                if response.status == 204:
                    return None
                return json.load(response)
        except error.HTTPError as exc:
            if method == "DELETE" and exc.code in {404, 422}:
                return None
            detail = exc.read().decode("utf-8", errors="replace")
            raise GitHubError(f"GitHub API {exc.code}: {detail}") from exc

    def branches(self) -> list[str]:
        values = self._request("branches?per_page=100")
        return [item["name"] for item in values]

    def open_pr_exists(self, branch: str) -> bool:
        owner = self.repository.split("/", 1)[0]
        head = parse.quote(f"{owner}:{branch}", safe="")
        values = self._request(f"pulls?state=open&head={head}&per_page=100")
        return bool(values)

    def merged_pr_to(self, branch: str, base: str) -> bool:
        owner = self.repository.split("/", 1)[0]
        head = parse.quote(f"{owner}:{branch}", safe="")
        base_value = parse.quote(base, safe="")
        values = self._request(
            f"pulls?state=closed&head={head}&base={base_value}&per_page=100"
        )
        return any(item.get("merged_at") for item in values)

    def delete_branch(self, branch: str) -> None:
        encoded = parse.quote(branch, safe="")
        self._request(f"git/refs/heads/{encoded}", method="DELETE")
