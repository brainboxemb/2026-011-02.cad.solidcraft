"""Tests for the first tool.cad.ci consumer boundary in the CAD repository."""

from __future__ import annotations

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class ToolCadCiMigrationTests(unittest.TestCase):
    def test_root_config_discovers_plate_as_model_root_item(self):
        """The first item is the Plate folder, not an invented central CI folder."""

        data = yaml.safe_load(
            (ROOT / "cad-ci.yml").read_text(encoding="utf-8")
        )
        self.assertEqual(data["schema"], 1)
        self.assertEqual(data["items"], ["models/basic/plate"])

    def test_plate_item_has_explicit_parallel_proof_steps(self):
        """Plate must compile, verify and compare with the current pipeline."""

        data = yaml.safe_load(
            (ROOT / "models/basic/plate/ci.yml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(data["id"], "plate")
        self.assertFalse(data["strategy"]["reuse"])
        self.assertEqual(
            [step["id"] for step in data["steps"]],
            ["compile", "verify", "compare-current"],
        )

    def test_workflow_keeps_durable_build_checkout_out_of_local_build(self):
        """tool.cad.ci owns local build/, so the generated branch uses another path."""

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
        self.assertIn(
            "ref: ${{ github.event_name == 'pull_request' && github.event.pull_request.head.sha || github.sha }}",
            workflow,
        )
        self.assertIn(
            "github.event.pull_request.head.repo.full_name == github.repository",
            workflow,
        )


if __name__ == "__main__":
    unittest.main()
