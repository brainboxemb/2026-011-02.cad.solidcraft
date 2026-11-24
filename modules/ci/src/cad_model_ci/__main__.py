"""CLI entrypoint for project CI."""

from __future__ import annotations

import os
from pathlib import Path

from .config import current_branch, full_selection, load_build, load_project
from .history import changed_paths, last_successful_dev_sha
from .items import discover_models, discover_modules, select
from .runner import execute
from .selection import changed_selection, expand_model_dependents


def _selection(repo, project, branch, modules, models):
    event = os.environ.get("GITHUB_EVENT_NAME", "")
    base = os.environ.get("GITHUB_BASE_REF", "")

    if branch == project.stable_branch:
        return full_selection(branch)

    if (
        event == "pull_request"
        and branch == project.development_branch
        and base == project.stable_branch
    ):
        return full_selection(branch)

    if (
        branch == project.development_branch
        and event in {"push", "workflow_dispatch"}
    ):
        token = os.environ.get("GH_TOKEN", "")
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        target = os.environ.get("GITHUB_SHA", "")
        run_id = os.environ.get("GITHUB_RUN_ID", "")
        if not all((token, repository, target, run_id.isdigit())):
            return full_selection(branch)

        baseline = last_successful_dev_sha(
            repository=repository,
            branch=branch,
            token=token,
            current_run_id=int(run_id),
            target_sha=target,
        )
        if baseline is None:
            return full_selection(branch)

        paths = changed_paths(repo, baseline, target)
        if paths is None:
            return full_selection(branch)

        return changed_selection(
            branch=branch,
            paths=paths,
            modules=modules,
            models=models,
        )

    return load_build(repo, branch) or full_selection(branch)


def _output_namespace(project, branch: str) -> str:
    base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if base in {project.stable_branch, project.development_branch}:
        return base
    if branch in {project.stable_branch, project.development_branch}:
        return branch
    return project.development_branch


def main() -> None:
    repo = Path.cwd()
    project = load_project(repo)
    branch = current_branch(repo)

    modules = discover_modules(repo, project)
    models = discover_models(repo, project)
    selection = expand_model_dependents(
        _selection(repo, project, branch, modules, models),
        models,
    )

    execute(
        repo=repo,
        project=project,
        selection=selection,
        namespace=_output_namespace(project, branch),
        modules=select(modules, selection.modules),
        models=select(models, selection.models),
    )


if __name__ == "__main__":
    main()
