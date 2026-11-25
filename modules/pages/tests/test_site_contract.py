from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
SITE = ROOT / "site"


class SiteContractTests(unittest.TestCase):
    def test_site_mounts_source_metadata_and_stable_build_scope(self):
        mounts = (SITE / "config/_default/module.toml").read_text(
            encoding="utf-8"
        )
        self.assertIn('source = "../models"', mounts)
        self.assertIn('target = "assets/cad-source"', mounts)
        self.assertIn('source = "../prepared-build/main"', mounts)
        self.assertIn('target = "assets/build"', mounts)

    def test_adapter_joins_model_ci_build_plan_and_catalog_without_model_names(self):
        adapter = (SITE / "content/models/_content.gotmpl").read_text(
            encoding="utf-8"
        )
        self.assertIn('resources.Match "cad-source/**/model.yml"', adapter)
        self.assertIn('resources.Get (printf "cad-source/%s/ci.yml"', adapter)
        self.assertIn('resources.Get "build/build-plan.json"', adapter)
        self.assertIn('index $ci "variants"', adapter)
        self.assertIn('where $rows "id" $slug', adapter)
        self.assertIn("hugo.Data.cad.model_history", adapter)
        self.assertIn("hugo.Data.cad.catalog", adapter)
        self.assertIn('"dates" (dict "lastmod" $lastmod)', adapter)
        self.assertIn('"cadGroup" $group', adapter)
        self.assertIn('unknown catalog section', adapter)
        self.assertIn('unknown catalog group', adapter)
        self.assertNotIn('dict "source" (printf "build/models/', adapter)
        self.assertNotIn('kind "build"', adapter)
        self.assertNotIn("simple-box", adapter)
        self.assertNotIn("simple-mft", adapter)

    def test_shared_layout_supports_model_owned_context_and_extra_views(self):
        page = (SITE / "layouts/models/single.html").read_text(encoding="utf-8")
        self.assertIn('.Resources.Get "page.md"', page)
        self.assertIn('index $m "extra_views"', page)
        self.assertIn('eq $kind "url"', page)
        self.assertIn('eq $kind "asset"', page)
        self.assertNotIn('image_url', page)
        self.assertIn('.Resources.Get "scpf-source.py"', page)
        self.assertIn('resources.Get (printf "build/%s" $commandsPath)', page)
        self.assertIn("raw.githubusercontent.com", page)
        self.assertIn("blob/build/%s/", page)
        self.assertIn("View STL on GitHub", page)
        self.assertNotIn("simple-box", page)
        self.assertNotIn("simple-mft", page)

    def test_catalog_layout_uses_configured_sections_groups_and_navigation(self):
        home = (SITE / "layouts/home.html").read_text(encoding="utf-8")
        catalog = (SITE / "layouts/models/list.html").read_text(encoding="utf-8")
        category = (SITE / "layouts/models/single.html").read_text(encoding="utf-8")
        groups = (SITE / "layouts/partials/cad/model-groups.html").read_text(
            encoding="utf-8"
        )
        card = (SITE / "layouts/partials/cad/model-card.html").read_text(
            encoding="utf-8"
        )
        menu = (SITE / "config/_default/menus.en.toml").read_text(
            encoding="utf-8"
        )
        taxonomy = (SITE / "data/cad/catalog.yml").read_text(encoding="utf-8")

        self.assertIn("Recently updated models", home)
        self.assertIn("ByLastmod.Reverse", home)
        self.assertIn("showUpdated", home)
        self.assertIn("hugo.Data.cad.catalog", catalog)
        self.assertIn('partial "cad/model-groups.html"', catalog)
        self.assertIn('partial "cad/model-groups.html"', category)
        self.assertIn("hugo.Data.cad.catalog", groups)
        self.assertIn("Params.cadGroup", groups)
        self.assertIn("cad-catalog-group", groups)
        self.assertIn("data-cad-group", groups)
        self.assertIn("hugo.Data.cad.catalog", card)
        self.assertIn("cadGroup", card)

        for section in ("basic", "components", "subassemblies", "assemblies"):
            self.assertIn(f"id: {section}", taxonomy)
        for group in ("display", "mft"):
            self.assertIn(f"id: {group}", taxonomy)
        for name in (
            "Models",
            "Basic",
            "Components",
            "Sub Assemblies",
            "Assemblies",
        ):
            self.assertIn(f'name = "{name}"', menu)
        self.assertNotIn('name = "Advanced"', menu)
        self.assertIn("Updated {{ $page.Lastmod.Format", card)

    def test_pages_build_passes_durable_scope_to_hugo(self):
        build = (ROOT / "modules/pages/src/cad_model_pages/build.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('env["HUGO_PARAMS_BUILDSCOPE"] = build_namespace', build)
        self.assertIn(
            'env["HUGO_PARAMS_CADSOURCEREPOSITORY"] = source_repository',
            build,
        )

    def test_pages_workflow_builds_main_and_dev_scopes(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("--build-scope prepared-build/main", workflow)
        self.assertIn("--destination generated-site", workflow)
        self.assertIn("--build-scope prepared-build/dev", workflow)
        self.assertIn("--destination generated-site/dev", workflow)
        self.assertIn("github.repository_owner", workflow)
        self.assertIn("github.event.repository.name", workflow)
        self.assertIn('--source-repository "${{ github.repository }}"', workflow)
        self.assertNotIn("2026-011-02.cad.solidcraft.NEW", workflow)
        self.assertNotIn("simple-box", workflow)
        self.assertNotIn("simple-mft", workflow)
        self.assertIn("fetch-depth: 0", workflow)

    def test_pages_pr_verifies_matching_durable_scope(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("github.base_ref == 'dev' || github.head_ref == 'dev'", workflow)
        self.assertIn("--build-scope prepared-build/$PAGES_SCOPE", workflow)
        self.assertNotIn('"models/**/model.yml"', workflow)
        self.assertNotIn('"models/**/page.md"', workflow)

    def test_pages_publish_jobs_run_only_from_explicit_dispatch(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("workflow_run:", workflow)
        self.assertIn("if: github.event_name == 'workflow_dispatch'", workflow)

    def test_pages_workflow_publishes_configured_gh_pages_branch(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(
            encoding="utf-8"
        )
        config = (ROOT / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("pages_branch: gh-pages", config)
        self.assertIn("cad_model_pages.publish", workflow)
        self.assertIn("--repo source-main", workflow)
        self.assertIn("contents: write", workflow)
        self.assertNotIn("actions/configure-pages", workflow)
        self.assertNotIn("actions/upload-pages-artifact", workflow)
        self.assertNotIn("actions/deploy-pages", workflow)
        self.assertNotIn("github-pages", workflow)

    def test_site_defaults_use_canonical_repository_name(self):
        config = (SITE / "config/_default/hugo.toml").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "brainboxemb/2026-011-02.cad.solidcraft",
            config,
        )
        self.assertNotIn("2026-011-02.cad.solidcraft.NEW", config)

    def test_catalog_card_images_are_lazy_and_async_decoded(self):
        card = (SITE / "layouts/partials/cad/model-card.html").read_text(
            encoding="utf-8"
        )
        self.assertIn('loading="lazy"', card)
        self.assertIn('decoding="async"', card)

    def test_site_uses_accepted_hextra_version(self):
        go_mod = (SITE / "go.mod").read_text(encoding="utf-8")
        self.assertIn("github.com/imfing/hextra v0.13.0", go_mod)


if __name__ == "__main__":
    unittest.main()
