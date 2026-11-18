"""Focused tests for shared model-root mapping and output lookup."""

from __future__ import annotations

from pathlib import Path
import json
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

import model_item  # noqa: E402


class ModelItemTests(unittest.TestCase):
    def test_shared_roots_expose_all_catalog_members(self):
        self.assertEqual(
            model_item.item_members(ROOT / "models/components/guide_rail"),
            ("guide-rail", "guide-rail-makita"),
        )
        self.assertEqual(
            model_item.item_members(ROOT / "models/advanced/simple_mft"),
            ("simple-mft", "simple-mft-assembly"),
        )

    def test_nested_sources_stay_in_their_physical_model_root(self):
        """Implementation/assembly subfolders do not become extra CI items."""

        self.assertEqual(
            model_item.catalog_root("hub75-panel"),
            Path("models/components/hub75_panel"),
        )
        self.assertEqual(
            model_item.catalog_root("simple-mft-assembly"),
            Path("models/advanced/simple_mft"),
        )

    def test_item_dependencies_are_unique_folder_dependencies(self):
        self.assertEqual(
            model_item.item_dependencies("simple-mft"),
            ("guide-rail",),
        )
        self.assertEqual(
            model_item.item_dependencies("hub75-wood-frame"),
            ("corner-bracket",),
        )
        self.assertEqual(
            model_item.item_dependencies("hub75-display2"),
            ("corner-bracket",),
        )

    def test_current_output_is_preferred_over_stable_fallback(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            current = root / "output/models/plate/scpf/solidcraft.json"
            stable = (
                root
                / "generated-build/main/models/basic/plate/scpf/model"
                / "generated/scpf/solidcraft.json"
            )
            current.parent.mkdir(parents=True)
            stable.parent.mkdir(parents=True)
            current.write_text("current", encoding="utf-8")
            stable.write_text("stable", encoding="utf-8")

            with patch.object(model_item, "ROOT", root):
                path, source = model_item._existing_commands("plate", "scpf")

            self.assertEqual(path, current)
            self.assertEqual(source, "current-run")

    def test_package_item_combines_current_and_stable_shared_variants(self):
        """A shared item packages fresh output plus an unchanged stable sibling."""

        with TemporaryDirectory() as temp:
            root = Path(temp)
            item_root = root / "models/components/guide_rail"
            item_root.mkdir(parents=True)
            output = root / "build/models/components/guide_rail"

            def write_result(base, slug, commit):
                target = base / model_item.model_build_path(slug)
                native = target / "native"
                native.mkdir(parents=True)
                (native / "model.sc").write_text(
                    f"{slug}-native",
                    encoding="utf-8",
                )
                (target / "verification.json").write_text(
                    json.dumps(
                        {
                            "model": slug,
                            "verified": True,
                            "source_commit": commit,
                        }
                    ),
                    encoding="utf-8",
                )

            write_result(
                root / "output/candidate",
                "guide-rail",
                "current",
            )
            write_result(
                root / "generated-build/main",
                "guide-rail-makita",
                "stable",
            )

            with patch.object(model_item, "ROOT", root), patch.dict(
                model_item.os.environ,
                {
                    "CAD_CI_ITEM_PATH": str(item_root),
                    "CAD_CI_OUTPUT": str(output),
                },
            ):
                model_item.package_item()

            current = json.loads(
                (output / "results/guide-rail/verification.json").read_text(
                    encoding="utf-8"
                )
            )
            stable = json.loads(
                (
                    output
                    / "results/guide-rail-makita/verification.json"
                ).read_text(encoding="utf-8")
            )
            summary = json.loads(
                (output / "checks/package.json").read_text(
                    encoding="utf-8"
                )
            )

        self.assertEqual(current["source_commit"], "current")
        self.assertEqual(stable["source_commit"], "stable")
        self.assertEqual(
            summary["models"]["guide-rail"]["source"],
            "current-run",
        )
        self.assertEqual(
            summary["models"]["guide-rail-makita"]["source"],
            "stable-build",
        )


if __name__ == "__main__":
    unittest.main()
