"""Tests for model-root tool.cad.ci ownership in the CAD repository."""

from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path
import sys
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import MODELS, direct_input_paths  # noqa: E402
import model_item  # noqa: E402


def watch_matches(path: str, pattern: str) -> bool:
    """Apply tool.cad.ci watch semantics needed by these config tests."""

    if pattern.endswith("/**"):
        prefix = pattern[:-3].rstrip("/")
        return path == prefix or path.startswith(prefix + "/")
    return fnmatch(path, pattern)


class ToolCadCiMigrationTests(unittest.TestCase):
    def config_for(self, item_id: str) -> dict:
        """Load the ci.yml owned by one derived model-root item."""

        root = model_item.catalog_root(item_id)
        return yaml.safe_load(
            (ROOT / root / "ci.yml").read_text(encoding="utf-8")
        )

    def item_ids(self) -> tuple[str, ...]:
        """Return one stable item ID for every unique catalog model root."""

        result: list[str] = []
        for slug in MODELS:
            item_id = model_item.item_id_for_slug(slug)
            if item_id not in result:
                result.append(item_id)
        return tuple(result)

    def test_root_config_discovers_model_root_folders(self):
        """The root config discovers folders, not a second list of model slugs."""

        data = yaml.safe_load(
            (ROOT / "cad-ci.yml").read_text(encoding="utf-8")
        )
        self.assertEqual(data["schema"], 1)
        self.assertEqual(
            data["items"],
            [
                "models/basic/*",
                "models/components/*",
                "models/advanced/*",
            ],
        )

    def test_every_catalog_root_owns_one_ci_file(self):
        """Every catalog model is covered by its physical model-root folder."""

        for item_id in self.item_ids():
            config = self.config_for(item_id)
            self.assertEqual(config["id"], item_id)

    def test_shared_catalog_variants_use_one_item(self):
        """Variants in one folder must not create artificial nested CI items."""

        self.assertEqual(
            model_item.item_id_for_slug("guide-rail-makita"),
            "guide-rail",
        )
        self.assertEqual(
            model_item.item_id_for_slug("simple-mft-assembly"),
            "simple-mft",
        )
        self.assertEqual(
            model_item.item_members(
                ROOT / "models/components/guide_rail"
            ),
            ("guide-rail", "guide-rail-makita"),
        )

    def test_ci_dependencies_follow_catalog_dependencies(self):
        """Folder-level needs must stay derived from catalog relationships."""

        for item_id in self.item_ids():
            config = self.config_for(item_id)
            self.assertEqual(
                tuple(config.get("needs", ())),
                model_item.item_dependencies(item_id),
                item_id,
            )

    def test_external_model_inputs_are_watched_or_dependency_owned(self):
        """Shared source outside an item root must still select the owner."""

        for item_id in self.item_ids():
            config = self.config_for(item_id)
            watches = tuple(config.get("watch", ()))
            root = model_item.catalog_root(item_id).as_posix()
            needs = tuple(config.get("needs", ()))
            dependency_roots = tuple(
                model_item.catalog_root(need).as_posix()
                for need in needs
            )

            members = model_item.item_members(ROOT / root)
            for slug in members:
                for path in direct_input_paths(slug):
                    normalized = path.rstrip("/")
                    if normalized == root or normalized.startswith(root + "/"):
                        continue
                    if any(
                        normalized == dep or normalized.startswith(dep + "/")
                        for dep in dependency_roots
                    ):
                        continue
                    self.assertTrue(
                        any(watch_matches(normalized, watch) for watch in watches),
                        f"{item_id} does not watch external input {path}",
                    )

    def test_every_item_watches_shared_runner_and_keeps_reuse_off(self):
        """Parallel comparisons stay fresh until the old path is removed."""

        for item_id in self.item_ids():
            config = self.config_for(item_id)
            self.assertIn("scripts/ci/model_item.py", config["watch"])
            self.assertFalse(config["strategy"]["reuse"])
            self.assertEqual(
                [step["id"] for step in config["steps"]],
                ["compile", "compare-current", "package"],
            )
            package = config["steps"][-1]
            self.assertIn("results", package["outputs"])
            self.assertIn("checks/package.json", package["outputs"])

    def test_workflow_keeps_generated_branch_out_of_local_build(self):
        """Local tool output and durable generated-branch checkout stay separate."""

        workflow = (
            ROOT / ".github" / "workflows" / "cad.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("path: generated-build", workflow)
        self.assertIn("--build-root generated-build", workflow)
        self.assertNotIn("path: build\n", workflow)
        self.assertIn(
            "python scripts/ci/bootstrap_cad_ci.py",
            workflow,
        )
        exact_head_checkout = (
            "ref: $" +
            "{{ github.event_name == 'pull_request' && "
            "github.event.pull_request.head.sha || github.sha }}"
        )
        self.assertIn(exact_head_checkout, workflow)
        self.assertIn(
            "github.event.pull_request.head.repo.full_name == github.repository",
            workflow,
        )
        self.assertIn("build/models/**", workflow)


if __name__ == "__main__":
    unittest.main()
