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

    def test_adapter_joins_model_ci_and_build_plan_without_model_names(self):
        adapter = (SITE / "content/models/_content.gotmpl").read_text(
            encoding="utf-8"
        )
        self.assertIn('resources.Match "cad-source/**/model.yml"', adapter)
        self.assertIn('resources.Get (printf "cad-source/%s/ci.yml"', adapter)
        self.assertIn('resources.Get "build/build-plan.json"', adapter)
        self.assertIn('index $ci "variants"', adapter)
        self.assertIn('where $rows "id" $slug', adapter)
        self.assertNotIn("simple-box", adapter)
        self.assertNotIn("simple-mft", adapter)

    def test_shared_layout_supports_model_owned_context_and_extra_views(self):
        page = (SITE / "layouts/models/single.html").read_text(encoding="utf-8")
        self.assertIn('.Resources.Get "page.md"', page)
        self.assertIn('index $m "extra_views"', page)
        self.assertIn('.Resources.Get "scpf-source.py"', page)
        self.assertIn('.Resources.Get "solidcraft.json"', page)
        self.assertNotIn("simple-box", page)
        self.assertNotIn("simple-mft", page)

    def test_pages_workflow_builds_main_and_dev_scopes(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("--build-scope prepared-build/main", workflow)
        self.assertIn("--destination generated-site", workflow)
        self.assertIn("--build-scope prepared-build/dev", workflow)
        self.assertIn("--destination generated-site/dev", workflow)
        self.assertIn(
            'https://brainboxemb.github.io/2026-011-02.cad.solidcraft.NEW/dev/',
            workflow,
        )
        self.assertNotIn("simple-box", workflow)
        self.assertNotIn("simple-mft", workflow)

    def test_pages_pr_check_is_limited_to_pages_implementation(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn('"site/**"', workflow)
        self.assertIn('"modules/pages/**"', workflow)
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

    def test_site_uses_accepted_hextra_version(self):
        go_mod = (SITE / "go.mod").read_text(encoding="utf-8")
        self.assertIn("github.com/imfing/hextra v0.13.0", go_mod)


if __name__ == "__main__":
    unittest.main()
