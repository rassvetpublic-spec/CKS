import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "cks-package-003.yml"


class Package003WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_required_triggers_are_present(self):
        self.assertIn("push:", self.text)
        self.assertIn("- main", self.text)
        self.assertIn("pull_request:", self.text)
        self.assertIn("workflow_dispatch:", self.text)

    def test_existing_package003_implementations_are_reused(self):
        required = [
            "python tools/cks_index_generator.py",
            "python tools/cks_migration_audit.py",
            "python tools/cks_ci.py --mode traceability",
            "python tools/cks_ci.py --mode canon",
            "uses: ./.github/actions/cks-review-gate",
            "python tools/cks_governance_runner.py",
            "python scripts/run_integration_tests.py",
        ]
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_full_suite_has_explicit_zero_test_guard(self):
        self.assertIn('discover("tests", pattern="test_*.py")', self.text)
        self.assertIn("countTestCases()", self.text)
        self.assertIn("if count == 0:", self.text)
        self.assertIn("result.wasSuccessful()", self.text)

    def test_index_and_migration_reports_are_published(self):
        self.assertIn("cks-package003-knowledge-index", self.text)
        self.assertIn("artifacts/package003/knowledge-index.json", self.text)
        self.assertIn("cks-package003-migration-audit", self.text)
        self.assertIn("artifacts/package003/migration-audit.json", self.text)
        self.assertIn("actions/upload-artifact@v4", self.text)

    def test_workflow_does_not_write_canon_or_frozen_core(self):
        forbidden = [
            "> canon/",
            ">> canon/",
            "> decisions/",
            ">> decisions/",
            "git add canon",
            "git add decisions",
        ]
        lowered = self.text.lower()
        for fragment in forbidden:
            with self.subTest(fragment=fragment):
                self.assertNotIn(fragment, lowered)


if __name__ == "__main__":
    unittest.main()
