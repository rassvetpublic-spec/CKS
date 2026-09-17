import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import cks_governance_runner as runner


class GovernanceRunnerV2Tests(unittest.TestCase):
    def test_pass_when_all_checks_pass(self):
        with mock.patch.object(runner, "run_self_audit", return_value={"status": "PASS"}), \
             mock.patch.object(runner, "run_ci_validator", return_value={"status": "PASS"}):
            result = runner.run_all(ROOT)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["schema_version"], "2.0")
        self.assertEqual(result["runner_version"], "2")

    def test_fail_if_self_audit_fails(self):
        with mock.patch.object(runner, "run_self_audit", return_value={"status": "FAIL"}), \
             mock.patch.object(runner, "run_ci_validator", return_value={"status": "PASS"}):
            result = runner.run_all(ROOT)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["summary"]["failed_checks"], 1)

    def test_fail_if_ci_validator_fails(self):
        with mock.patch.object(runner, "run_self_audit", return_value={"status": "PASS"}), \
             mock.patch.object(runner, "run_ci_validator", return_value={"status": "FAIL"}):
            result = runner.run_all(ROOT)
        self.assertEqual(result["status"], "FAIL")

    def test_self_audit_exception_is_fail_closed(self):
        fake = mock.Mock()
        fake.run.side_effect = RuntimeError("boom")
        with mock.patch.object(runner, "SelfAudit", return_value=fake):
            result = runner.run_self_audit(ROOT)
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("RuntimeError", result["error"])

    def test_missing_ci_validator_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = runner.run_ci_validator(Path(tmp))
        self.assertEqual(result["status"], "FAIL")

    def test_workflow_is_continuous_and_publishes_report(self):
        text = (ROOT / ".github/workflows/cks-governance-runner.yml").read_text(encoding="utf-8")
        self.assertIn("push:", text)
        self.assertIn("branches:", text)
        self.assertIn("- main", text)
        self.assertIn("pull_request:", text)
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("--report artifacts/cks-governance/governance-report.json", text)
        self.assertIn("actions/upload-artifact@v6", text)


if __name__ == "__main__":
    unittest.main()
