import json
from pathlib import Path
import unittest

from scripts.import_context_package import validate_package


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def load_flat_example(relative_path: str) -> dict:
    result = {}
    for raw_line in read(relative_path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        result[key.strip()] = json.loads(value) if value.startswith("[") else value.strip('"')
    return result


class PostSnapshotFinalRegressionTests(unittest.TestCase):
    def test_expected_workflow_inventory_and_removed_duplicates(self):
        workflow_names = {
            path.name
            for path in WORKFLOWS.iterdir()
            if path.suffix in {".yml", ".yaml"}
        }
        self.assertEqual(len(workflow_names), 15)
        self.assertNotIn("cks-preflight.yml", workflow_names)
        self.assertNotIn("cks-release-check.yml", workflow_names)
        self.assertIn("cks-integration-test.yml", workflow_names)
        self.assertIn("cks-validation.yml", workflow_names)

    def test_false_green_repairs_remain_fail_closed_and_wired(self):
        bootstrap = read("scripts/validate_bootstrap.py")
        control_plane = read("validators/control_plane_validator.py")
        bootstrap_workflow = read(".github/workflows/bootstrap-check.yml")
        control_workflow = read(".github/workflows/cks-control-plane-validation.yml")

        self.assertIn("raise SystemExit(main())", bootstrap)
        self.assertIn("return 0 if ok else 1", bootstrap)
        self.assertIn("raise SystemExit(main())", control_plane)
        self.assertIn('return 0 if result["status"] == "PASS" else 1', control_plane)
        self.assertIn("test_cks_workflow_exit_semantics_stage_e3_2_a.py", bootstrap_workflow)
        self.assertIn("test_cks_workflow_exit_semantics_stage_e3_2_a.py", control_workflow)

    def test_integration_gate_executes_real_tests_and_watches_contract_surface(self):
        workflow = read(".github/workflows/cks-integration-test.yml")
        runner = read("scripts/run_integration_tests.py")

        self.assertIn("python scripts/run_integration_tests.py", workflow)
        for required_path in (
            "schemas/context_package_kat9i_v1.yaml",
            "scripts/import_context_package.py",
            "scripts/run_integration_tests.py",
            "adapters/**",
            "examples/kat9i_os_import/context_package.yaml",
            "tests/test_cks_context_package_integration_stage_e3_2_c2f2.py",
        ):
            self.assertGreaterEqual(workflow.count(required_path), 2, required_path)

        self.assertIn("unittest.defaultTestLoader.discover", runner)
        self.assertIn("test_count == 0", runner)
        self.assertIn('raise SystemExit(0 if summary["status"] == "PASS" else 1)', runner)
        self.assertNotIn('"status": "PASS", "tests": 2', runner)

    def test_kat9i_example_matches_active_validator(self):
        package = load_flat_example("examples/kat9i_os_import/context_package.yaml")
        self.assertTrue(validate_package(package))
        self.assertEqual(package["source_system"], "KAT9I_OS")
        self.assertEqual(package["split_mode"], "SPLIT")
        self.assertEqual(package["artifacts"], ["decision.yaml", "evidence.yaml"])

    def test_knowledge_runtime_trigger_gap_does_not_return(self):
        workflow = read(".github/workflows/cks-knowledge-runtime-intelligence.yml")
        self.assertGreaterEqual(workflow.count("tools/cks_ci.py"), 2)

    def test_node24_guard_is_present_and_wired(self):
        validation = read(".github/workflows/cks-validation.yml")
        guard = ROOT / "tests" / "test_cks_github_actions_node24_stage_e3_3.py"
        self.assertTrue(guard.exists())
        self.assertIn("test_cks_github_actions_node24_stage_e3_3.py", validation)
        self.assertNotIn("actions/checkout@v4", "\n".join(read(str(p.relative_to(ROOT))) for p in WORKFLOWS.glob("*.yml")))
        self.assertNotIn("actions/setup-python@v5", "\n".join(read(str(p.relative_to(ROOT))) for p in WORKFLOWS.glob("*.yml")))
        self.assertNotIn("actions/upload-artifact@v4", "\n".join(read(str(p.relative_to(ROOT))) for p in WORKFLOWS.glob("*.yml")))


if __name__ == "__main__":
    unittest.main()
