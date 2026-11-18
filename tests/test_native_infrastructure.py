"""Infrastructure checks for native CAD validation."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / "scripts" / "ci"
sys.path.insert(0, str(CI))

from model_catalog import MODELS  # noqa: E402
from native_cases import NATIVE_MUTATIONS  # noqa: E402
from native_checks import VALIDATORS  # noqa: E402


class NativeInfrastructureTests(unittest.TestCase):
    def test_validators_reference_registered_native_models(self):
        for slug in VALIDATORS:
            self.assertIn(slug, MODELS)
            self.assertTrue(MODELS[slug]["native"])

    def test_mutations_reference_registered_native_models(self):
        for slug, mutations in NATIVE_MUTATIONS.items():
            self.assertIn(slug, MODELS)
            self.assertTrue(MODELS[slug]["native"])
            names = [mutation["name"] for mutation in mutations]
            self.assertEqual(len(names), len(set(names)))
            for mutation in mutations:
                self.assertTrue(mutation["changes"])
                for parameter, expression in mutation["changes"].items():
                    self.assertIsInstance(parameter, str)
                    self.assertIsInstance(expression, str)

    def test_actions_expose_one_normal_cad_workflow_plus_image_worker(self):
        workflows = {
            path.name
            for path in (ROOT / ".github/workflows").glob("*.yml")
        }
        self.assertEqual(workflows, {"cad.yml", "image.yml"})

        cad = (ROOT / ".github/workflows/cad.yml").read_text(encoding="utf-8")
        image = (ROOT / ".github/workflows/image.yml").read_text(encoding="utf-8")
        self.assertIn("name: CAD", cad)
        self.assertIn("toolchain", image.lower())
        self.assertNotIn("workflow_run:", cad)

    def test_cad_workflow_is_thin_and_runner_owns_native_checks(self):
        workflow = (ROOT / ".github/workflows/cad.yml").read_text(
            encoding="utf-8"
        )
        pipeline = (ROOT / "scripts/ci/pipeline_ci.py").read_text(
            encoding="utf-8"
        )
        runner = (ROOT / "scripts/ci/native_ci.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("python scripts/ci/pipeline_ci.py", workflow)
        self.assertIn("native_ci.execute(", pipeline)
        self.assertNotIn("run_native_mutations.py", workflow)
        self.assertNotIn("native_validation.py", workflow)
        self.assertIn("scripts/ci/run_native_mutations.py", runner)
        self.assertIn("scripts/ci/native_validation.py", runner)
        self.assertNotIn('"command":"parameters.change"', workflow)
        self.assertNotIn("measurements-height-400.json", workflow)


if __name__ == "__main__":
    unittest.main()
