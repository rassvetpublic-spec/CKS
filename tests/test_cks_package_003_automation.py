import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "cks-package-003-automation.yml"


class Package003AutomationWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_continuous_and_manual_triggers_exist(self):
        self.assertIn("push:", self.text)
        self.assertIn("- main", self.text)
        self.assertIn("pull_request:", self.text)
        self.assertIn("workflow_dispatch:", self.text)

    def test_environment_is_explicit_and_history_is_complete(self):
        self.assertIn("actions/checkout@v5", self.text)
        self.assertIn("fetch-depth: 0", self.text)
        self.assertIn("actions/setup-python@v6", self.text)
        self.assertIn("python-version: '3.12'", self.text)

    def test_full_test_suite_is_fail_closed_on_zero_tests(self):
        self.assertIn("countTestCases()", self.text)
        self.assertIn("count > 0", self.text)
        self.assertIn("python -m unittest discover -s tests -p 'test_*.py' -v", self.text)
        self.assertIn("python scripts/run_integration_tests.py", self.text)

    def test_package_003_tools_are_wired(self):
        required = (
            "tools/cks_index_generator.py",
            "tools/cks_migration_audit.py",
            "tools/cks_ci.py --mode traceability",
            "tools/cks_ci.py --mode canon",
            "tools/cks_ci.py --mode review-gate",
            "tools/cks_governance_runner.py",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_package_artifacts_are_published_even_on_failure(self):
        self.assertIn("if: always()", self.text)
        self.assertIn("actions/upload-artifact@v6", self.text)
        self.assertIn("artifacts/cks-package-003/", self.text)
        self.assertIn("artifacts/cks-ci/", self.text)
        self.assertIn("cks-package-003-evidence", self.text)

    def test_workflow_remains_validation_only(self):
        forbidden = (
            "git push",
            "gh pr merge",
            "contents: write",
            "issues: write",
            "pull-requests: write",
        )
        lowered = self.text.lower()
        for marker in forbidden:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, lowered)


if __name__ == "__main__":
    unittest.main()
