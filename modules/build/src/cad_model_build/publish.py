"""Publish permanent-lane or rolling test model output to the generated build branch."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from .config import active_variant_ids, BuildConfigError, discover_models, load_project


class PublishError(RuntimeError):
    """Build publication failed."""


def _run(command: list[str], *, cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=cwd,
        check=check,
        capture_output=True,
        text=True,
    )


def _remote_sha(repo: Path, ref: str) -> str | None:
    result = _run(
        ["git", "ls-remote", "--heads", "origin", f"refs/heads/{ref}"],
        cwd=repo,
    )
    line = result.stdout.strip()
    if not line:
        return None
    return line.split()[0]


def _require_fresh_source(repo: Path, source_ref: str, source_sha: str) -> None:
    actual = _remote_sha(repo, source_ref)
    if actual != source_sha:
        raise PublishError(
            f"source ref moved: {source_ref} expected {source_sha}, found {actual}"
        )


def _read_plan(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PublishError(f"missing build plan: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PublishError(f"invalid build plan: {path}: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema") != 1:
        raise PublishError(f"unsupported build plan: {path}")
    if not isinstance(value.get("models"), list):
        raise PublishError(f"build plan models must be a list: {path}")
    return value


def _write_plan(path: Path, plan: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(plan, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _merge_plan(
    existing: dict | None,
    candidate: dict,
    *,
    active_ids: set[str],
    full: bool,
) -> dict:
    if full or existing is None:
        result = dict(candidate)
        result["models"] = sorted(candidate["models"], key=lambda row: row["id"])
        return result

    if existing.get("schema") != 1 or existing.get("namespace") != candidate.get("namespace"):
        raise PublishError("existing build plan is incompatible with candidate scope")

    rows = {
        row["id"]: row
        for row in existing.get("models", [])
        if isinstance(row, dict)
        and isinstance(row.get("id"), str)
        and row["id"] in active_ids
    }
    for row in candidate["models"]:
        rows[row["id"]] = row

    result = dict(candidate)
    result["models"] = [rows[key] for key in sorted(rows)]
    return result


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
            ["git", "worktree", "add", "--detach", str(target), f"refs/remotes/origin/{branch}"],
            cwd=repo,
        )
    else:
        _run(["git", "worktree", "add", "--detach", str(target), "HEAD"], cwd=repo)
        _run(["git", "switch", "--orphan", branch], cwd=target)
        _run(["git", "rm", "-rf", "."], cwd=target, check=False)
        for child in target.iterdir():
            if child.name != ".git":
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
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


def _copy_model(candidate_scope: Path, published_scope: Path, model_id: str) -> None:
    source = candidate_scope / "models" / model_id
    if not source.is_dir():
        raise PublishError(f"missing candidate model output: {source}")
    target = published_scope / "models" / model_id
    if target.exists():
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)


def _update_scope(
    *,
    worktree: Path,
    candidate_scope: Path,
    candidate_plan: dict,
    active_ids: set[str],
    namespace: str,
    full: bool,
) -> None:
    published_scope = worktree / namespace
    existing_plan_path = published_scope / "build-plan.json"
    existing_plan = _read_plan(existing_plan_path) if existing_plan_path.is_file() else None

    if full:
        if published_scope.exists():
            shutil.rmtree(published_scope)
        shutil.copytree(candidate_scope, published_scope)
        _write_plan(
            published_scope / "build-plan.json",
            _merge_plan(None, candidate_plan, active_ids=active_ids, full=True),
        )
        return

    published_models = published_scope / "models"
    if published_models.is_dir():
        for child in tuple(published_models.iterdir()):
            if child.is_dir() and child.name not in active_ids:
                shutil.rmtree(child)

    for row in candidate_plan["models"]:
        model_id = row.get("id")
        if not isinstance(model_id, str):
            raise PublishError("candidate plan model is missing id")
        _copy_model(candidate_scope, published_scope, model_id)

    merged = _merge_plan(
        existing_plan,
        candidate_plan,
        active_ids=active_ids,
        full=False,
    )
    _write_plan(existing_plan_path, merged)


def _update_test_scope(
    *,
    worktree: Path,
    candidate_scope: Path,
    candidate_plan: dict,
    active_ids: set[str],
    baseline_namespace: str,
) -> None:
    """Materialize one complete rolling review scope from dev plus candidate."""

    baseline_scope = worktree / baseline_namespace
    baseline_plan_path = baseline_scope / "build-plan.json"
    if not baseline_plan_path.is_file():
        raise PublishError(
            f"rolling test output requires durable {baseline_namespace!r} baseline"
        )

    baseline_plan = _read_plan(baseline_plan_path)
    if baseline_plan.get("namespace") != baseline_namespace:
        raise PublishError("rolling test baseline namespace is invalid")

    published_scope = worktree / "test"
    if published_scope.exists():
        shutil.rmtree(published_scope)
    shutil.copytree(baseline_scope, published_scope)

    published_models = published_scope / "models"
    if published_models.is_dir():
        for child in tuple(published_models.iterdir()):
            if child.is_dir() and child.name not in active_ids:
                shutil.rmtree(child)

    rows = {
        row["id"]: row
        for row in baseline_plan.get("models", [])
        if isinstance(row, dict)
        and isinstance(row.get("id"), str)
        and row["id"] in active_ids
    }

    for row in candidate_plan["models"]:
        model_id = row.get("id")
        if not isinstance(model_id, str):
            raise PublishError("candidate plan model is missing id")
        _copy_model(candidate_scope, published_scope, model_id)
        rows[model_id] = row

    result = dict(candidate_plan)
    result["models"] = [rows[key] for key in sorted(rows)]
    _write_plan(published_scope / "build-plan.json", result)


def publish(
    *,
    repo: Path,
    namespace: str,
    source_ref: str,
    source_sha: str,
    full: bool = False,
    attempts: int = 3,
) -> str | None:
    repo = repo.resolve()
    project = load_project(repo)
    permanent = {
        project.stable_branch,
        project.development_branch,
        project.experimental_branch,
    }
    if namespace == "test":
        if source_ref in permanent:
            raise PublishError("test output must come from a temporary source branch")
        if not full:
            raise PublishError("test output must replace the complete test scope")
    else:
        if namespace not in permanent:
            raise BuildConfigError(f"cannot publish namespace {namespace!r}")
        if source_ref != namespace:
            raise PublishError(
                f"source ref {source_ref!r} must match build namespace {namespace!r}"
            )

    candidate_scope = repo / project.output_root / namespace
    candidate_plan = _read_plan(candidate_scope / "build-plan.json")
    if candidate_plan.get("namespace") != namespace:
        raise PublishError("candidate plan namespace does not match publication scope")
    if candidate_plan.get("source_sha") != source_sha:
        raise PublishError("candidate plan source SHA does not match publication source")
    if candidate_plan.get("source_ref") != source_ref:
        raise PublishError("candidate plan source ref does not match publication source")
    if not candidate_plan["models"]:
        return None

    active_ids = active_variant_ids(discover_models(repo, project))
    _require_fresh_source(repo, source_ref, source_sha)

    for attempt in range(1, attempts + 1):
        with tempfile.TemporaryDirectory(prefix="cad-build-publish-") as tmp:
            worktree = Path(tmp) / "build-branch"
            try:
                _prepare_worktree(repo, project.build_branch, worktree)
                if namespace == "test":
                    _update_test_scope(
                        worktree=worktree,
                        candidate_scope=candidate_scope,
                        candidate_plan=candidate_plan,
                        active_ids=active_ids,
                        baseline_namespace=project.development_branch,
                    )
                else:
                    _update_scope(
                        worktree=worktree,
                        candidate_scope=candidate_scope,
                        candidate_plan=candidate_plan,
                        active_ids=active_ids,
                        namespace=namespace,
                        full=full,
                    )
                _run(["git", "add", namespace], cwd=worktree)
                diff = _run(
                    ["git", "diff", "--cached", "--quiet"],
                    cwd=worktree,
                    check=False,
                )
                if diff.returncode == 0:
                    return _run(["git", "rev-parse", "HEAD"], cwd=worktree).stdout.strip()

                _run(
                    ["git", "commit", "-m", f"build: {namespace} {source_sha}"],
                    cwd=worktree,
                )
                commit = _run(["git", "rev-parse", "HEAD"], cwd=worktree).stdout.strip()
                _require_fresh_source(repo, source_ref, source_sha)
                pushed = _run(
                    [
                        "git",
                        "push",
                        "origin",
                        f"HEAD:refs/heads/{project.build_branch}",
                    ],
                    cwd=worktree,
                    check=False,
                )
                if pushed.returncode == 0:
                    return commit
            finally:
                _run(
                    ["git", "worktree", "remove", "--force", str(worktree)],
                    cwd=repo,
                    check=False,
                )
                _run(["git", "worktree", "prune"], cwd=repo, check=False)

        if attempt == attempts:
            raise PublishError(
                f"could not update {project.build_branch!r} after {attempts} attempts"
            )

    raise AssertionError("unreachable")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args(argv)

    commit = publish(
        repo=args.repo,
        namespace=args.namespace,
        source_ref=args.source_ref,
        source_sha=args.source_sha,
        full=args.full,
    )
    if commit is None:
        print("No materialized model output; build branch unchanged")
    else:
        print(f"Build commit: {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
