"""Consistency checks for the central CAD model catalog."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import (  # noqa: E402
    MODELS,
    SECTION_INFO,
    SOURCES,
    COMMAND_SOURCES,
    COMPONENT_SOURCES,
    COMPONENT_DEFINITION_PRIMARY,
    SECTIONS,
    model_slugs,
    model_build_path,
    model_dependencies,
    model_input_paths,
)


class ModelCatalogTests(unittest.TestCase):
    def test_every_model_has_complete_metadata_and_existing_source(self):
        required = {
            "source",
            "section",
            "title",
            "tagline",
            "description",
            "parameters",
            "diagram",
            "stages",
            "native",
            "native_snapshot_required",
        }
        self.assertEqual(
            model_build_path("guide-rail-makita"),
            Path("models/components/guide_rail/scpf/makita"),
        )
        self.assertEqual(
            model_build_path("simple-mft-assembly"),
            Path("models/advanced/simple_mft/scpf/assemblies/guide_rail"),
        )
        self.assertEqual(
            len({model_build_path(slug) for slug in MODELS}),
            len(MODELS),
        )
        for slug, model in MODELS.items():
            with self.subTest(slug=slug):
                self.assertFalse(required - set(model))
                self.assertIn(model["section"], SECTION_INFO)
                self.assertTrue((ROOT / model["source"]).is_file())
                self.assertTrue(model["title"])
                self.assertTrue(model["tagline"])
                self.assertTrue(model["description"])
                self.assertTrue(model["stages"])
                if model["native_snapshot_required"]:
                    self.assertTrue(model["native"])

    def test_derived_tables_match_model_records(self):
        self.assertEqual(SOURCES, {
            slug: model["source"]
            for slug, model in MODELS.items()
        })
        self.assertEqual(COMMAND_SOURCES, {
            slug: model["scpc_source"]
            for slug, model in MODELS.items()
            if model.get("scpc_source")
        })
        self.assertEqual(COMPONENT_SOURCES, {
            slug: model["component_source"]
            for slug, model in MODELS.items()
            if model.get("component_source")
        })
        self.assertEqual(COMPONENT_DEFINITION_PRIMARY, frozenset(
            slug
            for slug, model in MODELS.items()
            if model.get("component_definition_primary")
        ))

    def test_sections_and_cli_selections_are_derived_from_catalog(self):
        self.assertEqual(set(model_slugs("scpf")), set(MODELS))
        self.assertEqual(set(model_slugs("scpc")), set(COMMAND_SOURCES))
        self.assertEqual(
            set(model_slugs("native")),
            {
                slug for slug, model in MODELS.items()
                if model["native"]
            },
        )
        self.assertEqual(
            set(model_slugs("native-snapshot-required")),
            {
                slug for slug, model in MODELS.items()
                if model["native_snapshot_required"]
            },
        )

        section_slugs = []
        for section, (_, _, slugs) in SECTIONS.items():
            self.assertEqual(
                slugs,
                tuple(
                    slug for slug, model in MODELS.items()
                    if model["section"] == section
                ),
            )
            section_slugs.extend(slugs)
        self.assertEqual(set(section_slugs), set(MODELS))

    def test_build_paths_mirror_source_model_roots(self):
        self.assertEqual(
            model_build_path("plate"),
            Path("models/basic/plate/scpf"),
        )
        self.assertEqual(
            model_build_path("hub75-panel"),
            Path("models/components/hub75_panel/detailed/scpf"),
        )
        for slug, model in MODELS.items():
            with self.subTest(slug=slug):
                source = Path(model["source"])
                build = model_build_path(slug)
                self.assertEqual(source.parts[:len(build.parts)], build.parts)
                self.assertNotIn("scpf", build.parts)
                self.assertNotIn("scpc", build.parts)

    def test_declared_model_dependencies_are_valid_and_acyclic(self):
        for slug in MODELS:
            with self.subTest(slug=slug):
                for dependency in model_dependencies(slug):
                    self.assertIn(dependency, MODELS)
                    self.assertNotEqual(dependency, slug)

                # model_input_paths walks the dependency graph; a cycle would
                # fail rather than silently selecting an incomplete set.
                paths = model_input_paths(slug)
                self.assertTrue(paths)

    def test_declared_extra_inputs_use_repository_relative_paths(self):
        for slug, model in MODELS.items():
            for path in model.get("extra_inputs", ()):
                with self.subTest(slug=slug, path=path):
                    self.assertFalse(Path(path).is_absolute())
                    self.assertTrue(path.endswith("/"))

    def test_scpc_metadata_is_complete(self):
        for slug, model in MODELS.items():
            with self.subTest(slug=slug):
                if "scpc_source" in model:
                    self.assertTrue((ROOT / model["scpc_source"]).is_file())
                    self.assertIsInstance(model.get("scpc_command_count"), int)
                    self.assertGreater(model["scpc_command_count"], 0)
                else:
                    self.assertNotIn("scpc_command_count", model)


if __name__ == "__main__":
    unittest.main()
